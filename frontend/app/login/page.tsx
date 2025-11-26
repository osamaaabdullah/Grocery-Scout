"use client";

import Link from "next/link";
import { useState } from "react";

export default function LoginPage() {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    const body = new URLSearchParams();
    body.append("username", form.email);
    body.append("password", form.password);

    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body,
      });

      const data = await res.json();

      if (!res.ok) {
        if (Array.isArray(data.detail)) {
          setMessage(data.detail[0].msg);
        } else {
          setMessage(data.detail || "Login failed");
        }
        setLoading(false);
        return;
      }

      localStorage.setItem("access_token", data.access_token);
      setMessage("Login successful!");

      setTimeout(() => {
        window.location.href = "/";
      }, 800);
    } catch (err) {
      setMessage("Network error");
      setLoading(false);
    }

    setLoading(false);
  };

  return (
    <div className="h-[75svh] content-center w-9/10 mx-auto">
      <div className="h-110 max-w-md mx-auto mt-10 p-6 border rounded border-zinc-300 rounded-xl">
        <h1 className="text-center mx-auto text-2xl font-semibold mb-8">Login</h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-8">
          <input
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            className="input border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            className="input border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="mt-5 btn-primary bg-[#D4F6FF] font-bold py-2 rounded rounded-xl hover:shadow-md"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
        {message && <p className="text-center text-sm mt-3">{message}</p>}
        <div className="text-center mt-4 hover:text-sky-500 hover:underline">
          <Link href="/forgot-password">Forgot your password?</Link>
        </div>
        <div className="text-center mt-2 hover:text-sky-500 hover:underline">
          <Link href="/signup">Create an account</Link>
        </div>
      </div>
    </div>
  );
}
