"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

type Product = {
    product_id: string
    retailer: string
    product_name: string
    product_size: string | null
    category: string
    product_url: string 
    image_url: string
    store_id: number
    current_price: number
    regular_price: number
    timestamp: string
}


export default function ResultsPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get("search") || "";
  const [results, setResults] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query) return;
    setLoading(true);

    fetch(`http://localhost:8000/prices/search?product_name=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => {
        setResults(data);        
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [query]);

  return (
    <div>
      <h1>
        Results for "{query}"
      </h1>

      {loading && <p>Loading...</p>}

      {results.length === 0 && !loading && <p>No results found.</p>}

      <ul>
        {results.map((item) => (
          <li key={`${item.retailer}-${item.product_id}`}>
            <img src={item.image_url} alt={item.product_name} />
            <div>
              <a href={item.product_url} target="_blank" rel="noopener noreferrer">
                {item.product_name}
              </a>
              <p >{item.product_size}</p>
              {item.current_price !== item.regular_price ? 
                    <span>
                        <span>{item.regular_price}</span>
                        <span>{item.current_price}</span>
                    </span>:
                    <span>{item.current_price}</span>
                }
              <p>{item.retailer}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
