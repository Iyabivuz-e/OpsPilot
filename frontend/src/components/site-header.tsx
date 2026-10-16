// src/components/site-header.tsx
"use client"

import { usePathname } from "next/navigation"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

function getHeaderTitle(pathname: string): string {
  if (pathname === "/dashboard") return "Dashboard"
  if (pathname.startsWith("/cases")) return "Cases"
  if (pathname.startsWith("/analytics")) return "Analytics"
  if (pathname === "/chat") return "New Conversation"
  if (pathname.startsWith("/chat/")) {
    const id = decodeURIComponent(pathname.replace("/chat/", ""))
    return `Conversation #${id}`
  }
  return "OpsPilot"
}

export function SiteHeader() {
  const pathname = usePathname()
  const title = getHeaderTitle(pathname)

  return (
    <header className="sticky top-0 z-10 flex h-(--header-height) shrink-0 items-center gap-2 border-b bg-background/95 backdrop-blur transition-[width,height] ease-linear supports-[backdrop-filter]:bg-background/60 group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
      <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
        <SidebarTrigger className="-ml-1" />
        <Separator
          orientation="vertical"
          className="mx-2 h-4 data-vertical:self-auto"
        />
        <h1 className="text-base font-medium">{title}</h1>
      </div>
    </header>
  )
}