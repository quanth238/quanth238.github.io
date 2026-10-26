"use client";

import Image from "next/image";
import { Mail, GraduationCap, MapPin, Github, Linkedin } from "lucide-react";
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
      href: social.email ? "mailto:" + social.email : undefined,
      icon: Mail,
    },
    {
      name: "Google Scholar",
      href: social.google_scholar,
      icon: GraduationCap,
    },
    { name: "GitHub", href: social.github, icon: Github },
    { name: "LinkedIn", href: social.linkedin, icon: Linkedin },
  ];
  return (
    <aside className="profile" aria-label="Researcher profile">
      <div className="profile-content">
        <Image
          className="profile-photo"
          src={author.avatar}
          alt={author.name}
          width={300}
          height={300}
          sizes="(max-width: 479px) 112px, (max-width: 959px) 144px, 248px"
          priority
        />
        <div className="profile-summary">
          <h1 className="profile-name">{author.name}</h1>
          <p className="profile-role">{author.title}</p>
          <p className="profile-institution">{author.institution}</p>
          {social.location && (
            <p className="profile-location">
              <MapPin aria-hidden="true" />
              {social.location}
            </p>
          )}
          <div className="profile-social">
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
                >
                  <Icon aria-hidden="true" />
                </a>
              ))}
          </div>
        </div>
      </div>
      {researchInterests && researchInterests.length > 0 && (
        <section
          className="profile-interests"
          aria-labelledby="research-interests-heading"
        >
          <h2 id="research-interests-heading">Research Interests</h2>
          <ul className="interest-list">
            {researchInterests.map((interest) => (
              <li key={interest}>{interest}</li>
            ))}
          </ul>
        </section>
      )}
    </aside>
  );
}
