"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Brain, Hammer, BugPlay, Home } from "lucide-react";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: Home },
  { href: "/plan", label: "Plan", icon: Brain },
  { href: "/build", label: "Build", icon: Hammer },
  { href: "/test", label: "Test", icon: BugPlay },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 bg-background border-r p-4 space-y-2">
      {items.map(({ href, label, icon: Icon }) => (
        <Link
          key={href}
          href={href}
          className={`flex items-center gap-2 p-2 rounded hover:bg-accent/20 ${pathname === href ? "bg-accent text-white" : ""}`}
        >
          <Icon className="w-4 h-4" />
          <span>{label}</span>
        </Link>
      ))}
    </aside>
  );
}
