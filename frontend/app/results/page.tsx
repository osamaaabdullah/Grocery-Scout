import { Suspense } from "react";
import ResultsClient from "./ResultsClient";
import Pagination from "@/components/Pagination";
import FilterBar from "@/components/FilterBar";

interface SearchPageProps {
  searchParams: Promise<{
    search?: string;
    postal_code?: string;
    set_distance?: string;
    page?: string;
    category?: string;
    retailer?: string;
    sort_by?: string;
    multi_offer?: string;
  }>;
}

async function getResults(
  search: string,
  postalCode: string,
  distance: string,
  page: string,
  category: string,
  retailer: string,
  sortBy: string,
  multiOffer: string
) {
  const res = await fetch(
    `${process.env.BACKEND_URL}/prices/search?product_name=${encodeURIComponent(search)}&postal_code=${encodeURIComponent(postalCode)}&set_distance=${encodeURIComponent(distance)}&page=${page}&category=${encodeURIComponent(category)}&retailer=${encodeURIComponent(retailer)}&sort_by=${encodeURIComponent(sortBy)}&multi_offer=${multiOffer}`,
    { cache: "no-store" }
  );
  if (!res.ok) throw new Error("Failed to fetch results");
  return res.json();
}

export default async function ResultsPage({ searchParams }: SearchPageProps) {
  const sp = await searchParams;
  const search = sp.search || "";
  const postalCode = sp.postal_code || `${process.env.DEFAULT_POSTAL_CODE}`;
  const distance = sp.set_distance || "5";
  const page = sp.page || "1";
  const category = sp.category || "";
  const retailer = sp.retailer || "";
  const sortBy = sp.sort_by || "relevance";
  const multiOffer = sp.multi_offer || "false";
  const currentPage = parseInt(page, 10) || 1;

  const data = await getResults(search, postalCode, distance, page, category, retailer, sortBy, multiOffer);
  const results = data.results ?? [];
  const totalPages = data.pagination?.total_pages ?? 1;

  return (
    <div>
      <Suspense fallback={<div>Loading filters...</div>}>
        <FilterBar basePath="/results" />
      </Suspense>

      <Suspense fallback={<div>Loading search results...</div>}>
        <ResultsClient
          results={results}
          search={search}
          postalCode={postalCode}
        />
        <div className="w-9/10 mx-auto">
          <Pagination
            page={currentPage}
            totalPages={totalPages}
            search={search}
            postalCode={postalCode}
            distance={distance}
            category={category}
            retailer={retailer}
            sortBy={sortBy}
            multiOffer={multiOffer}
          />
        </div>
      </Suspense>
    </div>
  );
}