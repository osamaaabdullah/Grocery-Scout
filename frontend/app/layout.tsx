import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import SearchBar from "@/components/SearchBar";
import Image from "next/image";

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
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={inter.className}
      >
      <nav className = 'flex m-2 mx-auto w-7/10'>
        
        <div className="flex p-3 min-w-[60px]">
          <Link href= "/">
            <Image src="/logo.svg" alt="Grocery Scout Logo" width= "40" height="40"/>
          </Link>
        </div>
        <div className="flex-auto p-1 rounded-full content-center border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md w-1/100 h-10 my-auto min-w-[500px]">
          <SearchBar />
        </div>

        <div className="flex-auto min-w-[670px] my-auto">
          <ul className = 'flex justify-end gap-4 content-center'>
          
          <Link href="/"><li className="hover:bg-zinc-200 p-3 rounded-md">Home</li></Link>
          <Link href="/products"><li className="hover:bg-zinc-200 p-3 rounded-md">Compare Vegetable Prices</li></Link>
          <Link href="/"><li className="hover:bg-zinc-200 p-3 rounded-md">Compare Vegetable Prices</li></Link>
          <Link href="/"><li className="hover:bg-zinc-200 p-3 rounded-md">Sign up</li></Link>
          <Link href="/"><li className="hover:bg-zinc-200 p-3 rounded-md">Sign in</li></Link>
        </ul></div>
        

      </nav>
      <hr className="border-zinc-300"/>
        {children}
      <hr className="border-zinc-300 mt-20 mb-20"/>
      </body>
      
    </html>
  );
}
