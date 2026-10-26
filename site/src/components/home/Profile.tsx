"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import {
  EnvelopeIcon,
  AcademicCapIcon,
  MapPinIcon,
} from "@heroicons/react/24/outline";
import { Github, Linkedin } from "lucide-react";
import type { SiteConfig } from "@/lib/config";

interface ProfileProps {
  author: SiteConfig["author"];
  social: SiteConfig["social"];
  features: SiteConfig["features"];
  researchInterests?: string[];
}

export default function Profile({
  author,
  social,
  researchInterests,
}: ProfileProps) {
  const links = [
    {
      name: "Email",
      href: social.email ? `mailto:${social.email}` : undefined,
      icon: EnvelopeIcon,
    },
    {
      name: "Google Scholar",
      href: social.google_scholar,
      icon: AcademicCapIcon,
    },
    { name: "GitHub", href: social.github, icon: Github },
    { name: "LinkedIn", href: social.linkedin, icon: Linkedin },
  ];
  return (
    <motion.aside
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="lg:sticky lg:top-28"
    >
      <div className="mx-auto mb-6 h-64 w-64 overflow-hidden rounded-2xl shadow-lg">
        <Image
          src={author.avatar}
          alt={author.name}
          width={256}
          height={256}
          className="h-full w-full object-cover"
          priority
        />
      </div>
      <div className="mb-4 text-center">
        <h1 className="mb-2 font-serif text-3xl font-bold text-primary">
          {author.name}
        </h1>
        <p className="mb-1 text-base font-medium text-accent">{author.title}</p>
        <p className="text-neutral-600 dark:text-neutral-500">
          {author.institution}
        </p>
        {social.location && (
          <p className="mt-2 inline-flex items-center gap-1 text-sm text-neutral-500">
            <MapPinIcon className="h-4 w-4" aria-hidden="true" />
            {social.location}
          </p>
        )}
      </div>
      <div className="mb-5 flex justify-center gap-3">
        {links
          .filter((link) => link.href)
          .map(({ name, href, icon: Icon }) => (
            <a
              key={name}
              href={href}
              aria-label={name}
              title={name}
              target={name === "Email" ? undefined : "_blank"}
              rel={name === "Email" ? undefined : "noopener noreferrer"}
              className="rounded-md p-2 text-neutral-600 transition-colors hover:text-accent dark:text-neutral-500"
            >
              <Icon className="h-5 w-5" aria-hidden="true" />
            </a>
          ))}
      </div>
      {researchInterests && (
        <div className="rounded-lg border border-neutral-200 bg-neutral-50 p-5 dark:border-neutral-700/50 dark:bg-neutral-800">
          <h2 className="mb-3 font-semibold text-primary">
            Research Interests
          </h2>
          <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-500">
            {researchInterests.map((interest) => (
              <li key={interest}>{interest}</li>
            ))}
          </ul>
        </div>
      )}
    </motion.aside>
  );
}
