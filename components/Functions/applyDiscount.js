import axios from "axios";

/**
 * PATCH calling function to apply discount rate for multiple food items
 * It sends a patch call including selected food ids list and discount rate as a request body
 * then render the updated food list to the main page
 * @param {*} formData
 * @param {*} selectedFoodIds
 * @param {*} setFoodList 
 */
export default async function applyDiscount( formData, selectedFoodIds, setFoodList ){
    try {
        console.log("applyDiscount setFoodList before patching:", setFoodList);
        let discountRate = parseFloat(formData.get("discount_rate"));
        console.log("selectedFoodIds:", selectedFoodIds);
        const request = {
            rate: discountRate,
            foodIds: selectedFoodIds
        }
        
        await axios.patch(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/discount/`, request);
        const updatedFoodList = await axios.get(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/`);
        const newFoodData = updatedFoodList.data

        setFoodList(prevFoodList => {
            const resetCheckedList = newFoodData.map(newFood => {
                return { ...newFood, checked: false };
            });
            console.log("applyDiscount: Setting state with this merged list:", resetCheckedList); 
            return resetCheckedList;
        });
    }
    catch (err) {
        console.log('Bad request. something wrong');
        console.error(err);
    } 
}