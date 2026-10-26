"use client";

import ReactMarkdown from "react-markdown";
import { ArrowRight } from "lucide-react";
import { useMessages } from "@/lib/i18n/useMessages";

interface AboutProps {
  content: string;
  title?: string;
}
export default function About({ content, title }: AboutProps) {
  const messages = useMessages();
  return (
    <section>
      <h2 className="section-heading">{title || messages.home.about}</h2>
      <div className="about-copy">
        <ReactMarkdown
          components={{
            a: ({ children, href, ...props }) => (
              <a
                {...props}
                href={href}
                className="text-link"
                target={href?.startsWith("http") ? "_blank" : undefined}
                rel={
                  href?.startsWith("http") ? "noopener noreferrer" : undefined
                }
              >
                <span>{children}</span>
                <ArrowRight aria-hidden="true" />
              </a>
            ),
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    </section>
  );
}
