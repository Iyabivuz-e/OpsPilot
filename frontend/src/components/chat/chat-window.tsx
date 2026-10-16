"use client"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { useConversation } from "@/hooks/use-conversations"
import { ChatSkeleton } from "./chat-skeleton"
import { Composer } from "./composer"
import { MessageList } from "./message-list"

export function ChatWindow({ conversationId }: { conversationId: string }) {
  const { messages, send } = useConversation(conversationId)

  function handleSend(content: string) {
    send.mutate(content, {
      onError: (err) => {
        console.error("[chat] send failed", { conversationId, err })
        toast.error("Message failed to send. Please try again.")
      },
    })
  }

  return (
    // Bounded height so only the message list scrolls, not the whole page.
    // The 1rem is the m-2 (top + bottom) that SidebarInset gets with variant="inset" on md+.
    <div className="flex h-[calc(100svh-var(--header-height))] flex-col md:h-[calc(100svh-var(--header-height)-1rem)]">
      {messages.isPending ? (
        <ChatSkeleton />
      ) : messages.isError ? (
        <div className="flex flex-1 flex-col items-center justify-center gap-3 p-6 text-sm" role="alert">
          <p>Couldn't load this conversation.</p>
          <Button variant="outline" onClick={() => messages.refetch()} disabled={messages.isFetching}>
            {messages.isFetching ? "Retrying…" : "Try again"}
          </Button>
        </div>
      ) : (
        <MessageList messages={messages.data} isAssistantTyping={send.isPending} />
      )}

      <Composer onSubmit={handleSend} disabled={send.isPending || messages.isError} />
    </div>
  )
}