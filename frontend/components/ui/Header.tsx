"use client";
import { Menu, Settings } from "lucide-react";
import { motion } from "framer-motion";
import React from "react";

type Props = {
  onMenu?: () => void;
  onSettings?: () => void;
};

export default function Header({ onMenu, onSettings }: Props) {
  return (
    <header className="flex items-center justify-between p-4 border-b bg-white dark:bg-gray-900">
      <motion.button whileTap={{ scale: 0.9 }} onClick={onMenu}>
        <Menu className="w-5 h-5" />
      </motion.button>
      <h1 className="font-semibold text-lg">Audio Platform</h1>
      <motion.button whileTap={{ scale: 0.9 }} onClick={onSettings}>
        <Settings className="w-5 h-5" />
      </motion.button>
    </header>
  );
}
