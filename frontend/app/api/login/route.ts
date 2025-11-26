import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.text(); 

    const res = await fetch(`${process.env.BACKEND_URL}/auth/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body, 
    });

    const data = await res.json();

    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json(
      { detail: "Server error" },
      { status: 500 }
    );
  }
}
