"use client"
import { useLayoutEffect, useRef } from "react"
import { MessageBubble } from "./message-bubble"
import type { Message } from "@/lib/api/chat"

const STICK_THRESHOLD_PX = 80

type MessageListProps = {
  messages: Message[]
  isAssistantTyping?: boolean
}

export function MessageList({ messages, isAssistantTyping = false }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null)
  // Start pinned to the bottom. Stop auto-scrolling when the user scrolls up to read older messages.
  const stickToBottom = useRef(true)

  function handleScroll() {
    const el = scrollRef.current
    if (!el) return
    stickToBottom.current = el.scrollHeight - el.scrollTop - el.clientHeight < STICK_THRESHOLD_PX
  }

  const last = messages.at(-1)

  useLayoutEffect(() => {
    const el = scrollRef.current
    if (!el) return
    // Always follow your own new message; otherwise only follow if already near the bottom.
    if (stickToBottom.current || last?.role === "user") {
      el.scrollTop = el.scrollHeight
    }
  }, [messages.length, last?.id, last?.role, isAssistantTyping])

  if (messages.length === 0 && !isAssistantTyping) {
    return (
      <div className="flex flex-1 items-center justify-center p-6 text-sm text-muted-foreground">
        No messages yet. Ask OpsPilot something to get started.
      </div>
    )
  }

  return (
    <div
      ref={scrollRef}
      onScroll={handleScroll}
      role="log"
      aria-live="polite"
      aria-relevant="additions"
      className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto p-4 lg:p-6"
    >
      {messages.map((m) => (
        <MessageBubble key={m.id} message={m} />
      ))}
      {isAssistantTyping && <TypingIndicator />}
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex justify-start" aria-label="OpsPilot is typing">
      <div className="flex gap-1 rounded-2xl bg-muted px-4 py-3">
        {[0, 150, 300].map((delay) => (
          <span
            key={delay}
            className="size-1.5 animate-bounce rounded-full bg-muted-foreground"
            style={{ animationDelay: `${delay}ms` }}
          />
        ))}
      </div>
    </div>
  )
}