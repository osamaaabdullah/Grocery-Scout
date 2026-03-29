"use client";

import Image from "next/image";

interface Product {
  product_id: string;
  retailer: string;
  store_name?: string;
  city?: string;
  store_province?: string;
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
  is_stale?: boolean;
  price_source?: string;
}

interface ResultsClientProps {
  results: Product[];
  search: string;
  postalCode: string;
}

export default function ResultsClient({ results, search, postalCode }: ResultsClientProps) {
  return (
    <div className="p-4 3xl:w-8/10 mx-auto">
      <h2 className="text-xl font-semibold mb-4">
        {`Search Results for "${search}" near "${postalCode}"`}
      </h2>

      {results.length === 0 && <p>No results found.</p>}

      {/* ROW LAYOUT — below 500px */}
      <div className="flex flex-col gap-3 [@media(min-width:500px)]:hidden">
        {results.map((item, index) => (
          <div
            key={`${item.retailer}-${item.product_id}-${index}`}
            className="border border-zinc-100 rounded-xl p-3 shadow hover:shadow-md flex flex-row gap-4 bg-white items-center"
          >
            <div className="shrink-0">
              <Image
                src={item.image_url && !item.image_url.includes("?v=") ? item.image_url : "/no_image.webp"}
                alt={item.product_name.length > 40 ? item.product_name.slice(0, 40) + "…" : item.product_name}
                width={80}
                height={80}
                className="object-contain"
              />
            </div>
            <div className="flex flex-col flex-1 gap-1 min-w-0">
              <p className="font-semibold text-sm leading-tight">
                {item.product_name.length > 60 ? item.product_name.slice(0, 60) + "…" : item.product_name}
              </p>
              <p className="text-xs text-gray-500">{item.retailer} · {item.store_name ?? item.city}</p>
              <p className="text-xs text-gray-400">{item.category}</p>
            </div>
            <div className="shrink-0 flex flex-col items-end gap-2">
              <p className="font-bold text-base">
                ${item.current_price.toFixed(2)} <span className="text-xs font-normal">{(item.unit_type || "EA").toLowerCase()}</span>
              </p>
              <div className="flex flex-wrap gap-1 justify-end">
                {item.multi_save_qty && item.multi_save_price && (
                  <span className="text-white bg-[#FCB53B] text-xs p-0.5 rounded px-2 whitespace-nowrap">
                    {item.multi_save_qty} for ${item.multi_save_price}
                  </span>
                )}
                {item.timestamp && (
                  <span className="text-white bg-[#97B067] text-xs p-0.5 rounded px-2 whitespace-nowrap">
                    Updated: {new Date(item.timestamp).toLocaleDateString("en-CA", { day: "2-digit", month: "short" })}
                  </span>
                )}
              </div>
              <a
                href={item.product_url}
                target="_blank"
                className="bg-[#D4F6FF] text-xs p-1.5 px-3 rounded-full whitespace-nowrap"
              >
                View Product
              </a>
            </div>
          </div>
        ))}
      </div>

      {/* GRID LAYOUT — 500px and above */}
      <div className="hidden [@media(min-width:500px)]:grid [@media(max-width:800px)]:grid-cols-2 grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
        {results.map((item, index) => (
          <div
            key={`${item.retailer}-${item.product_id}-${index}`}
            className="border border-zinc-100 rounded-lg p-2 text-center shadow hover:shadow-md h-140 flex flex-col bg-white"
          >
            <div className="h-1/2 flex items-center justify-center">
              <Image
                src={item.image_url && !item.image_url.includes("?v=") ? item.image_url : "/no_image.webp"}
                alt={item.product_name.length > 40 ? item.product_name.slice(0, 40) + "…" : item.product_name}
                width={150}
                height={150}
                className="object-contain"
              />
            </div>
            <div className="h-40/100 flex flex-col justify-between">
              <p className="min-h-12 font-semibold text-base">
                {item.product_name.length > 50 ? item.product_name.slice(0, 50) + "…" : item.product_name}
              </p>
              <div>
                <p className="text-sm">{item.retailer}</p>
                <p className="text-sm">{item.store_name ?? item.city}</p>
                <p className="text-sm">{item.category}</p>
              </div>
              <div>
                <p className="font-bold">
                  ${item.current_price.toFixed(2)} {(item.unit_type || "EA").toLowerCase()}
                </p>
              </div>
              <div className="mb-3">
                {item.multi_save_qty && item.multi_save_price && (
                  <span className="text-white bg-[#FCB53B] border-none p-0.5 rounded px-2">
                    {item.multi_save_qty} for ${item.multi_save_price}
                  </span>
                )}
                {item.timestamp && (
                  <span className="text-white bg-[#97B067] border-none mx-2 p-0.5 rounded px-2 whitespace-nowrap">
                    Updated: {new Date(item.timestamp).toLocaleDateString("en-CA", { day: "2-digit", month: "short" })}
                  </span>
                )}
              </div>
              <div>
                <a
                  href={item.product_url}
                  target="_blank"
                  className="bg-[#D4F6FF] mt-2 mx-auto p-2 pl-4 pr-4 rounded-full"
                >
                  View Product
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}