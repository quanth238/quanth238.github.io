"use client";

import { useLocaleStore } from "@/lib/stores/localeStore";
import { useMessages } from "@/lib/i18n/useMessages";

interface FooterProps {
  lastUpdated?: string;
  lastUpdatedByLocale?: Record<string, string | undefined>;
  defaultLocale?: string;
}

export default function Footer({
  lastUpdated,
  lastUpdatedByLocale,
  defaultLocale = "en",
}: FooterProps) {
  const locale = useLocaleStore((state) => state.locale);
  const messages = useMessages();

  const resolvedLastUpdated =
    lastUpdatedByLocale?.[locale] ||
    (defaultLocale ? lastUpdatedByLocale?.[defaultLocale] : undefined) ||
    lastUpdated ||
    new Date().toLocaleDateString(locale || "en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });

  return (
    <footer className="site-footer">
      <div className="page-container footer-inner">
        <p>
          {messages.footer.lastUpdated}: {resolvedLastUpdated}
        </p>
        <a
          href="https://github.com/xyjoey/PRISM"
          target="_blank"
          rel="noopener noreferrer"
        >
          {messages.footer.builtWithPrism}
        </a>
      </div>
    </footer>
  );
}
