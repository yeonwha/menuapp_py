import axios from "axios";

/**
 * DELETE calling function to delete a food item
 * send a delete request with the selected food's id
 * then re-render the main page
 * @param {*} selectedFood 
 * @param {*} setFoodList 
 */
export default async function deleteFood(selectedFood, setFoodList){
    try {
        await axios.delete(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/${selectedFood.id}/`);
        const updatedFoodList = await axios.get(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/`);
        setFoodList(updatedFoodList.data);
    }
    catch (err) {
        console.log('Bad request. Check the error message.');
        console.error(err);
    }
}