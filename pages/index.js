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
      await axios.get(`${process.env.NEXT_PUBLIC_HOST}/m1/menu`);
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
  console.log("Home component: Current foodList state is:", foodList);
  console.log("Home Component: setFoodLis function is:", setFoodList)

  return (
    <>
      <div className="min-h-screen flex flex-col">
        <div className="container m-6"><Header /></div>
        <main className="inline-block justify-center container mx-8 px-4">
          <div className="flex justify-center">
          <Form setFoodList={setFoodList}/>
          </div>
          <div className="container my-4 flex justify-center">
          <List foodList={foodList} setFoodList={setFoodList}/>
          </div>
          <div className="flex justify-center">
          <DiscountSelect foodList={foodList} setFoodList={setFoodList}/>
          </div>
        </main>
        <Footer />
      </div>
    </>
  );
}
