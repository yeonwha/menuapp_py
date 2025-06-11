from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
from decimal import Decimal
from .models import Food

class FoodAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create the admin user
        cls.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@example.com',
            password='adminpassword'
        )

        cls.food_admin_add_url = '/admin/menuapp/food/add/' 


    def setUp(self):
        # Initialize a Client
        self.client = Client()
        # Log in the admin user with the test account
        login_successful = self.client.login(username='admin_test', password='adminpassword')
        self.assertTrue(login_successful, "Admin user failed to log in for the test client.")

    # Test food model creating as admin user
    def test_create_food_via_admin(self):
        response = self.client.get(self.food_admin_add_url)

        if response.status_code == 302:
            print(f"Redirected to URL: {response.url}")

        self.assertEqual(response.status_code, 200, "Expected 200 OK for admin add page after successful login")

        # Ensure CSRF token is included
        self.assertIsNotNone(response.context, "Response context is None, could not get CSRF token.")
        self.assertIn('csrf_token', response.context, "CSRF token not found in response context.")
        csrf_token = response.context['csrf_token']


        # Data for a valid food item
        food_data = {
            'category': 'Main',
            'name': 'Cheese burger',
            'price': '7.99', 
            'checked': '', 
            '_save': 'Save', 
            'csrfmiddlewaretoken': csrf_token, 
        }

        # Submit the form with the valid data
        response = self.client.post(self.food_admin_add_url, food_data, follow=True) # follow=True to follow redirects

        # Check that the submission was successful (e.g., redirects to changelist or success page)
        self.assertEqual(response.status_code, 200) # Should be 200 after following redirect
        self.assertContains(response, 'was added successfully') # Check for success message

        # Verify the object was created in the database
        food = Food.objects.get(name='Cheese burger')
        self.assertEqual(food.category, 'Main')
        self.assertEqual(food.price, 7.99)
        self.assertEqual(food.checked, False) 

    def test_out_of_range_price_via_admin(self):
        # Test admin user is logged in with csrf token before attempt invaild data
        response = self.client.get(self.food_admin_add_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context)
        csrf_token = response.context['csrf_token']

        # Data for a food item with an out-of-range price
        food_data_too_big = {
            'category': 'Main',
            'name': 'Poke Too Big',
            'price': '1000.00', # greater than the maximum value 999.99
            'checked': 'off',
            '_save': 'Save',
            'csrfmiddlewaretoken': csrf_token,
        }
        food_data_too_small = {
            'category': 'Main',
            'name': 'Poke Too Small',
            'price': '0.09', # less than the minimum value 0.1
            'checked': 'off',
            '_save': 'Save',
            'csrfmiddlewaretoken': csrf_token,
        }

        # Test too big price
        response_get_big = self.client.get(self.food_admin_add_url)
        self.assertEqual(response_get_big.status_code, 200, "GET before too_big POST failed.")
        csrf_token_big = response_get_big.context['csrf_token']
        food_data_too_big['csrfmiddlewaretoken'] = csrf_token_big

        response_too_big = self.client.post(self.food_admin_add_url, food_data_too_big)
        self.assertEqual(response_too_big.status_code, 200, "POST for too_big did not return 200.")
        self.assertContains(response_too_big, 'Ensure this value is less than or equal to 999.99.', status_code=200)

        # Test too small price
        # 1. Get the form page AGAIN for a fresh CSRF token for 'too small' post
        response_get_small = self.client.get(self.food_admin_add_url)
        self.assertEqual(response_get_small.status_code, 200, "Expected 200 OK for GET before 'too small' POST.")

        # Ensure context exists before accessing CSRF token
        self.assertIsNotNone(response_get_small.context, "Context is None for GET before 'too small' POST.")
        self.assertIn('csrf_token', response_get_small.context, "CSRF token not in context for GET before 'too small' POST.")
        csrf_token_small = response_get_small.context['csrf_token']
        food_data_too_small['csrfmiddlewaretoken'] = csrf_token_small

        # 2. Post the form with the invalid data for 'too small'
        response_too_small = self.client.post(self.food_admin_add_url, food_data_too_small)

        # This assertion is where it's failing
        self.assertEqual(response_too_small.status_code, 200, "Expected 200 OK to re-render form on 'too small' POST.")

        # 3. Check for the error message
        self.assertContains(response_too_small, 'Ensure this value is greater than or equal to 0.1.', status_code=200)

        # Verify that no Food objects with these names were created
        self.assertFalse(Food.objects.filter(name='Poke Too Big').exists())
        self.assertFalse(Food.objects.filter(name='Poke Too Small').exists())

