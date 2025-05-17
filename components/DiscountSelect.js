 import PrimaryButton from "./Buttons/PrimaryButton"

 export default function DiscountSelect({foodList}) {
    return(
    <>
    <div className="food_add_form border-2 border-gray-200 rounded-lg p-6 max-w-4xl mx-2 items-center">
        <h2 className="text-xl font-bold text-center mb-6">Discount Apply</h2>
        <div className="grid grid-cols-2 gap-6">
            {/*Selected Food*/}
            <div className="mb-4">
                <p className="text-lg font-medium text-gray-900">Selected Foods:</p>
                {foodList.map((food) => <p key={food.id}>{food.checked ? food.name : ""}</p>)}
            </div>
        </div>
         {/* Discount % */}
         <div className="w-full max-w-96 mb-6">
            <label htmlFor="discount_rate" className="block mb-2 text-lg font-medium text-gray-900">Discount Rate</label>
            <input type="float" id="discount_rate" className="bg-white border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="Discount rate" />
        </div>
        {/* Discount Apply button */}
        <div className="flex justify-end">
            <PrimaryButton>Apply</PrimaryButton>
        </div>
    </div>
    </>
    )
 }