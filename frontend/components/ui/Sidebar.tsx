"use client";
import { motion } from "framer-motion";
import { Home, PieChart, Settings, User } from "lucide-react";
import React from "react";

const items = [
  { icon: Home, label: "Home" },
  { icon: PieChart, label: "Analytics" },
  { icon: User, label: "Agents" },
  { icon: Settings, label: "Settings" },
];

type Props = {
  onSelect?: (label: string) => void;
};

export default function Sidebar({ onSelect }: Props) {
  return (
    <aside className="w-48 border-r p-4 space-y-2 bg-white dark:bg-gray-900">
      {items.map(({ icon: Icon, label }) => (
        <motion.button
          key={label}
          whileHover={{ scale: 1.03 }}
          className="flex items-center gap-2 w-full p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
          onClick={() => onSelect && onSelect(label)}
        >
          <Icon className="w-4 h-4" />
          <span>{label}</span>
        </motion.button>
      ))}
    </aside>
  );
}
