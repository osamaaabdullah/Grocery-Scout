"use client";
import Link from "next/link";
import { useState } from "react";

export default function SignupPage() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    name: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.detail || "Signup failed");
      } else {
        setMessage("Verification email sent! Check your inbox.");
      }
    } catch (err) {
      setMessage("Network error. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="h-[75svh] content-center w-9/10 mx-auto">
      <div className="h-120 max-w-md mx-auto mt-10 p-6 border rounded border-zinc-300 rounded-xl">
        <h1 className="text-center mx-auto text-2xl font-semibold mb-8">Create Account</h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-8 ">
          <input
            name="name"
            placeholder="Name"
            value={form.name}
            onChange={handleChange}
            required
            className="input border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
          />
          <input
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
            className="input border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
            className="input border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
          />
          <button
            type="submit"
            disabled={loading}
            className="mt-5 btn-primary bg-[#D4F6FF] font-bold py-2 rounded rounded-xl hover:shadow-md"
          >
            {loading ? "Signing up..." : "Sign Up"}
          </button>
        </form>
        <div className="text-center mt-4 hover:text-sky-500 hover:underline">
            <Link href="/login"> Already have an account?</Link>
        </div>
        {message && <p className="mt-4 text-center">{message}</p>}
      </div>
    </div>
  );
}
