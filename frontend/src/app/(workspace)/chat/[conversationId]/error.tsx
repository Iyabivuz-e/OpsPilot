"use client"
import { useEffect } from "react"

export default function ChatError({ error, retry }: { error: Error & { digest?: string }; retry: () => void }) {
  useEffect(() => {
    console.error("[chat] render failed", { digest: error.digest, error }) // swap for Sentry etc.
  }, [error])
  return (
    <div className="p-6">
      <p>Couldn't load this conversation.</p>
      <button onClick={retry}>Try again</button>
    </div>
  )
}