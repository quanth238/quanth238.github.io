"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import DownloadCV from "@/components/ui/DownloadCV";
import type { SiteConfig } from "@/lib/config";
import type { I18nRuntimeConfig } from "@/types/i18n";

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
    <header
      className="site-header"
      onKeyDown={(event) => {
        if (event.key === "Escape") setOpen(false);
      }}
    >
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <div className="page-container header-inner">
        <Link href="/" onClick={() => setOpen(false)} className="site-brand">
          {siteTitle}
        </Link>
        <div className="header-actions">
          <nav className="desktop-navigation" aria-label="Main navigation">
            {items.map((item) => (
              <Link
                key={item.target}
                href={item.href}
                aria-current={active(item.href) ? "page" : undefined}
                className="navigation-link"
              >
                {item.title}
              </Link>
            ))}
          </nav>
          <DownloadCV compact />
          <ThemeToggle />
          <button
            type="button"
            className="icon-button menu-toggle"
            onClick={() => setOpen(!open)}
            aria-label={open ? "Close main menu" : "Open main menu"}
            aria-expanded={open}
            aria-controls="mobile-navigation"
          >
            {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
          </button>
        </div>
      </div>
      <nav
        id="mobile-navigation"
        aria-label="Mobile navigation"
        className="mobile-navigation"
        hidden={!open}
      >
        {items.map((item) => (
          <Link
            key={item.target}
            href={item.href}
            onClick={() => setOpen(false)}
            aria-current={active(item.href) ? "page" : undefined}
          >
            {item.title}
          </Link>
        ))}
      </nav>
    </header>
  );
}
