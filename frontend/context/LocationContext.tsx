"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useSearchParams } from "next/navigation";

interface LocationContextType {
  postalCode: string;
  setPostalCode: (code: string) => void;
  distance: string;
  setDistance: (dist: string) => void;
}

const LocationContext = createContext<LocationContextType>({
  postalCode: "",
  setPostalCode: () => {},
  distance: "5",
  setDistance: () => {},
});

export function LocationProvider({ children }: { children: ReactNode }) {
  const [postalCode, setPostalCode] = useState("");
  const [distance, setDistance] = useState("5");
  const searchParams = useSearchParams();

  useEffect(() => {
    const urlPostal = searchParams.get("postal_code");
    const urlDistance = searchParams.get("set_distance");
    if (urlPostal) setPostalCode(urlPostal);
    if (urlDistance) setDistance(urlDistance);
  }, [searchParams]);

  return (
    <LocationContext.Provider value={{ postalCode, setPostalCode, distance, setDistance }}>
      {children}
    </LocationContext.Provider>
  );
}

export function useLocation() {
  return useContext(LocationContext);
}