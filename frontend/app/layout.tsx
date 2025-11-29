import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Postalbar from "@/components/Postalbar";
import { Suspense } from "react";
import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "Grocery Scout",
  description: "Compare grocery prices across retailers in Canada",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Suspense fallback={null}>
          <div className="sm:w-9/10 mx-auto 3xl:w-8/10">
            <Navbar />
          </div>

          <div className="[@media(min-width:480px)]:hidden w-95/100 m-1 mx-auto">
            <Postalbar />
          </div>
        </Suspense>

        <hr className="border-zinc-300" />

        {children}
        <Analytics />
        <SpeedInsights />

        <hr className="border-zinc-300 mt-20 mb-20" />
      </body>
    </html>
  );
}
