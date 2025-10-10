import Pagination from "@/components/Pagination";

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

async function getProducts(type: string, page: number) {
  const res = await fetch(
    `http://127.0.0.1:8000/province/prices?category=${type}&page=${page}&sort_by=price&sort_order=asc`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch products");
  }

  const data = await res.json();
  return data;
}

export default async function ProductsPage({
  params,
}: {
  params: { type: string; page: string };
}) {
  const currentPage = parseInt(params.page, 10) || 1;
  const data = await getProducts(params.type, currentPage);
  const products: Product[] = data.results;
  const totalPages = data.max_page;

  return (
    <div className="p-6 2xl:w-7/10 mx-auto">
      <h1 className="text-2xl font-bold mb-4">
        {params.type.charAt(0).toUpperCase() + params.type.slice(1)}
      </h1>

      <div className="grid [@media(max-width:800px)]:grid-cols-2 grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
        {products.map((item) => (
          <div
            key={`${item.retailer}-${item.product_id}=${item.province}`}
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

            <div className="flex flex-col justify-between">
              <p className="min-h-12 font-semibold text-base">{item.product_name}</p>
              <p className="text-sm">{item.retailer}</p>
              <p>{item.category}</p>

              <p className="font-bold">
                {item.price_unit === "¢"
                  ? `$${(item.current_price / 100).toFixed(2)} ${item.unit_type}`
                  : `$${item.current_price.toFixed(2)} ${item.unit_type}`}
              </p>

              <a
                href={item.product_url}
                target="_blank"
                className="bg-[#D4F6FF] mt-10 mx-auto p-2 pl-4 pr-4 rounded-full"
              >
                View Product
              </a>
            </div>
          </div>
        ))}
      </div>

      <div className="w-9/10 mx-auto">
        <Pagination
          page={currentPage}
          totalPages={totalPages}
          type= {params.type}
        />
      </div>
    </div>
  );
}
