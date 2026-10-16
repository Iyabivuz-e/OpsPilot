import { Skeleton } from "@/components/ui/skeleton"
import { cn } from "@/lib/utils"

const ROWS = [
  { align: "start", width: "w-2/3" },
  { align: "end", width: "w-1/2" },
  { align: "start", width: "w-3/4" },
  { align: "end", width: "w-1/3" },
] as const

export function ChatSkeleton() {
  return (
    <div className="flex flex-1 flex-col gap-4 p-4 lg:p-6" aria-busy="true" aria-label="Loading conversation">
      {ROWS.map((row, i) => (
        <div key={i} className={cn("flex", row.align === "end" ? "justify-end" : "justify-start")}>
          <Skeleton className={cn("h-14 rounded-2xl", row.width)} />
        </div>
      ))}
    </div>
  )
}