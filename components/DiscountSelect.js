import applyDiscount  from "./Functions/applyDiscount.js";
import PrimaryButton from "./Buttons/PrimaryButton"

 export default function DiscountSelect({ foodList, setFoodList }) {
    console.log("discount selet setFoodList:", setFoodList);
    // Apply discount form handler
    // send discount rate and selected food ids list to applyDiscount function for PATCH
    // Call applyDiscount function only if there's selected food item
    function handleDiscountSumbit(e){
        e.preventDefault();
        const form = e.target; 
        const formData = new FormData(form);
        const checkedFoods = foodList.filter((food) => food.checked === true);
        const checkedFoodIds = checkedFoods.map(food => food.id);

        if (checkedFoods.length > 0) {
            applyDiscount(formData, checkedFoodIds, setFoodList);
        } else {
            console.log("No food items selected for discount.");
        }
    }

    return(
    <>
    <div className="discount_select_form border-2 border-gray-200 rounded-lg p-6 max-w-4xl mx-2 items-center">
        <form id="discount_form" className="discount_select_form" onSubmit={handleDiscountSumbit}>
            <h2 className="text-xl font-bold text-center mb-6">Apply Discount</h2>
            <div className="grid grid-cols-2 gap-6">
                {/*Selected Food*/}
                <div className="mb-4">
                    <p className="text-lg font-medium text-gray-900">Selected Foods:</p>
                    {foodList.map((food) => <p key={food.id}>{food.checked ? food.name : ""}</p>)}
                </div>
            </div>
            {/* Discount rate % */}
            <div className="w-full max-w-96 mb-6">
                <label htmlFor="discount_rate" className="block mb-2 text-lg font-medium text-gray-900">Discount Rate</label>
                <input 
                    type="number" 
                    name="discount_rate" 
                    min="0.1" max="0.9" step="0.05" 
                    className="bg-white border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" 
                    placeholder="Discount rate" 
                    required/>
            </div>
            {/* Discount Apply button */}
            <div className="flex justify-end">
                <PrimaryButton type="submit">Apply</PrimaryButton>
            </div>
        </form>
    </div>
    </>
    )
 }