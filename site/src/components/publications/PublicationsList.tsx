"use client";

import { useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";
import type { Publication } from "@/types/publication";
import type { PublicationPageConfig } from "@/types/page";
import PublicationRow from "./PublicationRow";

interface PublicationsListProps {
  config: PublicationPageConfig;
  publications: Publication[];
  embedded?: boolean;
}
export default function PublicationsList({
  config,
  publications,
  embedded = false,
}: PublicationsListProps) {
  const [query, setQuery] = useState("");
  const [year, setYear] = useState<number | "all">("all");
  const [type, setType] = useState("all");
  const [showFilters, setShowFilters] = useState(false);
  const years = useMemo(
    () =>
      [...new Set(publications.map((pub) => pub.year))].sort((a, b) => b - a),
    [publications],
  );
  const types = useMemo(
    () => [...new Set(publications.map((pub) => pub.type))].sort(),
    [publications],
  );
  const filtered = useMemo(() => {
    const search = query.trim().toLowerCase();
    return publications.filter((pub) => {
      const text = [
        pub.title,
        pub.conference,
        pub.journal,
        pub.description,
        ...pub.authors.map((author) => author.name),
      ]
        .join(" ")
        .toLowerCase();
      return (
        text.includes(search) &&
        (year === "all" || pub.year === year) &&
        (type === "all" || pub.type === type)
      );
    });
  }, [publications, query, year, type]);
  const Heading = embedded ? "h2" : "h1";
  return (
    <section>
      <Heading className={embedded ? "section-heading" : "page-heading"}>
        {config.title}
      </Heading>
      {config.description && (
        <p className="page-description">{config.description}</p>
      )}
      <div className="publication-toolbar">
        <label className="publication-search">
          <Search aria-hidden="true" />
          <input
            type="search"
            aria-label="Search publications"
            placeholder="Search titles, authors, or venues…"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </label>
        <button
          type="button"
          className="filter-toggle"
          aria-expanded={showFilters}
          aria-controls="publication-filters"
          onClick={() => setShowFilters(!showFilters)}
        >
          <SlidersHorizontal aria-hidden="true" />
          Filters
        </button>
      </div>
      <div
        id="publication-filters"
        className="publication-filters"
        hidden={!showFilters}
      >
        <fieldset>
          <legend>Year</legend>
          <div className="filter-options">
            <button
              type="button"
              aria-pressed={year === "all"}
              onClick={() => setYear("all")}
            >
              All
            </button>
            {years.map((value) => (
              <button
                type="button"
                key={value}
                aria-pressed={year === value}
                onClick={() => setYear(value)}
              >
                {value}
              </button>
            ))}
          </div>
        </fieldset>
        <fieldset>
          <legend>Type</legend>
          <div className="filter-options">
            <button
              type="button"
              aria-pressed={type === "all"}
              onClick={() => setType("all")}
            >
              All
            </button>
            {types.map((value) => (
              <button
                type="button"
                key={value}
                aria-pressed={type === value}
                onClick={() => setType(value)}
              >
                {value.replaceAll("-", " ")}
              </button>
            ))}
          </div>
        </fieldset>
      </div>
      <p className="results-count" role="status">
        {filtered.length}{" "}
        {filtered.length === 1 ? "publication" : "publications"}
      </p>
      <div className="publication-list">
        {filtered.length ? (
          filtered.map((pub) => (
            <PublicationRow key={pub.id} publication={pub} detailed />
          ))
        ) : (
          <p className="empty-results">No publications match your search.</p>
        )}
      </div>
      {filtered.some((pub) =>
        pub.authors.some((author) => author.isCoAuthor),
      ) && <p className="contribution-note">† Equal contribution.</p>}
    </section>
  );
}
