import axios from "axios";

/**
 * PATCH calling function to apply discount rate for multiple food items
 * It sends a patch call including selected food ids list and discount rate as a request body
 * then render the updated food list on the main page
 * @param {*} formData
 * @param {*} selectedFoodIds
 * @param {*} setFoodList 
 */
export default async function applyDiscount( formData, selectedFoodIds, setFoodList ){
    try {
        let discountRate = parseFloat(formData.get("discount_rate"));

        const request = {
            rate: discountRate,
            foodIds: selectedFoodIds
        }
        
        await axios.patch(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/discount/`, request);
        const updatedFoodList = await axios.get(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/`);
        const newFoodData = updatedFoodList.data

        // Update foodList to reset the checked attribute to unchecked 
        setFoodList(prevFoodList => {
            const resetCheckedList = newFoodData.map(newFood => {
                return { ...newFood, checked: false };
            });
            return resetCheckedList;
        });
    }
    catch (err) {
        console.log('Bad request. Check the error message.');
        console.error(err);
    } 
}