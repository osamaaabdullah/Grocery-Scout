"use client"

import { useState } from "react";
import { useRouter } from "next/navigation";
import { SearchIcon } from 'lucide-react';

export default function SearchBar({ postalCode, distance}: any) {
    const [query, setQuery] = useState("");
    const router = useRouter();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!query) return;
        router.push(`/results?search=${encodeURIComponent(query)}&postal_code=${postalCode}&set_distance=${distance}`);
    };

    return (
        <form onSubmit={handleSubmit} className="flex gap-2 items-center " >
                <div className="pl-1 flex-grow">
                    <input
                    type="text"
                    placeholder="Search products"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="pl-3 w-full rounded-full"
                    />
                </div>
                
                <div>
                    <button
                    type="submit"
                    className="flex pr-3"
                    >
                    <SearchIcon/>
                    </button>
                </div>
        </form>

    );
}
