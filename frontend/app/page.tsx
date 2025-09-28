import SearchBar from "@/components/SearchBar";
import Image from "next/image";

export default function Home() {
  return (
    <div className="w-7/10 mx-auto">
      <main className="text-center">
        <div className="mt-16">
          <div className="m-4 mx-auto pl-2"><h1 className="font-bold text-5xl"><span className="text-[#FCB53B]">Save money</span> on your <span className="text-[#97B067]">groceries.</span></h1></div>
        </div>
        
        <div>
          <h2 className="font-bold text-3xl pl-2"><span className="text-[#97B067]">Grocery</span> <span className="text-[#FCB53B]">Scout</span> helps you compare grocery prices across retailers in Canada for free.</h2>
        </div>
        <div className="m-2">
          <button className="ml-0 m-2 p-3 min-w-[170px] font-bold rounded-full bg-[#D4F6FF]">Sign up for Free</button>
          <button className=" m-2 p-3 min-w-[120px] font-bold rounded-full bg-[#D4F6FF]">Log In</button>
        </div>
        <div className="mt-10 mb-10 m-30 p-1 rounded-full content-center border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md  h-10 my-auto "><SearchBar/></div>
        
        <div>
          <p className="font-semibold">Compare Vegetable Prices</p>
          <p className="font-semibold">Compare Fruit Prices</p>
        </div>
        
      </main>
    </div>
  );
}
