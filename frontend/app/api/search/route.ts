import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);

  const query = searchParams.get("search") || "";
  const postal = searchParams.get("postal_code");
  const distance = searchParams.get("set_distance") || "5";

  const isNearby = postal && postal !== "null" && postal !== "";

  let apiURL = "";

  if (isNearby) {
    apiURL = `${process.env.BACKEND_URL}/province/prices/search-nearby?product_name=${encodeURIComponent(
      query
    )}&postal_code=${encodeURIComponent(
      postal
    )}&set_distance=${encodeURIComponent(distance)}`;
  } else {
    apiURL = `${process.env.BACKEND_URL}/province/prices/search?product_name=${encodeURIComponent(
      query
    )}`;
  }

  const apiRes = await fetch(apiURL, { cache: "no-store" });
  const data = await apiRes.json();

  return NextResponse.json(data);
}
