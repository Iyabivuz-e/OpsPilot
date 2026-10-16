// lib/api/chat.ts
import { z } from "zod"
import { api } from "./client"

export const MessageSchema = z.object({
  id: z.string(),
  role: z.enum(["user", "assistant"]),
  content: z.string(),
  created_at: z.string(),
})
export type Message = z.infer<typeof MessageSchema>

export const ConversationSchema = z.object({ id: z.string(), title: z.string() })

export const chatKeys = {
  all: ["conversations"] as const,
  messages: (id: string) => ["conversations", id, "messages"] as const,
}

export async function listConversations(signal?: AbortSignal) {
  const { data } = await api.get("/api/v1/conversations", { signal })
  return z.array(ConversationSchema).parse(data)
}

export async function getMessages(id: string, signal?: AbortSignal) {
  const { data } = await api.get(`/api/v1/conversations/${encodeURIComponent(id)}/messages`, { signal })
  return z.array(MessageSchema).parse(data)
}

export async function sendMessage(id: string, content: string) {
  const { data } = await api.post(`/api/v1/conversations/${encodeURIComponent(id)}/messages`, { content })
  return MessageSchema.parse(data)
}