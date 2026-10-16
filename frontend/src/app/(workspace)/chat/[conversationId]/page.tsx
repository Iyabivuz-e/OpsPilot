// app/(workspace)/chat/[conversationId]/page.tsx
import { notFound } from "next/navigation"
import { ChatWindow } from "@/components/chat/chat-window"

const CONVERSATION_ID = /^[A-Za-z0-9_-]{1,64}$/ // match your backend id format

export default async function ChatPage(props: PageProps<"/chat/[conversationId]">) {
  const { conversationId } = await props.params   // params is a Promise in Next 15+
  if (!CONVERSATION_ID.test(conversationId)) notFound()

  // key = full remount when switching chats → no leaked draft text/scroll/stream from the previous chat
  return <ChatWindow key={conversationId} conversationId={conversationId} />
}