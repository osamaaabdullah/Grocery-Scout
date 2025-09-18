
async function getProducts() {
  const res = await fetch("http://127.0.0.1:8000/prices", {
    cache: "no-store",
  });
  const data = await res.json();
  return data.slice(0, 20); // take first 20
}

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <div className="p-6 w-7/10 mx-auto">
      <h1 className="text-2xl font-bold mb-4">Products (First 20)</h1>
      <ul className="space-y-4">
        {products.map((p: any) => (
          <li
            key={p.product_id}
            className="border p-4 rounded shadow flex items-center gap-4"
          >
            <img
              src={p.image_url}
              alt={p.product_name}
              className="w-20 h-20 object-contain"
            />
            <div>
              <h2 className="font-semibold">{p.product_name}</h2>
              <p className="text-sm text-gray-500">{p.category}</p>
              <p className="text-lg font-bold">${p.current_price}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

