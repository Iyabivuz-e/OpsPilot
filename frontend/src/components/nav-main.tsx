"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { CirclePlusIcon } from "lucide-react"

import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

export type NavMainItem = {
  title: string
  url: string
  icon?: React.ReactNode
}

export function NavMain({ items }: { items: NavMainItem[] }) {
  const pathname = usePathname()

  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        {/* Primary action: New Conversation (/chat) */}
        {/* <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="New Conversation"
              isActive={pathname === "/chat"}
              render={<Link href="/chat" />}
              className="min-w-8 bg-primary text-primary-foreground duration-200 ease-linear hover:bg-primary/90 hover:text-primary-foreground active:bg-primary/90 active:text-primary-foreground"
            >
              <CirclePlusIcon />
              <span>New Conversation</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu> */}

        {/* Main section routes: /dashboard, /cases, /analytics */}
        <SidebarMenu>
          {items.map((item) => {
            const isActive =
              pathname === item.url || pathname.startsWith(`${item.url}/`)

            return (
              <SidebarMenuItem key={item.url}>
                <SidebarMenuButton
                  tooltip={item.title}
                  isActive={isActive}
                  render={<Link href={item.url} />}
                >
                  {item.icon}
                  <span>{item.title}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            )
          })}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}