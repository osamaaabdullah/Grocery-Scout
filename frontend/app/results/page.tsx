"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

interface Product {
  product_id: string;
  retailer: string;
  province: string;
  product_name: string;
  product_size?: string;
  category?: string;
  product_url?: string;
  image_url?: string;
  current_price: number;
  regular_price?: number;
  price_unit?: string;
  unit_type?: string;
  multi_save_qty?: number;
  multi_save_price?: number;
  timestamp: string;
}

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const search = searchParams.get("search") || "";
  const postalCode = searchParams.get("postal_code") || "";
  const distance = searchParams.get("set_distance") || "5";
  const [results, setResults] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

useEffect(() => {
  if (!search || !postalCode) return;

  const fetchResults = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/province/prices/search-nearby?product_name=${encodeURIComponent(search)}&postal_code=${encodeURIComponent(postalCode)}&set_distance=${encodeURIComponent(distance)}`
      );

      if (!res.ok) {
        throw new Error(`API error: ${res.status}`);
      }

      const data = await res.json();

      const main = Array.isArray(data.main_results) ? data.main_results : [];
      const related = Array.isArray(data.related_results) ? data.related_results : [];

      setResults([...main, ...related]);
    } catch (err) {
      console.error("Error fetching results:", err);
      setResults([]); 
    } finally {
      setLoading(false);
    }
  };

  fetchResults();
}, [search, postalCode]);

  return (
    <div className="p-4 2xl:w-7/10 mx-auto">
      <h2 className="text-xl font-semibold mb-4">
        Search Results for "{search}" near "{postalCode}"
      </h2>

      {loading && <p>Loading...</p>}

      <div className="grid [@media(max-width:800px)]:grid-cols-2 grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
        {results.map((item) => (
          <div key={`${item.retailer}-${item.product_id}`} className="border border-zinc-100 rounded-lg p-2 text-center shadow hover:shadow-md h-140 flex flex-col bg-white">
            <div className="h-1/2 flex items-center justify-center">
              <img
                src={item.image_url || "/placeholder.png"}
                alt={item.product_name}
                width={150}
                height={150}
                className="object-contain"
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
    </div>
  );
}
