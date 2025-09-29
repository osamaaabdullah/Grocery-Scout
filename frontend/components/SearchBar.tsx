"use client"

import { useState } from "react";
import { useRouter } from "next/navigation";
import { MapPinned } from 'lucide-react';

export default function SearchBar() {
    const [query, setQuery] = useState("");
    const [postalCode, setPostalCode] = useState("");
    const [loadingLocation, setLoadingLocation] = useState(false);
    const router = useRouter();

    const handleUseLocation = () => {
        if (!navigator.geolocation) return alert("Geolocation not supported");

        setLoadingLocation(true);
        navigator.geolocation.getCurrentPosition(
            async (pos) => {
                const { latitude, longitude } = pos.coords;
                try {
                    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`);
                    const data = await res.json();
                    setPostalCode(data.address.postcode || "");
                } catch {
                    alert("Unable to detect postal code");
                } finally {
                    setLoadingLocation(false);
                }
            },
            () => {
                alert("Location detection failed");
                setLoadingLocation(false);
            }
        );
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!query) return;
        router.push(`/results?search=${encodeURIComponent(query)}&postalCode=${encodeURIComponent(postalCode)}`);
    };

    return (
        <form onSubmit={handleSubmit} className="flex gap-2" >
            
            <div className="pl-1 w-1/2">
                <input
                type="text"
                placeholder="Search products"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="pl-3 w-full rounded-full"
                />
            </div>

          
            <div className="pr-1 w-1/2 flex gap-2">
            
                <button
                type="button"
                onClick={handleUseLocation}
                disabled={loadingLocation}
                className=""
                >
                {loadingLocation ? "..." : <MapPinned />}
                </button>
                
                <input
                type="text"
                placeholder="Postal Code"
                value={postalCode}
                onChange={(e) => setPostalCode(e.target.value)}
                className="w-2/3 pl-2 rounded-full"
                />

                

                
                <button
                type="submit"
                className="w-1/3 rounded-full hover:bg-zinc-200"
                >
                Search
                </button>
            </div>
        </form>

    );
}

{/* <form onSubmit={handleSubmit} className="flex gap-2">
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
            </form> */}