"use client"

import Image from "next/image";
import Link from "next/link";
import SearchBar from "./SearchBar";
import {Menu, X} from "lucide-react";
import { useState } from "react";
import Postalbar from "./Postalbar";

export default function Navbar(){

    const [menuOpen, setMenuOpen] = useState(false);

    const [postalCode, setPostalCode] = useState("");
    const [distance, setDistance] = useState("5");

    return(
      <nav className = 'relative flex justify-between m-2 '>
        <div className="flex xl:w-1/2">
            <div className="flex p-3 min-w-[60px]">
              <Link href= "/">
                <Image src="/logo.svg" alt="Grocery Scout Logo" width= "40" height="40"/>
              </Link>
            </div>
            <div className="flex-auto p-1 rounded-full content-center border border-zinc-100 inset-shadow-2xs shadow-2xs hover:shadow-md w-1/2 h-10 my-auto max-w-[500px]">
              <SearchBar postalCode = {postalCode} distance = {distance} />
            </div>
            <div className="[@media(max-width:480px)]:hidden my-auto ml-2">
              <Postalbar postalCode = {postalCode} setPostalCode = {setPostalCode} distance = {distance} setDistance = {setDistance}/>
            </div>
        </div>

        <div className="m-2 my-auto">
          <button onClick={()=> setMenuOpen(!menuOpen)} className="xl:hidden pt-2">
            {menuOpen ? <X size={30} /> : <Menu size={30} />}
          </button>
        </div>

        {menuOpen && (
        <div className="absolute top-full right-2 mt-2 bg-white border border-zinc-200 rounded-lg shadow-md w-48 p-2 xl:hidden z-50">
          <ul className="flex flex-col text-sm">
            <Link href="/"><li className="p-2 hover:bg-zinc-100 rounded-md">Home</li></Link>
            <Link href="/products/vegetable/page/1"><li className="p-2 hover:bg-zinc-100 rounded-md">Vegetables</li></Link>
            <Link href="/products/fruit/page/1"><li className="p-2 hover:bg-zinc-100 rounded-md">Fruits</li></Link>
            <Link href="/"><li className="p-2 hover:bg-zinc-100 rounded-md hidden">Sign up</li></Link>
            <Link href="/"><li className="p-2 hover:bg-zinc-100 rounded-md hidden">Sign in</li></Link>
          </ul>
        </div>
        )}
      
        <ul className = 'hidden xl:flex justify-end gap-4 content-center my-auto'>
          
          <Link href="/"><li className="hover:bg-zinc-200 p-3 rounded-md">Home</li></Link>
          <Link href="/products/vegetable/page/1"><li className="hover:bg-zinc-200 p-3 rounded-md">Compare Vegetable Prices</li></Link>
          <Link href="/products/fruit/page/1"><li className="hover:bg-zinc-200 p-3 rounded-md">Compare Fruit Prices</li></Link>
          <Link href="/"><li className="hover:bg-zinc-200 p-3 rounded-md hidden">Sign up</li></Link>
          <Link href="/"><li className="hover:bg-zinc-200 p-3 rounded-md hidden">Sign in</li></Link>
        </ul>
      </nav>
    )
}