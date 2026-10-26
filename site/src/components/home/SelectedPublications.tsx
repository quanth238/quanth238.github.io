"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Publication } from "@/types/publication";
import PublicationRow from "@/components/publications/PublicationRow";
import { useMessages } from "@/lib/i18n/useMessages";

interface SelectedPublicationsProps {
  publications: Publication[];
  title?: string;
  enableOnePageMode?: boolean;
}
export default function SelectedPublications({
  publications,
  title,
  enableOnePageMode = false,
}: SelectedPublicationsProps) {
  const messages = useMessages();
  return (
    <section
      className="selected-publications"
      aria-labelledby="selected-publications-heading"
    >
      <div className="section-header">
        <h2 id="selected-publications-heading" className="section-heading">
          {title || messages.home.selectedPublications}
        </h2>
        <Link
          href={enableOnePageMode ? "/#publications" : "/publications/"}
          className="text-link"
        >
          <span>View all</span>
          <ArrowRight aria-hidden="true" />
        </Link>
      </div>
      <div className="publication-list">
        {publications.map((pub) => (
          <PublicationRow key={pub.id} publication={pub} />
        ))}
      </div>
      {publications.some((pub) =>
        pub.authors.some((author) => author.isCoAuthor),
      ) && <p className="contribution-note">† Equal contribution.</p>}
    </section>
  );
}
