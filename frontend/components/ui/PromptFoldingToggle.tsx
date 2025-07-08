'use client'
import { useState } from 'react'
import { motion } from 'framer-motion'

export default function PromptFoldingToggle() {
  const [large, setLarge] = useState(true)
  return (
    <motion.button
      whileTap={{ scale: 0.95 }}
      onClick={() => setLarge(!large)}
      className="px-3 py-1 border rounded bg-white dark:bg-gray-800"
    >
      {large ? 'Large Model' : 'Small Model'}
    </motion.button>
  )
}
