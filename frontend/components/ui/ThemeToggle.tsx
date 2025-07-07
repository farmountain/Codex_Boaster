"use client"
import { useEffect, useState } from 'react'

export default function ThemeToggle() {
  const [dark, setDark] = useState(false)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])

  return (
    <button
      aria-label="Toggle Theme"
      onClick={() => setDark(!dark)}
      className="p-2 border rounded"
    >
      {dark ? '🌙' : '☀️'}
    </button>
  )
}
