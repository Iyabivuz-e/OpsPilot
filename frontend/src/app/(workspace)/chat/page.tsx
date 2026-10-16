"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { MessageSquarePlusIcon } from "lucide-react"

import { Composer } from "@/components/chat/composer"
import { Button } from "@/components/ui/button"

const STARTER_PROMPTS = [
  "Check the status of order #1042",
  "How do we handle a refund for a damaged item?",
  "List recent failed payment attempts",
]

export default function NewChatPage() {
  const router = useRouter()
  const [isCreating, setIsCreating] = useState(false)

  async function handleStartConversation(firstMessage: string) {
    setIsCreating(true)
    try {
      // TODO: Once your FastAPI endpoint exists, replace this with:
      // const { id } = await createConversation(firstMessage)
      const id = crypto.randomUUID().slice(0, 8)
      router.push(`/chat/${encodeURIComponent(id)}`)
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <div className="flex h-[calc(100svh-var(--header-height))] flex-col md:h-[calc(100svh-var(--header-height)-1rem)]">
      <div className="flex flex-1 flex-col items-center justify-center gap-6 p-6 text-center">
        <div className="flex size-12 items-center justify-center rounded-2xl bg-muted">
          <MessageSquarePlusIcon className="size-6 text-muted-foreground" />
        </div>

        <div className="max-w-md space-y-1.5">
          <h2 className="text-lg font-semibold">Ask OpsPilot about orders, refunds, payments, or internal policies.</h2>
          {/* <p className="text-sm text-muted-foreground">
            Ask OpsPilot about orders, refunds, payments, or internal policies.
          </p> */}
        </div>

        {/* <div className="flex flex-wrap justify-center gap-2 max-w-lg">
          {STARTER_PROMPTS.map((prompt) => (
            <Button
              key={prompt}
              variant="outline"
              size="sm"
              disabled={isCreating}
              onClick={() => handleStartConversation(prompt)}
            >
              {prompt}
            </Button>
          ))}
        </div> */}
      </div>

      <Composer
        disabled={isCreating}
        placeholder="Type a message to start a new conversation…"
        onSubmit={handleStartConversation}
      />
    </div>
  )
}