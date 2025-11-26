"use client";

import Image from "next/image";
import Link from "next/link";
import SearchBar from "./SearchBar";
import { Menu, X } from "lucide-react";
import { useState, useEffect } from "react";
import Postalbar from "./Postalbar";
import { useSearchParams } from "next/navigation";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [postalCode, setPostalCode] = useState("");
  const [distance, setDistance] = useState("5");
  const [loggedIn, setLoggedIn] = useState(false);

  const searchParams = useSearchParams();
  const currentPostal = searchParams.get("postal_code") ?? "";

  useEffect(() => {
    const t = localStorage.getItem("access_token");
    if (t) setLoggedIn(true);

    if (currentPostal) {
      setPostalCode(currentPostal);
    }
  }, [currentPostal]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    window.location.href = "/";
  };

  const withPostal = (url: string) =>
    postalCode ? `${url}?postal_code=${postalCode}` : url;

  return (
    <nav className="relative flex justify-between m-2">
      <div className="flex xl:w-1/2">
        <div className="flex p-3 min-w-[60px]">
          <Link href={withPostal("/")}>
            <Image src="/logo.svg" alt="Grocery Scout Logo" width={40} height={40} />
          </Link>
        </div>

        <div className="flex-auto p-1 rounded-full content-center border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md w-1/2 h-10 my-auto max-w-[500px]">
          <SearchBar postalCode={postalCode} distance={distance} />
        </div>

        <div className="[@media(max-width:480px)]:hidden my-auto ml-2">
          <Postalbar
            postalCode={postalCode}
            setPostalCode={setPostalCode}
            distance={distance}
            setDistance={setDistance}
          />
        </div>
      </div>

      <div className="m-2 my-auto">
        <button onClick={() => setMenuOpen(!menuOpen)} className="xl:hidden pt-2">
          {menuOpen ? <X size={30} /> : <Menu size={30} />}
        </button>
      </div>

      {/* MOBILE MENU */}
      {menuOpen && (
        <div className="absolute top-full right-2 mt-2 bg-white border border-zinc-200 rounded-lg shadow-md w-48 p-2 xl:hidden z-50">
          <ul className="flex flex-col text-sm">
            <li className="p-2 hover:bg-zinc-100 rounded-md">
              <Link href={withPostal("/")}>Home</Link>
            </li>

            <li className="p-2 hover:bg-zinc-100 rounded-md">
              <Link href={withPostal("/products/vegetable/page/1")}>Vegetables</Link>
            </li>

            <li className="p-2 hover:bg-zinc-100 rounded-md">
              <Link href={withPostal("/products/fruit/page/1")}>Fruits</Link>
            </li>

            {!loggedIn && (
              <li className="p-2 hover:bg-zinc-100 rounded-md">
                <Link href={withPostal("/signup")}>Sign up</Link>
              </li>
            )}

            {loggedIn ? (
              <li
                onClick={handleLogout}
                className="p-2 hover:bg-zinc-100 rounded-md cursor-pointer"
              >
                Logout
              </li>
            ) : (
              <li className="p-2 hover:bg-zinc-100 rounded-md">
                <Link href={withPostal("/login")}>Sign in</Link>
              </li>
            )}
          </ul>
        </div>
      )}

      {/* DESKTOP MENU */}
      <ul className="hidden xl:flex justify-end gap-4 content-center my-auto">
        <li className="hover:bg-zinc-200 p-3 rounded-md">
          <Link href={withPostal("/")}>Home</Link>
        </li>

        <li className="hover:bg-zinc-200 p-3 rounded-md">
          <Link href={withPostal("/products/vegetable/page/1")}>
            Compare Vegetable Prices
          </Link>
        </li>

        <li className="hidden 3xl:block hover:bg-zinc-200 p-3 rounded-md">
          <Link href={withPostal("/products/fruit/page/1")}>
            Compare Fruit Prices
          </Link>
        </li>

        {!loggedIn && (
          <li className="hover:bg-zinc-200 p-3 rounded-md bg-[#D4F6FF] font-bold">
            <Link href={withPostal("/signup")}>Sign up</Link>
          </li>
        )}

        {loggedIn ? (
          <li
            onClick={handleLogout}
            className="hover:bg-zinc-200 p-3 rounded-md bg-[#D4F6FF] font-bold cursor-pointer"
          >
            Logout
          </li>
        ) : (
          <li className="hover:bg-zinc-200 p-3 rounded-md bg-[#D4F6FF] font-bold">
            <Link href={withPostal("/login")}>Sign in</Link>
          </li>
        )}
      </ul>
    </nav>
  );
}
