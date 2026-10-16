"use client"
import { useLayoutEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react"
import { SendHorizontalIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export const MAX_MESSAGE_LENGTH = 4000 // keep in sync with backend validation
const MAX_TEXTAREA_HEIGHT_PX = 200

type ComposerProps = {
  onSubmit: (content: string) => void
  disabled?: boolean
  placeholder?: string
}

export function Composer({ onSubmit, disabled = false, placeholder = "Ask OpsPilot…" }: ComposerProps) {
  const [value, setValue] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const trimmed = value.trim()
  const tooLong = trimmed.length > MAX_MESSAGE_LENGTH
  const canSend = !disabled && trimmed.length > 0 && !tooLong

  // Auto-grow the textarea up to a max height. A JS fallback is used so it works in every browser.
  useLayoutEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = "auto"
    el.style.height = `${Math.min(el.scrollHeight, MAX_TEXTAREA_HEIGHT_PX)}px`
  }, [value])

  function submit() {
    if (!canSend) return
    onSubmit(trimmed)
    setValue("")
    textareaRef.current?.focus()
  }

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    submit()
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    // Enter sends, Shift+Enter adds a new line.
    // isComposing guard: don't send mid-word for IME users (Chinese, Japanese, Korean input…).
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t bg-background p-3 lg:p-4">
      <div className="flex items-end gap-2 rounded-xl border bg-background p-2 focus-within:ring-3 focus-within:ring-ring/50">
        <label htmlFor="chat-composer" className="sr-only">Message</label>
        <textarea
          id="chat-composer"
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          autoFocus
          aria-invalid={tooLong || undefined}
          className="max-h-[200px] min-h-9 flex-1 resize-none bg-transparent px-2 py-1.5 text-sm outline-none placeholder:text-muted-foreground disabled:opacity-50"
        />
        <Button type="submit" size="icon" disabled={!canSend} aria-label="Send message">
          <SendHorizontalIcon />
        </Button>
      </div>
      <p className={cn("mt-1 px-1 text-xs text-muted-foreground", tooLong && "text-destructive")}>
        {tooLong
          ? `Message is too long (${trimmed.length}/${MAX_MESSAGE_LENGTH}).`
          : "Enter to send · Shift+Enter for a new line"}
      </p>
    </form>
  )
}