"use client";

import { useParams } from "next/navigation";
import { useState } from "react";
import Link from "next/link";

export default function ResetPasswordPage() {
  const { token } = useParams();
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [message, setMessage] = useState("");
  const [redirecting, setRedirecting] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setMessage("");

    if (password !== confirm) {
      setMessage("Passwords do not match.");
      return;
    }

    try {
      const res = await fetch(
        `/api/reset-password/${token}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ password }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.detail || "Password reset failed.");
        return;
      }

      setMessage("Password has been reset!");
      setRedirecting(true);

      setTimeout(() => {
        window.location.href = "/login";
      }, 10000);
    } catch {
      setMessage("Network error.");
    }
  };

  return (
    <div className="h-[75svh] content-center">
      <div className="max-w-md mx-auto mt-10 p-6 border rounded border-zinc-300 rounded-xl">
        <h1 className="text-center text-2xl font-semibold mb-8">
          Reset Password
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <input
            type="password"
            placeholder="New password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input border border-zinc-100 shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
            required
          />

          <input
            type="password"
            placeholder="Confirm password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            className="input border border-zinc-100 shadow-2xs hover:shadow-md h-12 p-1 pl-5 rounded-full"
            required
          />

          <button
            type="submit"
            className="btn-primary bg-[#D4F6FF] font-bold py-2 rounded-xl hover:shadow-md"
          >
            Reset Password
          </button>
        </form>

        {message && (
          <p className="text-center mt-4 text-sm">{message}</p>
        )}

        {redirecting && (
          <p className="text-center text-sm mt-2">
            Redirecting to login in 10 seconds…
            <br />
            <Link href="/login" className="text-sky-500 underline">
              Click here if not redirected
            </Link>
          </p>
        )}
      </div>
    </div>
  );
}
