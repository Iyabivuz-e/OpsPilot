import { memo } from "react"
import { cn } from "@/lib/utils"
import type { Message } from "@/lib/api/chat"

const timeFormatter = new Intl.DateTimeFormat(undefined, { hour: "2-digit", minute: "2-digit" })

function formatTime(iso: string) {
  const date = new Date(iso)
  return Number.isNaN(date.getTime()) ? "" : timeFormatter.format(date)
}

export const MessageBubble = memo(function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user"
  const isPending = message.id.startsWith("temp-") // optimistic message, not yet confirmed by the server

  return (
    <div
      className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}
      data-message-id={message.id}   // makes a specific message easy to find in DevTools
      data-role={message.role}
    >
      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-4 py-2 text-sm",
          isUser ? "bg-primary text-primary-foreground" : "bg-muted text-foreground",
          isPending && "opacity-60"
        )}
      >
        {/* Plain text on purpose: React escapes it, so there's no XSS risk from model output. */}
        <p className="break-words whitespace-pre-wrap">{message.content}</p>
        <time
          dateTime={message.created_at}
          className={cn("mt-1 block text-[0.7rem]", isUser ? "text-primary-foreground/70" : "text-muted-foreground")}
        >
          {isPending ? "Sending…" : formatTime(message.created_at)}
        </time>
      </div>
    </div>
  )
})