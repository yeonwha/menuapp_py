import Header from "@/components/Header";
import Form from "@/components/Form";
import List from "@/components/List";
import Footer from "@/components/Footer";
import DiscountSelect from "@/components/DiscountSelect";
import { useState } from "react"
import axios from 'axios';

// Static data generation pre-rendering at build time
export async function getStaticProps(){
  let jsonData;

  try {
    const { data } = 
      await axios.get('http://localhost:3004/m1/menu');
      jsonData = data;
  } 
  catch (err) {
    console.log('API error: ' + err);
  }

  return {
    props: { jsonData }
  }
}

export default function Home({ jsonData }) {
  const [foodList, setFoodList] = useState(jsonData);   // Menu list hook

  return (
    <>
      <div className="min-h-screen flex flex-col">
        <div className="container m-6"><Header /></div>
        <main className="inline-block justify-center container mx-8 px-4">
          <div className="flex justify-center">
          <Form key={() => (foodList.length + 1)} setFoodList={setFoodList}/>
          </div>
          <div className="container my-4 flex justify-center">
          <List key={() => (foodList.length + 1)} foodList={foodList} setFoodList={setFoodList}/>
          </div>
          <div className="flex justify-center">
          <DiscountSelect ket={() => (foodList.length + 1)} foodList={foodList}/>
          </div>
        </main>
        <Footer />
      </div>
    </>
  );
}