class FormTestCase(TestCase):
    # Test creating functionality via the form
    def test_create_food_via_form(self):
        food_data = {
            'category': 'Main',
            'name': 'Spot prawns',
            'price': 18.79,
            'checked': False,
        }

        response = self.client.post(
            '/m1/menu/',
            data=json.dumps(food_data), # convert food_date to json object
            content_type='application/json' 
        )

        # Assert if POST request is successful and verify if data is correct
        self.assertEqual(response.status_code, 201)
        spot_prawns = Food.objects.get(name='Spot prawns')
        self.assertEqual(spot_prawns.price, 18.79)
        self.assertEqual(spot_prawns.category, 'Main')
        self.assertEqual(spot_prawns.checked, False)

    # Test creating functionality fail by attempting with a too long name
    def test_create_food_long_name(self):
        long_name = {
            'category': 'Main',
            'name': 'Spot prawnsssssssssssssssssssssssssssssssssssss',
            'price': 18.79,
            'checked': False,
        }

        response = self.client.post(
            '/m1/menu/',
            data=json.dumps(long_name), # convert food_date to json object
            content_type='application/json' 
        )
        
        # Assert if POST request failed
        self.assertEqual(response.status_code, 400)

    # Test update functionality via price edit form 
    def test_edit_price(self):
        # 1. Create a valid data to update first
        food_data = {
            'category': 'Dessert',
            'name': 'Nanaimo bar',
            'price': 9.99,
            'checked': False,
        }

        self.client.post(
            '/m1/menu/',
            data=json.dumps(food_data), 
            content_type='application/json' 
        )

        # 2. Call a patch with new price to the created food's id endpoint
        new_price = {
            'price': 1.50,
        }

        nanaimo_bar = Food.objects.get(name='Nanaimo bar')
        response = self.client.patch(
            f'/m1/menu/{nanaimo_bar.id}/',
            data=json.dumps(new_price),
            content_type='application/json'
        )

        # 3. Verify if the patch is successful and the price is updated
        self.assertEqual(response.status_code, 200)
        updated_nanaimo_bar = Food.objects.get(name='Nanaimo bar')
        self.assertEqual(updated_nanaimo_bar.price, 1.50)

# Test bulk update functionality (applyDiscount)
class BulkUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some initial food items for testing
        cls.food1 = Food.objects.create(category='Main', name='Chicken pie', price=Decimal('10.00'), checked=False)
        cls.food2 = Food.objects.create(category='Drink', name='Bubble tea', price=Decimal('4.00'), checked=True)
        cls.food3 = Food.objects.create(category='Dessert', name='Mint jelly', price=Decimal('5.00'), checked=False)
        cls.food4 = Food.objects.create(category='Drink', name='Orange juice', price=Decimal('3.00'), checked=True)

    # Test valid rate and selected ids and verify with the successful status code
    def test_discount_apply_success(self):
        selected_food_ids = [self.food2.id, self.food4.id]

        payload = {
            'foodIds': selected_food_ids,
            'rate': 0.10
        }

        response = self.client.patch(
            '/m1/menu/discount/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    # Test unsuccessful attempt with invaild rate and verify Bad request 400 code
    def test_discount_apply_invaild_rate(self):
        selected_food_ids = [self.food2.id, self.food4.id]

        payload = {
            'foodIds': selected_food_ids,
            'rate': 1.5  # out of range (0.1 ~ 0.9)
        }

        response = self.client.patch(
            '/m1/menu/discount/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    # Test unsuccessful attempt with empty id list and verify Bad request 400 code
    def test_discount_apply_no_foods(self):
        payload = {
            'food_ids': [],  # empty id list to update
            'discount_rate': 0.15
        }

        response = self.client.patch(
            '/m1/menu/discount/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)