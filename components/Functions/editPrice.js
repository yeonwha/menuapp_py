import axios from "axios";

/**
 * PATCH calling function to update a food's price
 * send new price data routing the selected food's id endpoint
 * then render the updated food list
 * @param {*} formData 
 * @param {*} selectedItem 
 * @param {*} setFoodList 
 */
export default async function editPrice( formData, selectedItem, setFoodList ){
    try {
        let updatedPrice = { "price": formData.get("food_price") };
        await axios.patch(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/${selectedItem.id}/`, updatedPrice);
        const updatedFoodList = await axios.get(`${process.env.NEXT_PUBLIC_HOST}/m1/menu/`);
        setFoodList(updatedFoodList.data);
    }
    catch (err) {
        console.log('Bad request. something wrong');
    } 
}