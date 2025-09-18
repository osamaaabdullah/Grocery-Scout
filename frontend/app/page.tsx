import SearchBar from "@/components/SearchBar";
import Image from "next/image";

export default function Home() {
  return (
    <div className="w-7/10 mx-auto">
      <main>
        <h1>Save money on your groceries</h1>
        <p>Grocery Scout is a free price tracker of groceries in Canada.</p>
        <SearchBar/>
        <p>Compare Vegetable Prices</p>
        <p>Compare Fruit Prices</p>
      </main>
    </div>
  );
}
