import Pagination from "@/components/Pagination";
import Image from "next/image";

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

async function getProducts(type: string, page: number, postalCode: string | null) {
  const baseUrl =
    `${process.env.BACKEND_URL}/province/prices?page=${page}&sort_by=price&sort_order=asc&multi_offer=true`;

  const url = postalCode
    ? `${baseUrl}&postal_code=${postalCode}`
    : baseUrl;

  const res = await fetch(url, { cache: "no-store" });

  if (!res.ok) throw new Error("Failed to fetch products");

  return res.json();
}

export default async function ProductsPage(props: {
  params: Promise<{ type: string; page: string }>;
  searchParams: Promise<{ postal_code?: string }>;
}) {

  const { type, page } = await props.params;
  const sp = await props.searchParams;

  const postalCode = sp.postal_code ?? null;

  const currentPage = parseInt(page, 10) || 1;

  const data = await getProducts(type, currentPage, postalCode);

  const products: Product[] = data.results;
  const totalPages = data.max_page;

  return (
    <div className="p-6 2xl:w-8/10 mx-auto">
      <h1 className="text-2xl font-bold mb-4">
        {type.charAt(0).toUpperCase() + type.slice(1)}
      </h1>

      <div className="grid [@media(max-width:800px)]:grid-cols-2 grid-cols-3 xl:grid-cols-4 3xl:grid-cols-5 gap-4">
        {products.map((item) => (
          <div
            key={`${item.retailer}-${item.product_id}-${item.province}`}
            className="border border-zinc-100 rounded-lg p-2 text-center shadow hover:shadow-md h-140 flex flex-col bg-white"
          >
            <div className="h-1/2 flex items-center justify-center">
              <Image
                src={item.image_url && !item.image_url.includes("?v=")? item.image_url: "/no_image.webp"}
                alt={item.product_name.length > 40 ? item.product_name.slice(0, 40) + "…": item.product_name}
                width={150}
                height={150}
                className="mx-auto object-contain"
              />
            </div>

            <div className="flex flex-col justify-between">
              <p className="min-h-12 font-semibold text-base">{item.product_name.length > 50 ? item.product_name.slice(0, 50) + "…": item.product_name}</p>
              <p className="text-sm">{item.retailer}</p>
              <p className="text-sm">{item.province}</p>
              <p>{item.category}</p>

              <p className="font-bold">
                {item.price_unit === "¢"
                  ? `$${(item.current_price / 100).toFixed(2)} ${(item.unit_type || "EA").toLowerCase()}`
                  : `$${item.current_price.toFixed(2)} ${(item.unit_type || "EA").toLowerCase()}`}
              </p>

              <div className="mt-3">
                {item.multi_save_qty && item.multi_save_price && (
                  <span className="text-white bg-[#FCB53B] p-0.5 rounded px-2">
                    {item.multi_save_qty} for ${item.multi_save_price}
                  </span>
                )}
                <span className="text-white bg-[#97B067] mx-2 p-0.5 rounded px-2">
                  Updated:{" "}
                  {new Date(item.timestamp).toLocaleDateString("en-CA", {
                    day: "2-digit",
                    month: "short",
                  })}
                </span>
              </div>

              <a
                href={item.product_url}
                target="_blank"
                className="bg-[#D4F6FF] mt-10 mx-auto p-2 px-4 rounded-full"
              >
                View Product
              </a>
            </div>
          </div>
        ))}
      </div>

      <div className="w-9/10 mx-auto">
        <Pagination page={currentPage} totalPages={totalPages} type={type} />
      </div>
    </div>
  );
}
