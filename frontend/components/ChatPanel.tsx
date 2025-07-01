import { useState, useEffect, useRef } from "react"
import axios from "axios"

type ChatMsg = {
  role: "user" | "assistant"
  content: string
  actions?: string[]
  reflexion?: string
}

export default function ChatPanel({
  sessionId = "demo-session",
}: {
  sessionId?: string
}) {
  const [messages, setMessages] = useState<ChatMsg[]>([
    {
      role: "assistant",
      content: "Hello! I’m Codex. What would you like to build today?",
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const streamAssistantMessage = async (
    text: string,
    actions?: string[],
    reflexion?: string,
  ) => {
    let current: ChatMsg = { role: "assistant", content: "" }
    setMessages((prev) => [...prev, current])

    for (const ch of text) {
      await new Promise((r) => setTimeout(r, 20))
      current = { ...current, content: current.content + ch }
      setMessages((prev) => {
        const updated = [...prev]
        updated[updated.length - 1] = current
        return updated
      })
    }

    current = { ...current, actions, reflexion }
    setMessages((prev) => {
      const updated = [...prev]
      updated[updated.length - 1] = current
      return updated
    })
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    const newHistory = [...messages, { role: "user", content: input }]
    setMessages(newHistory)
    setInput("")
    setLoading(true)

    try {
      const res = await axios.post("/api/chat", {
        session_id: sessionId,
        message: input,
        history: newHistory,
      })

      const { response, actions, reflexion_summary } = res.data
      await streamAssistantMessage(response, actions, reflexion_summary)
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "❌ Error processing your request." },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed right-0 bottom-0 w-[400px] h-[600px] bg-white border-l border-t z-50 flex flex-col shadow-lg">
      <div className="p-2 border-b bg-gray-100 font-semibold">💬 Codex Chat</div>
      <div className="flex-1 overflow-auto p-2 space-y-3">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`text-sm max-w-[80%] break-words ${
              msg.role === "user" ? "ml-auto text-right" : "mr-auto text-left"
            }`}
          >
            <div
              className={`p-2 rounded ${
                msg.role === "user" ? "bg-blue-100" : "bg-gray-100"
              }`}
            >
              {msg.content}
            </div>
            {msg.actions && msg.actions.length > 0 && (
              <div className="mt-1 flex flex-wrap gap-1">
                {msg.actions.map((a) => (
                  <span
                    key={a}
                    className="bg-purple-200 text-xs px-1.5 py-0.5 rounded"
                  >
                    {a}
                  </span>
                ))}
              </div>
            )}
            {msg.reflexion && (
              <div className="text-[10px] text-gray-500 mt-1">{msg.reflexion}</div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div className="border-t p-2 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
          className="flex-1 border px-2 py-1 rounded"
          placeholder="Ask Codex..."
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white px-3 py-1 rounded"
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  )
}

