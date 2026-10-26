import { Download } from "lucide-react";

export default function DownloadCV({ compact = false }: { compact?: boolean }) {
  return (
    <a
      href="/files/quan-tran-hong-cv.pdf"
      download="Quan_Tran_Hong_CV.pdf"
      aria-label="Download CV (PDF)"
      title="Download CV (PDF)"
      className={"cv-download" + (compact ? " compact" : "")}
    >
      <Download aria-hidden="true" />
      <span>Download CV</span>
    </a>
  );
}
