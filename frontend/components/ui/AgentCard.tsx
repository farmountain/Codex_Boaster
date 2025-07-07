"use client";
import { Bot } from "lucide-react";
import { motion } from "framer-motion";
import React from "react";

type Props = {
  name: string;
  status?: string;
  onClick?: () => void;
};

export default function AgentCard({ name, status, onClick }: Props) {
  return (
    <motion.div
      onClick={onClick}
      whileHover={{ scale: 1.05 }}
      className="p-4 border rounded cursor-pointer flex items-center gap-2 hover:bg-gray-50 dark:hover:bg-gray-700"
    >
      <Bot className="w-5 h-5 text-primary" />
      <div className="flex-1">
        <h3 className="font-semibold">{name}</h3>
        {status && (
          <p className="text-sm text-gray-500 dark:text-gray-400">{status}</p>
        )}
      </div>
    </motion.div>
  );
}
