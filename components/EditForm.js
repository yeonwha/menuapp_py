import PrimaryButton from "./Buttons/PrimaryButton"
import editPrice from "./Functions/editPrice";

export default function EditForm({ selectedItem, handleClose, setFoodList }) {
    function handleApplySubmit(e){
        e.preventDefault();
        const form = e.target; 
        const formData = new FormData(form);
        editPrice(formData, setFoodList);
        handleClose();
    }
   return(
        <>
            <div className="edit_price_form">                
                <form id="form" className="edit_price_form" onSubmit={handleApplySubmit}>
                    <h2><b>{selectedItem.name}</b>&apos;s</h2>
                    <div className="mb-4">
                        <label htmlFor="food_price" className="block text-gray-700 text-sm font-bold mb-2">New Price:</label>
                        <input
                            type="text"
                            id="food_price"
                            name="food_price"
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            placeholder={selectedItem.price}
                            required
                        />
                    </div>
                    <div className="flex items-center justify-between">
                        <PrimaryButton type="submit">
                            Apply
                        </PrimaryButton>
                        <button className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800" onClick={()=> handleClose()}>
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </>
    )
}