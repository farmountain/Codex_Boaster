"use client";
import { X } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import React from "react";

type Props = {
  open: boolean;
  onClose: () => void;
  children?: React.ReactNode;
};

export default function SettingsModal({ open, onClose, children }: Props) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0.9 }}
            className="bg-white dark:bg-gray-900 p-4 rounded w-80 relative"
          >
            <button className="absolute top-2 right-2" onClick={onClose}>
              <X className="w-4 h-4" />
            </button>
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
