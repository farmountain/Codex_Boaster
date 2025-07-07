"use client";
import { LineChart } from "lucide-react";
import { motion } from "framer-motion";
import React from "react";

type Props = {
  data?: string;
};

export default function AnalyticsPanel({ data }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-4 border rounded bg-white dark:bg-gray-800"
    >
      <h3 className="font-semibold mb-2 flex items-center gap-1">
        <LineChart className="w-4 h-4" /> Analytics
      </h3>
      <pre className="text-sm whitespace-pre-wrap">{data}</pre>
    </motion.div>
  );
}
