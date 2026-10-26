"use client";

import { useEffect, useState } from "react";
import { Sun, Moon, Monitor } from "lucide-react";
import { useThemeStore, type Theme } from "@/lib/stores/themeStore";

export function ThemeToggle() {
  const { theme, setTheme } = useThemeStore();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const current = mounted ? theme : "light";
  const order: Theme[] = ["light", "dark", "system"];
  const next = order[(order.indexOf(current) + 1) % order.length];
  const label = current.charAt(0).toUpperCase() + current.slice(1);
  return (
    <button
      type="button"
      className="icon-button"
      onClick={() => setTheme(next)}
      title={"Current theme: " + label + ". Switch to " + next + "."}
      aria-label={"Change theme (current: " + label + ")"}
    >
      {current === "dark" ? (
        <Moon aria-hidden="true" />
      ) : current === "system" ? (
        <Monitor aria-hidden="true" />
      ) : (
        <Sun aria-hidden="true" />
      )}
    </button>
  );
}
