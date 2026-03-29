"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useState, useRef, useEffect } from "react";
import { ChevronDown } from "lucide-react";
import { CATEGORIES, RETAILERS } from "@/lib/constants";

interface FilterBarProps {
  basePath: string;
}

interface DropdownProps {
  label: string;
  value: string;
  options: { label: string; value: string }[];
  onChange: (value: string) => void;
}

function Dropdown({ label, value, options, onChange }: DropdownProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selected = options.find((o) => o.value === value);

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 border border-gray-200 rounded-full px-4 py-2 text-sm hover:shadow-sm transition bg-white"
      >
        <span>{selected ? selected.label : label}</span>
        <ChevronDown size={14} />
      </button>

      {open && (
        <div className="absolute mt-2 bg-white border border-gray-100 rounded-xl shadow-lg z-50 p-2 min-w-[180px]">
          <ul className="flex flex-col text-sm">
            <li
              onClick={() => { onChange(""); setOpen(false); }}
              className={`px-3 py-2 rounded-md cursor-pointer hover:bg-zinc-100 ${value === "" ? "font-semibold" : ""}`}
            >
              {label}
            </li>
            {options.map((o) => (
              <li
                key={o.value}
                onClick={() => { onChange(o.value); setOpen(false); }}
                className={`px-3 py-2 rounded-md cursor-pointer hover:bg-zinc-100 ${value === o.value ? "font-semibold" : ""}`}
              >
                {o.label}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function FilterBar({ basePath }: FilterBarProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const updateParam = useCallback(
    (key: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      params.set("page", "1");
      router.push(`${basePath}?${params.toString()}`);
    },
    [router, searchParams, basePath]
  );

  const hasFilters =
    searchParams.get("retailer") ||
    searchParams.get("category") ||
    searchParams.get("sort_by") ||
    searchParams.get("multi_offer");

  return (
    <div className="flex flex-wrap gap-3 px-6 py-4 mt-4 items-center 3xl:w-8/10 mx-auto">
      <Dropdown
        label="All Retailers"
        value={searchParams.get("retailer") || ""}
        options={RETAILERS.map((r) => ({ label: r, value: r }))}
        onChange={(v) => updateParam("retailer", v)}
      />

      {/* <Dropdown
        label="All Categories"
        value={searchParams.get("category") || ""}
        options={CATEGORIES.map((c) => ({ label: c, value: c }))}
        onChange={(v) => updateParam("category", v)}
      /> */}

      <Dropdown
        label="Sort by Relevance"
        value={searchParams.get("sort_by") || ""}
        options={[
          { label: "Price: Low to High", value: "price_asc" },
          { label: "Price: High to Low", value: "price_desc" },
        ]}
        onChange={(v) => updateParam("sort_by", v)}
      />

      <Dropdown
        label="All Offers"
        value={searchParams.get("multi_offer") || ""}
        options={[{ label: "Multi-offer Only", value: "true" }]}
        onChange={(v) => updateParam("multi_offer", v)}
      />

      {hasFilters && (
        <button
          className="text-sm text-gray-500 underline hover:text-black"
          onClick={() => {
            const params = new URLSearchParams(searchParams.toString());
            params.delete("retailer");
            params.delete("category");
            params.delete("sort_by");
            params.delete("multi_offer");
            params.set("page", "1");
            router.push(`${basePath}?${params.toString()}`);
          }}
        >
          Clear filters
        </button>
      )}
    </div>
  );
}