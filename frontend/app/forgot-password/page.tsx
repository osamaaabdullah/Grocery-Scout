"use client";

import Link from "next/link";
import { useState } from "react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("/api/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.detail || "Request failed");
      } else {
        setMessage("Password reset email sent! Check your inbox.");
      }
    } catch {
      setMessage("Network error");
    }

    setLoading(false);
  };

  return (
    <div className="h-[75svh] content-center w-9/10 mx-auto">
      <div className="h-85 max-w-md mx-auto mt-10 p-6 border rounded border-zinc-300 rounded-xl">
        <h1 className="text-center mx-auto text-2xl font-semibold mb-8">
          Forgot Password
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            name="email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="mt-5 btn-primary bg-[#D4F6FF] font-bold py-2 rounded rounded-xl hover:shadow-md"
          >
            {loading ? "Sending..." : "Send Reset Link"}
          </button>
        </form>

        {message && <p className="text-center text-sm mt-3">{message}</p>}

        <div className="text-center mt-4 hover:text-sky-500 underline">
          <Link href="/login">Back to Login</Link>
        </div>
      </div>
    </div>
  );
}
