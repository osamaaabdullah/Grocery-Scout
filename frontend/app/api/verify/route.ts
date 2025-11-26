import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const token = searchParams.get("token");

  if (!token) {
    return NextResponse.json({ error: "Missing token" }, { status: 400 });
  }

  const apiRes = await fetch(
    `${process.env.BACKEND_URL}/user/verify/${token}`,
    { cache: "no-store" }
  );

  const data = await apiRes.json();
  return NextResponse.json(data);
}
