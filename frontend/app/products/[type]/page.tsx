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

async function getProducts(type: string) {
  const res = await fetch(
    `http://127.0.0.1:8000/province/prices?category=${type}`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch products");
  }

  const data = await res.json();
  return data.slice(0, 20); // take first 20
}

export default async function ProductsPage({
  params,
}: {
  params: { type: string };
}) {
  const products: Product[] = await getProducts(params.type);

  return (
    <div className="p-6 w-7/10 mx-auto">
      <h1 className="text-2xl font-bold mb-4">
        {params.type.charAt(0).toUpperCase() + params.type.slice(1)}
      </h1>
      <div className="grid grid-cols-5 gap-4 ">
        {products.map((item) => (
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
                {item.price_unit && item.price_unit.trim().startsWith("¢") ? <p className="font-bold">${(item.current_price/100).toFixed(2)} {(item.unit_type)}</p> : <p className="font-bold">${(item.current_price).toFixed(2)} {(item.unit_type)}</p>}
              </div>
              <div><a href = {(item.product_url)} target="_blank" className="bg-[#D4F6FF] mt-2 mx-auto p-2 pl-4 pr-4 rounded-full">View Product</a></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
