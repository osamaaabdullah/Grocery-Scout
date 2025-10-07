"use client";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useSearchParams } from "next/navigation";


type HrefBuilder = (page: string) => string;

interface Pagination{
    page: number;
    totalPages: number;
    hrefForPage: HrefBuilder;
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

}