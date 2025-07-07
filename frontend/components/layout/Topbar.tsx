"use client";
import { Bell, KeyRound, User } from "lucide-react";
import React from "react";

type Props = {
  userName?: string;
  apiKeyPresent?: boolean;
};

export default function Topbar({ userName, apiKeyPresent }: Props) {
  return (
    <header className="flex items-center justify-between p-4 border-b bg-background">
      <div className="text-lg font-semibold">Codex Booster</div>
      <div className="flex items-center gap-4">
        <span className="text-sm flex items-center gap-1">
          <KeyRound className="w-4 h-4" />
          {apiKeyPresent ? "API Key" : "No Key"}
        </span>
        <button className="relative p-1 rounded hover:bg-accent/20">
          <Bell className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-1">
          <User className="w-5 h-5" />
          <span className="text-sm">{userName || "Guest"}</span>
        </div>
      </div>
    </header>
  );
}
