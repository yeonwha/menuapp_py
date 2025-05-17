import yup from 'yup';

// Data Schema for a new Food
// Matches the one from the front-end App
const foodSchema = yup.object().shape({
    category: yup
        .string()
        .required(),
    name: yup
        .string()
        .trim()
        .min(2, 'Food nmae must be at least ${min} characters')
        .max(15, 'Food nmae cannot be more than ${max} characters')
        .matches(/^[A-Za-z0-9 ]+$/, 'Invalid name. Use upper or lower case letters, 0 to 9, or whitespace only.')
        .required('Food name is required.'),
    price: yup
        .number()
        .positive()
        .min(0.1, 'Food price must be at least ${min} dollars')
        .max(999.999, 'Food price cannot be higher than ${max} dollars')
        .required('Food price is required'),
});

export default foodSchema;