// hooks/use-conversation.ts
"use client"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { chatKeys, getMessages, sendMessage, type Message } from "@/lib/api/chat"

export function useConversation(conversationId: string) {
  const qc = useQueryClient()
  const key = chatKeys.messages(conversationId)

  const messages = useQuery({
    queryKey: key,
    queryFn: ({ signal }) => getMessages(conversationId, signal), // aborted if you switch chats
  })

  const send = useMutation({
    mutationFn: (content: string) => sendMessage(conversationId, content),
    onMutate: async (content) => {
      await qc.cancelQueries({ queryKey: key })
      const previous = qc.getQueryData<Message[]>(key)
      const optimistic: Message = {
        id: `temp-${crypto.randomUUID()}`, role: "user", content, created_at: new Date().toISOString(),
      }
      qc.setQueryData<Message[]>(key, (old = []) => [...old, optimistic])
      return { previous }
    },
    onError: (_err, _content, ctx) => qc.setQueryData(key, ctx?.previous), // roll back
    onSettled: () => qc.invalidateQueries({ queryKey: key }),
  })

  return { messages, send }
}