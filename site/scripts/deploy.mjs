import { execFileSync } from "node:child_process";
import {
  cpSync,
  existsSync,
  mkdtempSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const git = (args, cwd = root) =>
  execFileSync("git", args, { cwd, encoding: "utf8" }).trim();

execFileSync("npm", ["run", "typecheck"], { cwd: root, stdio: "inherit" });
execFileSync("npm", ["run", "build"], { cwd: root, stdio: "inherit" });
if (!existsSync(join(root, "out/index.html")))
  throw new Error("Static build is missing.");

const remote = git(["remote", "get-url", "origin"]);
if (
  !/github\.com[:/]quanth238\/quanth238\.github\.io(?:\.git)?$/.test(remote)
) {
  throw new Error("Refusing to deploy to an unexpected repository.");
}
const name = git(["config", "user.name"]);
const email = git(["config", "user.email"]);
const checkout = mkdtempSync(join(root, ".deploy-"));

try {
  execFileSync(
    "git",
    [
      "clone",
      "--branch",
      "gh-pages",
      "--single-branch",
      "--depth",
      "1",
      remote,
      checkout,
    ],
    { stdio: "inherit" },
  );
  for (const item of readdirSync(checkout)) {
    if (item !== ".git")
      rmSync(join(checkout, item), { recursive: true, force: true });
  }
  for (const item of readdirSync(join(root, "out"))) {
    cpSync(join(root, "out", item), join(checkout, item), { recursive: true });
  }
  writeFileSync(join(checkout, ".nojekyll"), "");
  git(["config", "user.name", name], checkout);
  git(["config", "user.email", email], checkout);
  git(["add", "--all"], checkout);
  if (git(["status", "--porcelain"], checkout)) {
    git(["commit", "-m", "feat: publish PRISM portfolio"], checkout);
    execFileSync("git", ["push", "origin", "HEAD:gh-pages"], {
      cwd: checkout,
      stdio: "inherit",
    });
  } else {
    console.log("The current build is already published.");
  }
  console.log(
    "Published build to gh-pages. GitHub Pages will serve it at https://quanth238.github.io/ after its deployment completes.",
  );
} finally {
  rmSync(checkout, { recursive: true, force: true });
}
