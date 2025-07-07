"use client";
import { Play, Pause } from "lucide-react";
import { motion } from "framer-motion";
import React, { useRef, useState } from "react";

type Props = {
  src: string;
};

export default function AudioPlayer({ src }: Props) {
  const ref = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);

  const toggle = () => {
    const el = ref.current;
    if (!el) return;
    if (playing) {
      el.pause();
    } else {
      el.play();
    }
    setPlaying(!playing);
  };

  return (
    <div className="flex items-center gap-2">
      <motion.button whileTap={{ scale: 0.9 }} onClick={toggle}>
        {playing ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
      </motion.button>
      <audio ref={ref} src={src} className="hidden" />
    </div>
  );
}
