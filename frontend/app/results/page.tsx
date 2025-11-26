import { Suspense } from "react";
import ResultsClient from "./ResultsClient";

export default function Page() {
  return (
    <Suspense fallback={<div>Loading search results...</div>}>
      <ResultsClient />
    </Suspense>
  );
}
