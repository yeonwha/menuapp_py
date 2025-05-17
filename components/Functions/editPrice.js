import axios from "axios";

export default async function editPrice({ formData, setFoodList }){
    try {
        let updatedFood = {
            ...arguments,
            "price": formData.get("food_price"),
        }
        await axios.patch('http://192.168.0.14:3004/m1/menu', updatedFood);
        const updatedFoodList = await axios.get('http://192.168.0.14:3004/m1/menu');
        setFoodList(updatedFoodList.data);
    }
    catch (err) {
        console.log('Bad request. something wrong');
    } 
}