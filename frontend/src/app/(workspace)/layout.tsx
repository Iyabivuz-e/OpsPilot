import { AppSidebar } from "@/components/app-sidebar"
import { Providers } from "@/components/providers"
import { SiteHeader } from "@/components/site-header"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

export default function WorkspaceLayout({ children }: LayoutProps<"/">) {
  return (
    <Providers>
      <SidebarProvider
        className="h-svh overflow-hidden"
        style={
          {
            "--sidebar-width": "calc(var(--spacing) * 72)",
            "--header-height": "calc(var(--spacing) * 12)",
          } as React.CSSProperties
        }
      >
        <AppSidebar variant="inset" />
        <SidebarInset className="min-h-0 overflow-hidden">
          <SiteHeader />
          <div className="flex min-h-0 flex-1 flex-col overflow-y-auto">
            {children}
          </div>
        </SidebarInset>
      </SidebarProvider>
    </Providers>
  )
}