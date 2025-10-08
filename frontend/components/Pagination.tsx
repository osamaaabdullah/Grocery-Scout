"use client";
import { ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";


type HrefBuilder = (page: number) => string;

interface Pagination{
    page: number;
    totalPages: number;
    hrefForPage?: HrefBuilder;
}

function buildPages(current: number, total: number): Array<number|"dots"> {
    const pages: Array<number| "dots"> = [];
    const range = 1;
    
    if (total <= 1){
        pages.push(1)
        return pages;
    }

    for(let i =1; i<=total;i++){
        if (i === 1 || i === total || (i>= current-range && i<= current+range)){
            pages.push(i)
        }
        else if(pages[pages.length-1]!=="dots"){
            pages.push("dots")
        }
    }
    return pages;
}

export default function Pagination({
    page,
    totalPages,
    hrefForPage = (p) => `?page=${p}`
}: Pagination){

    const pages = buildPages(page, totalPages);

    const baseItem =
    "h-15 w-15 inline-flex items-center rounded-full px-3 py-2 justify-center text-sm transition";
    const idle = "hover:bg-gray-50";
    const selected = "text-black border-3 border-[#D4F6FF]";
    const muted = "opacity-50 cursor-not-allowed";
        
    return(
        <nav className="mt-8 flex justify-center" aria-label="Pagination">
            <ul className="flex items-center gap-3">
                <li>
                    {page>1? (
                        <Link 
                        href={hrefForPage(page-1)} rel="prev" className={`${baseItem} ${idle}`}>
                            <ChevronLeft className="size-10"/>
                        </Link>
                    ):(
                        <span className={`${baseItem} ${muted}`} aria-disabled="true">
                            <ChevronLeft className="size-10"/>
                        </span>
                    )}
                </li>
                {pages.map((p,i)=> (
                    <li key = {`${p}-${i}`}>
                        {p === "dots" ? (
                            <span className="px-3 py-2">...</span>
                        ): p===page? (
                            <span className={`${baseItem} ${selected}`}>{p}</span>
                        ):(
                            <Link
                                href={hrefForPage(p)} className={`${baseItem} ${idle}`}>
                                    {p}
                                </Link>
                        )}
                    </li>
                ))}
                <li>
                    {page <totalPages ? (
                        <Link
                            href = {hrefForPage(page+1)} rel="next" className={`${baseItem} ${idle}`}>
                                <ChevronRight className="size-10"/>
                            </Link>
                    ):
                     (<span className={`${baseItem} ${muted}`} aria-disabled="true">
                        <ChevronRight className="size-10"/>
                     </span>)}
                </li>
            </ul>
        </nav>
    )

}