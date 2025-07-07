"use client";
import { motion } from "framer-motion";
import { Send } from "lucide-react";
import React from "react";

type Props = {
  value: string;
  onChange: (v: string) => void;
  onSubmit?: () => void;
};

export default function PromptEditor({ value, onChange, onSubmit }: Props) {
  return (
    <div className="space-y-2">
      <textarea
        className="w-full p-2 border rounded dark:bg-gray-800"
        rows={4}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      {onSubmit && (
        <motion.button
          whileTap={{ scale: 0.95 }}
          className="px-3 py-1 bg-blue-600 text-white rounded flex items-center gap-1"
          onClick={onSubmit}
        >
          <Send className="w-4 h-4" /> Send
        </motion.button>
      )}
    </div>
  );
}
