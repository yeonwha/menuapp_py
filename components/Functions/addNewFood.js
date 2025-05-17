import axios from "axios";

/**
 * POST function to create a new food to the list.
 * It posts to add a new food to the food list, 
 * then get the list to update the app page.
 * @param formData: The data from the form
 * @param setFoodList: Foodlist hook to update after adding a new food
 */
export default async function addNewFood( formData , setFoodList ) {
    try {
        let newFood = {
            "category": formData.get("category"),
            "name": formData.get("food_name"), 
            "price": formData.get("food_price"),
        }
        await axios.post('http://192.168.0.14:3004/m1/menu', newFood);
        const updatedFoodList = await axios.get('http://192.168.0.14:3004/m1/menu');
        setFoodList(updatedFoodList.data);
    }
    catch (err) {
        console.log('Bad request. something wrong');
    }    
}