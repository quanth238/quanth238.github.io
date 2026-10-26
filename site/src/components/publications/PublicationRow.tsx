"use client";

import { useState } from "react";
import Image from "next/image";
import {
  ArrowUpRight,
  BookOpen,
  Check,
  Copy,
  FileText,
  Github,
} from "lucide-react";
import type { Publication } from "@/types/publication";
import FormattedBibTeXText from "./FormattedBibTeXText";

interface PublicationRowProps {
  publication: Publication;
  detailed?: boolean;
}

function venueLabel(publication: Publication): string {
  const venue =
    publication.journal || publication.conference || publication.type;
  const abbreviation = venue.match(/\(([^)]+)\)/)?.[1] || venue;
  const poster = /poster/i.test(publication.description || "")
    ? " · Poster"
    : "";
  return abbreviation + " " + publication.year + poster;
}

export default function PublicationRow({
  publication: pub,
  detailed = false,
}: PublicationRowProps) {
  const [expanded, setExpanded] = useState<"bibtex" | "abstract" | null>(null);
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "error">(
    "idle",
  );
  const title = (
    <FormattedBibTeXText nodes={pub.titleNodes} fallback={pub.title} />
  );
  const toggle = (panel: "bibtex" | "abstract") =>
    setExpanded(expanded === panel ? null : panel);
  return (
    <article className="publication-row">
      {pub.preview && (
        <a
          href={pub.url || "/papers/" + pub.preview}
          target="_blank"
          rel="noopener noreferrer"
          className="publication-thumbnail"
          aria-label={"View paper: " + pub.title}
        >
          <Image
            src={"/papers/" + pub.preview}
            alt={"Method overview for " + pub.title}
            width={440}
            height={232}
            sizes="(max-width: 600px) 360px, (max-width: 959px) 200px, (max-width: 1100px) 172px, 220px"
          />
        </a>
      )}
      <div className="publication-content">
        <p className="publication-venue" title={pub.journal || pub.conference}>
          {venueLabel(pub)}
        </p>
        <h3 className="publication-title">
          {pub.url ? (
            <a href={pub.url} target="_blank" rel="noopener noreferrer">
              {title}
            </a>
          ) : (
            title
          )}
        </h3>
        <p className="publication-authors">
          {pub.authors.map((author, index) => (
            <span key={author.name}>
              <span className={author.isHighlighted ? "owner" : undefined}>
                {author.name}
                {(author.isCoAuthor || author.isCorresponding) && <sup>†</sup>}
              </span>
              {index < pub.authors.length - 1 && ", "}
            </span>
          ))}
        </p>
        {detailed && pub.description && (
          <p className="publication-description">{pub.description}</p>
        )}
        <div className="publication-links">
          {pub.url && (
            <a href={pub.url} target="_blank" rel="noopener noreferrer">
              <FileText aria-hidden="true" />
              Paper
              <ArrowUpRight className="external-arrow" aria-hidden="true" />
            </a>
          )}
          {pub.code && (
            <a href={pub.code} target="_blank" rel="noopener noreferrer">
              <Github aria-hidden="true" />
              Code
              <ArrowUpRight className="external-arrow" aria-hidden="true" />
            </a>
          )}
          {pub.doi && (
            <a
              href={"https://doi.org/" + pub.doi}
              target="_blank"
              rel="noopener noreferrer"
            >
              DOI
              <ArrowUpRight className="external-arrow" aria-hidden="true" />
            </a>
          )}
          {detailed && pub.abstract && (
            <button
              type="button"
              aria-expanded={expanded === "abstract"}
              aria-controls={pub.id + "-abstract"}
              onClick={() => toggle("abstract")}
            >
              <FileText aria-hidden="true" />
              Abstract
            </button>
          )}
          {detailed && pub.bibtex && (
            <button
              type="button"
              aria-expanded={expanded === "bibtex"}
              aria-controls={pub.id + "-bibtex"}
              onClick={() => toggle("bibtex")}
            >
              <BookOpen aria-hidden="true" />
              BibTeX
            </button>
          )}
        </div>
        {expanded === "abstract" && pub.abstract && (
          <div className="citation-panel" id={pub.id + "-abstract"}>
            <p className="publication-description">{pub.abstract}</p>
          </div>
        )}
        {expanded === "bibtex" && pub.bibtex && (
          <div className="citation-panel" id={pub.id + "-bibtex"}>
            <pre>{pub.bibtex}</pre>
            <button
              type="button"
              className="citation-copy"
              aria-live="polite"
              onClick={async () => {
                try {
                  await navigator.clipboard.writeText(pub.bibtex || "");
                  setCopyStatus("copied");
                } catch {
                  setCopyStatus("error");
                }
              }}
            >
              {copyStatus === "copied" ? (
                <Check aria-hidden="true" />
              ) : (
                <Copy aria-hidden="true" />
              )}
              {copyStatus === "copied"
                ? "Copied"
                : copyStatus === "error"
                  ? "Copy unavailable — select the citation above"
                  : "Copy citation"}
            </button>
          </div>
        )}
      </div>
    </article>
  );
}
