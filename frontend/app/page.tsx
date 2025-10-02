"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import SearchBar from "@/components/SearchBar";

interface Product {
  product_id: string;
  retailer: string;
  province: string;
  product_name: string;
  product_size: string;
  category: string;
  product_url: string;
  image_url: string;
  current_price: number;
  regular_price: number;
  price_unit: string;
  unit_type: string;
  multi_save_qty: number;
  multi_save_price: number;
  timestamp: string;
}

export default function Home() {
  const [vegetables, setVegetables] = useState<Product[]>([]);
  const [fruits, setFruits] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [vegRes, fruitRes] = await Promise.all([
          fetch("http://127.0.0.1:8000/province/prices/search?product_name=acorn"),
          fetch("http://127.0.0.1:8000/province/prices/search?product_name=apple"),
        ]);

        const vegData = await vegRes.json();
        const fruitData = await fruitRes.json();

        function pickUniqueRetailers(data: any[]): Product[] {
          if (!Array.isArray(data)) return [];
          const seen = new Set<string>();
          const unique: Product[] = [];
          const fallback: Product[] = [];

          for (const item of data) {
            if (!seen.has(item.retailer)) {
              seen.add(item.retailer);
              unique.push(item);
            } else {
              fallback.push(item);
            }
          }

          // If fewer than 6 unique retailers, fill with fallback
          return [...unique, ...fallback].slice(0, 6);
        }

        setVegetables(pickUniqueRetailers(vegData.main_results));
        setFruits(pickUniqueRetailers(fruitData.main_results));
      } catch (err) {
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);


  return (
    <div className="w-7/10 mx-auto">
      <main>
        <div className="mt-16 text-center">
          <h1 className="font-bold text-5xl">
            <span className="text-[#FCB53B]">Save money</span> on your{" "}
            <span className="text-[#97B067]">groceries.</span>
          </h1>
        </div>

        <div className="text-center mt-4">
          <h2 className="font-bold text-3xl">
            <span className="text-[#97B067]">Grocery</span>{" "}
            <span className="text-[#FCB53B]">Scout</span> helps you compare grocery
            prices across retailers in Canada for free.
          </h2>
        </div>

        <div className="m-2 text-center">
          <button className="m-2 p-3 min-w-[170px] font-bold rounded-full bg-[#D4F6FF]">
            Sign up for Free
          </button>
          <button className="m-2 p-3 min-w-[120px] font-bold rounded-full bg-[#D4F6FF]">
            Log In
          </button>
        </div>

        <div>
          <div className="mx-auto my-auto w-7/10 min-w-[500px] mt-10 mb-10 m-30 p-1 rounded-full content-center border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md h-10">
            <SearchBar/>
          </div>
        </div>

        {loading ? (
          <p className="text-center mt-10">Loading prices...</p>
        ) : (
          <>
            <section className="mt-10">
              <h3 className="font-semibold text-xl mb-4">Compare Vegetable Prices</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 ">
                {vegetables.map((item) => (
                  <div
                    key={`${item.retailer}-${item.product_id}`}
                    className="border border-zinc-100 rounded-lg p-2 text-center shadow hover:shadow-md h-140 flex flex-col bg-white"
                  >
                    <div className="h-1/2 flex items-center justify-center">
                      <img
                        src={item.image_url}
                        alt={item.product_name}
                        width={150}
                        height={150}
                        className="mx-auto object-contain"
                      />
                    </div>
                    <div className="h-40/100 flex flex-col justify-between">
                      <p className="min-h-12 font-semibold text-base">{item.product_name}</p>
                      <div>
                        <p className="text-sm text-base">{item.retailer}</p>
                        <p>{(item.province)}</p>
                        <p>{(item.category)}</p>
                      </div>
                      <div>
                        {item.price_unit === "¢" ? <p className="font-bold">${(item.current_price/100).toFixed(2)} {(item.unit_type)}</p> : <p className="font-bold">${(item.current_price).toFixed(2)} {(item.unit_type)}</p>}
                      </div>
                      <div><a href = {(item.product_url)} target="_blank" className="bg-[#D4F6FF] mt-2 mx-auto p-2 pl-4 pr-4 rounded-full">View Product</a></div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <section className="mt-10">
              <h3 className="font-semibold text-xl mb-4">Compare Fruits Prices</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 ">
                {fruits.map((item) => (
                  <div
                    key={`${item.retailer}-${item.product_id}`}
                    className="border border-zinc-100 rounded-lg p-2 text-center shadow hover:shadow-md h-140 flex flex-col bg-white"
                  >
                    <div className="h-1/2 flex items-center justify-center">
                      <Image
                        src={item.image_url}
                        alt={item.product_name}
                        width={120}
                        height={120}
                        className="mx-auto object-contain"
                      />
                    </div>
                    <div className="h-40/100 flex flex-col justify-between">
                      <p className="min-h-12 font-semibold text-base">{item.product_name}</p>
                      <div>
                        <p className="text-sm text-base">{item.retailer}</p>
                        <p>{(item.province)}</p>
                        <p>{(item.category)}</p>
                      </div>
                      <div>
                        {item.price_unit === "¢" ? <p className="font-bold">${(item.current_price/100).toFixed(2)} {(item.unit_type)}</p> : <p className="font-bold">${(item.current_price).toFixed(2)} {(item.unit_type)}</p>}
                      </div>
                      <div><a href = {(item.product_url)} target="_blank" className="bg-[#D4F6FF] mt-2 mx-auto p-2 pl-4 pr-4 rounded-full">View Product</a></div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}
