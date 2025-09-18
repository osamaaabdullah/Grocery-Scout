"use client"

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SearchBar() {

    const [query, setQuery] = useState("");
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if(!query) 
            return;

        router.push(`/results?search=${encodeURIComponent(query)}`)
    };

    return (
            <form onSubmit={handleSubmit} className="flex gap-2">
                <input
                    type = "text"
                    placeholder= "Search Products"
                    value = {query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="flex-auto pl-3 rounded-full focus:outline-none"
                />
                <div className="flex justify-center p-1 mr-2  rounded-full w-15/100 hover:bg-zinc-200">
                    <button type = "submit" >
                        Search
                    </button>
                    
                </div>
            </form>
    );
}