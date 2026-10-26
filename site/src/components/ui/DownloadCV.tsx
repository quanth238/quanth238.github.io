import { ArrowDownTrayIcon } from "@heroicons/react/24/outline";
import { cn } from "@/lib/utils";

export default function DownloadCV({ compact = false }: { compact?: boolean }) {
  return (
    <a
      href="/files/quan-tran-hong-cv.pdf"
      download="Quan_Tran_Hong_CV.pdf"
      aria-label="Download CV (PDF)"
      title="Download CV (PDF)"
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-lg border border-accent/50 px-3 py-2 text-sm font-medium text-primary transition-colors hover:border-accent hover:bg-accent/10 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-accent",
        compact && "max-sm:p-2",
      )}
    >
      <ArrowDownTrayIcon className="h-4 w-4 shrink-0" aria-hidden="true" />
      <span className={compact ? "hidden sm:inline" : undefined}>
        Download CV
      </span>
    </a>
  );
}
