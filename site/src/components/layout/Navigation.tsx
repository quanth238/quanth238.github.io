"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import DownloadCV from "@/components/ui/DownloadCV";
import type { SiteConfig } from "@/lib/config";
import type { I18nRuntimeConfig } from "@/types/i18n";
import { cn } from "@/lib/utils";

interface NavigationProps {
  items: SiteConfig["navigation"];
  siteTitle: string;
  enableOnePageMode?: boolean;
  i18n: I18nRuntimeConfig;
  itemsByLocale?: Record<string, SiteConfig["navigation"]>;
  siteTitleByLocale?: Record<string, string>;
}

export default function Navigation({ items, siteTitle }: NavigationProps) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const active = (href: string) =>
    href === "/"
      ? pathname === "/"
      : pathname.startsWith(href.replace(/\/$/, ""));

  return (
    <nav
      aria-label="Main navigation"
      className="fixed inset-x-0 top-0 z-50 border-b border-neutral-200/60 bg-background/95 backdrop-blur-xl dark:border-neutral-700/50"
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-2 px-4 sm:px-6 lg:h-20 lg:px-8">
        <Link
          href="/"
          onClick={() => setOpen(false)}
          className="shrink-0 font-serif text-lg font-semibold text-primary transition-colors hover:text-accent sm:text-xl lg:text-2xl"
        >
          {siteTitle}
        </Link>
        <div className="flex items-center gap-1 sm:gap-3">
          <div className="mr-2 hidden items-center gap-1 md:flex">
            {items.map((item) => (
              <Link
                key={item.target}
                href={item.href}
                aria-current={active(item.href) ? "page" : undefined}
                className={cn(
                  "rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-accent/10 hover:text-primary",
                  active(item.href)
                    ? "bg-accent/10 text-primary"
                    : "text-neutral-600 dark:text-neutral-500",
                )}
              >
                {item.title}
              </Link>
            ))}
          </div>
          <DownloadCV compact />
          <ThemeToggle />
          <button
            type="button"
            onClick={() => setOpen(!open)}
            aria-label={open ? "Close main menu" : "Open main menu"}
            aria-expanded={open}
            aria-controls="mobile-navigation"
            className="rounded-lg p-2 text-primary hover:bg-accent/10 md:hidden"
          >
            {open ? (
              <XMarkIcon className="h-5 w-5" aria-hidden="true" />
            ) : (
              <Bars3Icon className="h-5 w-5" aria-hidden="true" />
            )}
          </button>
        </div>
      </div>
      {open && (
        <div
          id="mobile-navigation"
          className="space-y-1 border-t border-neutral-200/60 bg-background px-4 py-3 md:hidden"
        >
          {items.map((item) => (
            <Link
              key={item.target}
              href={item.href}
              onClick={() => setOpen(false)}
              aria-current={active(item.href) ? "page" : undefined}
              className={cn(
                "block rounded-lg px-3 py-2 text-sm font-medium text-primary",
                active(item.href) && "bg-accent/10",
              )}
            >
              {item.title}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
