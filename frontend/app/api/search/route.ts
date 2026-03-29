import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);

  const query = searchParams.get("search") || "";
  const postal = searchParams.get("postal_code") || `${process.env.DEFAULT_POSTAL_CODE}`;
  const distance = searchParams.get("set_distance") || "5";
  const category = searchParams.get("category") || "";
  const page = searchParams.get("page") || "1";
  const retailer = searchParams.get("retailer") || "";
  const sortBy = searchParams.get("sort_by") || "relevance";

  const isNearby = postal && postal !== "null" && postal !== "";

  let apiURL = "";


  apiURL = `${process.env.BACKEND_URL}/prices/search?product_name=${encodeURIComponent(query)}&postal_code=${encodeURIComponent(postal)}&set_distance=${encodeURIComponent(distance)}&category=${encodeURIComponent(category)}&retailer=${encodeURIComponent(retailer)}&sort_by=${encodeURIComponent(sortBy)}&page=${page}`;


  const apiRes = await fetch(apiURL, { cache: "no-store" });
  const data = await apiRes.json();

  return NextResponse.json(data);
}
