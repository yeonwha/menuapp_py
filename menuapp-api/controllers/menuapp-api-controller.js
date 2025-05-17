import foodSchema from "../models/food-schema.js";

// Initial temporary data to send to the frontend (before database setup)
const foodList = [
    {id: 1, category: "Main", name: "Pasta", price: 21.99, checked: false },
    {id: 2, category: "Main", name: "Cheese burger", price: 11.49, checked: false},
    {id: 3, category: "Main", name: "Salad", price: 14.99, checked: false},
    {id: 4, category: "Dessert", name: "Chocolate icecream", price: 6.99, checked: false},
    {id: 5, category: "Dessert", name: "Vanilia cake", price: 8.49, checked: false},
    {id: 6, category: "Drink", name: "Zero sprite", price: 3.49, checked: false},
    {id: 7, category: "Drink", name: "Ginger ale", price: 3.49, checked: false},
    {id: 8, category: "Drink", name: "Cappucino", price: 2.99, checked: false},
  ];

// GET request handler
const getAllFoods = (req, res) => {
    try {
        res.status(200).send(foodList);
    } 
    catch (err) {
        res.status(400).send('Bad request.');
    }
};

var foodId = foodList.length;
// POST request handler
const addNewFood = async (req, res) => {
    try {
        let food = await foodSchema.validate(req.body);
        foodId++;
        const newFood = {
            id: foodId, 
            category: food.category, 
            name: food.name, 
            price: food.price, 
            checked: false
        };
        foodList.push(newFood);
        res.status(201).send(newFood);
    } 
    catch (err) {
        res.status(400).send('Bad Request.  \
            The food in the body of the request is either missing or malformed.');
    };
};

// PATCH (will be revised)
const editPrice = async (req, res) => {
    try {
        let food = await foodSchema.validate(req.body);
        console.log(food);
        for (f in foodList) {
            if (f.id === food.id) {
                f.price = food.price;
            }
        }
        res.status(204).send(food);
    }
    catch (err){
        res.status(400).send('Bad request');
    }
}

export { getAllFoods, addNewFood , editPrice };