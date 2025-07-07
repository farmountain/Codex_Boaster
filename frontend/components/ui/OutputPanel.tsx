"use client";
import { motion } from "framer-motion";
import React from "react";

type Props = {
  title: string;
  content: string;
};

export default function OutputPanel({ title, content }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-4 border rounded bg-white dark:bg-gray-800"
    >
      <h3 className="font-semibold mb-2">{title}</h3>
      <pre className="whitespace-pre-wrap text-sm">{content}</pre>
    </motion.div>
  );
}
