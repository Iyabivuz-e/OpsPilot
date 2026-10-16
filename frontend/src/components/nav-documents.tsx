"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  MessageSquareIcon,
  MoreHorizontalIcon,
  PlusIcon,
  Trash2Icon,
} from "lucide-react"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  SidebarGroup,
  SidebarGroupAction,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar"

export type ChatNavItem = {
  id: string
  name: string
}

export function NavDocuments({ items }: { items: ChatNavItem[] }) {
  const { isMobile } = useSidebar()
  const pathname = usePathname()

  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden">
      <SidebarGroupLabel>Chats</SidebarGroupLabel>

      {/* "+" button in the Chats header to start a new conversation */}
      <SidebarGroupAction title="New Conversation" render={<Link href="/chat" />}>
        <PlusIcon />
        <span className="sr-only">New Conversation</span>
      </SidebarGroupAction>

      <SidebarMenu>
        {items.map((item) => {
          const href = `/chat/${encodeURIComponent(item.id)}`
          return (
            <SidebarMenuItem key={item.id}>
              <SidebarMenuButton
                isActive={pathname === href}
                render={<Link href={href} />}
              >
                <MessageSquareIcon />
                <span>{item.name}</span>
              </SidebarMenuButton>

              <DropdownMenu>
                <DropdownMenuTrigger
                  render={
                    <SidebarMenuAction
                      showOnHover
                      className="aria-expanded:bg-muted"
                    />
                  }
                >
                  <MoreHorizontalIcon />
                  <span className="sr-only">More options for {item.name}</span>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                  className="w-24"
                  side={isMobile ? "bottom" : "right"}
                  align={isMobile ? "end" : "start"}
                >
                  <DropdownMenuItem variant="destructive">
                    <Trash2Icon />
                    <span>Delete</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </SidebarMenuItem>
          )
        })}
      </SidebarMenu>
    </SidebarGroup>
  )
}