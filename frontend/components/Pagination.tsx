"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";

interface PaginationProps {
  page: number;
  totalPages: number;
  // Products mode
  type?: string;
  // Search results mode
  search?: string;
  postalCode?: string;
  distance?: string;
  category?: string;
  retailer?: string;
  sortBy?: string;
  multiOffer?: string;
}

function buildPages(current: number, total: number): Array<number | "dots"> {
  const pages: Array<number | "dots"> = [];
  const range = 1;

  if (total <= 1) {
    pages.push(1);
    return pages;
  }

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - range && i <= current + range)) {
      pages.push(i);
    } else if (pages[pages.length - 1] !== "dots") {
      pages.push("dots");
    }
  }

  return pages;
}

export default function Pagination({ page, totalPages, type, search, postalCode, distance, category, retailer, sortBy, multiOffer }: PaginationProps) {
  const pages = buildPages(page, totalPages);

  const buildHref = (p: number) => {
    if (type) {
      return postalCode
        ? `/products/${type}/page/${p}?postal_code=${postalCode}`
        : `/products/${type}/page/${p}`;
    }
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (postalCode) params.set("postal_code", postalCode);
    if (distance) params.set("set_distance", distance);
    if (category) params.set("category", category);
    if (retailer) params.set("retailer", retailer);
    if (sortBy) params.set("sort_by", sortBy);
    if (multiOffer) params.set("multi_offer", multiOffer);
    params.set("page", String(p));
    return `/results?${params.toString()}`;
  };

  const baseItem = "h-15 w-15 inline-flex items-center rounded-full px-3 py-2 justify-center text-sm transition";
  const idle = "hover:bg-gray-50";
  const selected = "text-black border-3 border-[#D4F6FF]";
  const muted = "opacity-50 cursor-not-allowed";

  return (
    <nav className="mt-8 flex justify-center" aria-label="Pagination">
      <ul className="flex items-center gap-3">
        <li>
          {page > 1 ? (
            <Link href={buildHref(page - 1)} rel="prev" className={`${baseItem} ${idle}`}>
              <ChevronLeft className="size-10" />
            </Link>
          ) : (
            <span className={`${baseItem} ${muted}`} aria-disabled="true">
              <ChevronLeft className="size-10" />
            </span>
          )}
        </li>

        {pages.map((p, i) => (
          <li key={`${p}-${i}`}>
            {p === "dots" ? (
              <span className="px-3 py-2">...</span>
            ) : p === page ? (
              <span className={`${baseItem} ${selected}`}>{p}</span>
            ) : (
              <Link href={buildHref(p)} className={`${baseItem} ${idle}`}>
                {p}
              </Link>
            )}
          </li>
        ))}

        <li>
          {page < totalPages ? (
            <Link href={buildHref(page + 1)} rel="next" className={`${baseItem} ${idle}`}>
              <ChevronRight className="size-10" />
            </Link>
          ) : (
            <span className={`${baseItem} ${muted}`} aria-disabled="true">
              <ChevronRight className="size-10" />
            </span>
          )}
        </li>
      </ul>
    </nav>
  );
}