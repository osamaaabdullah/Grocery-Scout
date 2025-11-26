"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { MapPinned, ChevronDown, LocateFixed } from "lucide-react";

interface PostalbarProps {
  postalCode?: string;
  setPostalCode?: (code: string) => void;
  distance?: string;
  setDistance?: (dist: string) => void;
}

export default function Postalbar({
  postalCode = "",
  setPostalCode = () => {},
  distance = "5",
  setDistance = () => {},
}: PostalbarProps) {
  const [open, setOpen] = useState(false);
  const [loadingLocation, setLoadingLocation] = useState(false);

  const router = useRouter();
  const searchParams = useSearchParams();

  // Load postal + distance from URL on first render
  useEffect(() => {
    const urlPostal = searchParams.get("postal_code");
    const urlDistance = searchParams.get("set_distance");

    if (urlPostal && !postalCode) setPostalCode(urlPostal);
    if (urlDistance && !distance) setDistance(urlDistance);
  }, []);

  // --- NEXT.JS NAVIGATION UPDATE ---
  const updateURLParams = (postal: string, dist: string) => {
    const url = new URL(window.location.href);

    if (postal) url.searchParams.set("postal_code", postal);
    if (dist) url.searchParams.set("set_distance", dist);

    router.replace(url.toString()); // <--- KEY FIX
  };

  const handleUseLocation = () => {
    if (!navigator.geolocation) return alert("Geolocation not supported");
    setLoadingLocation(true);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}&format=json`
          );
          const data = await res.json();

          if (data.address.postcode) {
            const pc = data.address.postcode;

            setPostalCode(pc);
            updateURLParams(pc, distance);
          } else {
            alert("Postal code not found");
          }
        } catch {
          alert("Unable to detect postal code");
        } finally {
          setLoadingLocation(false);
          setOpen(false);
        }
      },
      () => {
        alert("Location detection failed");
        setLoadingLocation(false);
      }
    );
  };

  return (
    <div className="relative w-full text-left">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-2 border border-gray-200 rounded-full px-4 py-2 hover:shadow-sm transition [@media(max-width:480px)]:border-none [@media(max-width:480px)]:justify-between"
      >
        <div className="flex items-center gap-2">
          <MapPinned size={18} />
          <span>Location</span>
        </div>
        <ChevronDown size={16} />
      </button>

      {open && (
        <div
          className="fixed inset-0 bg-black/10 z-40"
          onClick={() => setOpen(false)}
        />
      )}

      {open && (
        <div className="absolute mt-2 w-60 bg-white border border-gray-100 rounded-xl shadow-lg z-50 p-3 [@media(max-width:480px)]:w-full">
          <div className="flex flex-col gap-2">

            {/* POSTAL CODE INPUT */}
            <div className="mt-3 flex gap-2 items-center">
              <input
                type="text"
                placeholder="Enter postal code"
                value={postalCode}
                onChange={(e) => setPostalCode(e.target.value)}
                className="border border-gray-200 rounded-full px-3 py-2 w-40 [@media(max-width:480px)]:w-full"
              />

              <button
                onClick={() => {
                  updateURLParams(postalCode, distance);
                  setOpen(false);
                }}
                className="text-sm font-bold hover:underline m-2 p-2 mx-auto bg-[#D4F6FF] rounded-full"
              >
                Done
              </button>
            </div>

            {/* USE MY LOCATION */}
            <button
              onClick={handleUseLocation}
              disabled={loadingLocation}
              className="text-left px-3 py-2 rounded-md hover:bg-gray-50 flex items-center gap-2"
            >
              <LocateFixed size={16} />
              {loadingLocation ? "Detecting..." : "Use My Location"}
            </button>

            {/* DISTANCE SELECT */}
            <div className="flex items-center justify-between px-3 py-2 mt-1 border-t border-gray-100">
              <label className="text-sm text-gray-600">Distance (km)</label>
              <select
                value={distance}
                onChange={(e) => {
                  const dist = e.target.value;
                  setDistance(dist);
                  updateURLParams(postalCode, dist);
                  setOpen(false);
                }}
                className="border border-gray-200 rounded-md text-sm p-1"
              >
                <option value="1">1</option>
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="25">25</option>
              </select>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
