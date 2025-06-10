from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
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
        print(f"Attempting GET for 'too small' CSRF from: {self.food_admin_add_url}")
        response_get_small = self.client.get(self.food_admin_add_url)
        print(f"GET for 'too small' CSRF status code: {response_get_small.status_code}")
        if response_get_small.status_code != 200:
             print(f"GET for 'too small' CSRF redirected to: {response_get_small.url}") # <--- Check this if not 200
        self.assertEqual(response_get_small.status_code, 200, "Expected 200 OK for GET before 'too small' POST.")

        # Ensure context exists before accessing CSRF token
        self.assertIsNotNone(response_get_small.context, "Context is None for GET before 'too small' POST.")
        self.assertIn('csrf_token', response_get_small.context, "CSRF token not in context for GET before 'too small' POST.")
        csrf_token_small = response_get_small.context['csrf_token']
        print(f"CSRF Token obtained for 'too small': {csrf_token_small[:10]}...")
        food_data_too_small['csrfmiddlewaretoken'] = csrf_token_small
        print(f"Data for 'too small' POST: {food_data_too_small}")


        # 2. Post the form with the invalid data for 'too small'
        print(f"Attempting POST for 'too small' to: {self.food_admin_add_url}")
        response_too_small = self.client.post(self.food_admin_add_url, food_data_too_small)
        print(f"POST for 'too small' status code: {response_too_small.status_code}")
        if response_too_small.status_code == 302:
            print(f"POST for 'too small' REDIRECTED TO: {response_too_small.url}")
        else:
            # If not 302, but still fails other asserts, print content
            print(f"POST for 'too small' content (first 500 chars): {response_too_small.content.decode('utf-8')[:500]}...")

        # This assertion is where it's failing
        self.assertEqual(response_too_small.status_code, 200, "Expected 200 OK to re-render form on 'too small' POST.")

        # 3. Check for the error message
        self.assertContains(response_too_small, 'Ensure this value is greater than or equal to 0.1.', status_code=200)

        # Verify that no Food objects with these names were created
        self.assertFalse(Food.objects.filter(name='Poke Too Big').exists())
        self.assertFalse(Food.objects.filter(name='Poke Too Small').exists())

# Test creating functionality a food with the form
class FormTestCase(TestCase):
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

        # Assert if POST request is successful
        self.assertEqual(response.status_code, 201)
        spot_prawns = Food.objects.get(name='Spot prawns')
        self.assertEqual(spot_prawns.price, 18.79)
        self.assertEqual(spot_prawns.category, 'Main')
        self.assertEqual(spot_prawns.checked, False)

    # def test_out_of_range_price_via_form(self):
    #     response = self.client.post('/menu/', {
    #         'category': 'Drink',
    #         'name': 'Uranium juice',
    #         'price': 2000.00,0
    #         'checked': False,
    #     })
    #     try:
    #         Food.objects.get(name='Uranium juice')
    #         self.fail()
    #     except Food.DoesNotExist:
    #         pass
