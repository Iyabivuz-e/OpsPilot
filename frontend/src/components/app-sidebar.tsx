"use client"

import * as React from "react"
import Link from "next/link"
import {
  ChartBarIcon,
  CommandIcon,
  FolderIcon,
  LayoutDashboardIcon,
} from "lucide-react"

import { NavDocuments, type ChatNavItem } from "@/components/nav-documents"
import { NavMain, type NavMainItem } from "@/components/nav-main"
import { NavUser } from "@/components/nav-user"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar"
import { usePathname } from "next/navigation"

const data: {
  user: { name: string; email: string; avatar: string }
  navMain: NavMainItem[]
  chats: ChatNavItem[]
} = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard",
      icon: <LayoutDashboardIcon />,
    },
    {
      title: "Cases",
      url: "/cases",
      icon: <FolderIcon />,
    },
    {
      title: "Analytics",
      url: "/analytics",
      icon: <ChartBarIcon />,
    },
  ],
  chats: [
    { id: "1", name: "Chat 1" },
    { id: "2", name: "Chat 2" },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {

   const pathname = usePathname()
  const { setOpenMobile } = useSidebar()
  // Close the mobile sidebar sheet whenever the route changes
  React.useEffect(() => {
    setOpenMobile(false)
  }, [pathname, setOpenMobile])

  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              className="data-[slot=sidebar-menu-button]:p-1.5!"
              render={<Link href="/dashboard" />}
            >
              <CommandIcon className="size-5!" />
              <span className="text-base font-semibold">OpsPilot.</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavDocuments items={data.chats} />
      </SidebarContent>

      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  )
}