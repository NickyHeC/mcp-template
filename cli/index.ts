#!/usr/bin/env node

import prompts from "prompts";
import pc from "picocolors";
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

type AuthType = "no-auth" | "api-key" | "oauth";
type PackageManager = "uv" | "pip";

interface Config {
  projectName: string;
  authType: AuthType;
  packageManager: PackageManager;
}

const AUTH_CHOICES: { value: AuthType; title: string; description: string }[] = [
  {
    value: "no-auth",
    title: "No Auth",
    description: "Self-contained tools, no credentials needed",
  },
  {
    value: "api-key",
    title: "API Key",
    description: "Static credential via DAuth (GitHub, Slack, Discord)",
  },
  {
    value: "oauth",
    title: "OAuth",
    description: "Browser-based auth via DAuth (Gmail, Linear, Spotify)",
  },
];

const AUTH_LABELS: Record<AuthType, string> = {
  "no-auth": "No Auth",
  "api-key": "API Key",
  oauth: "OAuth",
};

function toSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9-]/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

async function getConfig(): Promise<Config | null> {
  const argName = process.argv[2];

  const response = await prompts(
    [
      {
        type: argName ? null : "text",
        name: "projectName",
        message: "Project name:",
        initial: "my-mcp-server",
        validate: (v: string) =>
          v.trim().length > 0 || "Project name is required",
      },
      {
        type: "select",
        name: "authType",
        message: "Auth type:",
        choices: AUTH_CHOICES.map(({ value, title, description }) => ({
          title: `${title} ${pc.dim(`— ${description}`)}`,
          value,
        })),
      },
      {
        type: "select",
        name: "packageManager",
        message: "Package manager:",
        choices: [
          { title: "uv", value: "uv", description: "Fast Python package manager" },
          { title: "pip", value: "pip" },
        ],
      },
    ],
    {
      onCancel: () => {
        console.log(pc.red("\n  Cancelled.\n"));
        process.exit(0);
      },
    },
  );

  return {
    projectName: argName || response.projectName,
    authType: response.authType,
    packageManager: response.packageManager,
  };
}

function copyTemplate(
  src: string,
  dest: string,
  replacements: [string, string][],
) {
  fs.mkdirSync(dest, { recursive: true });

  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyTemplate(srcPath, destPath, replacements);
    } else {
      let content = fs.readFileSync(srcPath, "utf-8");
      for (const [from, to] of replacements) {
        content = content.replaceAll(from, to);
      }
      fs.writeFileSync(destPath, content);
    }
  }
}

function installDeps(config: Config, projectDir: string) {
  const { packageManager } = config;
  console.log(pc.dim(`  Installing dependencies with ${packageManager}...`));

  try {
    if (packageManager === "uv") {
      execSync("uv sync", { cwd: projectDir, stdio: "inherit" });
    } else {
      execSync("pip install -e .", { cwd: projectDir, stdio: "inherit" });
    }
  } catch {
    console.log(pc.yellow(`\n  Could not auto-install. Run it manually.`));
  }
}

async function main() {
  console.log();
  console.log(pc.bold("  create-dmcp"));
  console.log(pc.dim("  Scaffold a Dedalus MCP server"));
  console.log();

  const config = await getConfig();
  if (!config) return;

  const { projectName, authType, packageManager } = config;
  const slug = toSlug(projectName);

  const templateDir = path.join(ROOT, `src-${authType}`);
  if (!fs.existsSync(templateDir)) {
    console.log(pc.red(`\n  Template not found: src-${authType}\n`));
    process.exit(1);
  }

  const projectDir = path.resolve(process.cwd(), projectName);
  if (fs.existsSync(projectDir)) {
    console.log(pc.red(`\n  Directory already exists: ${projectName}\n`));
    process.exit(1);
  }

  console.log();
  console.log(`  ${pc.bold("Creating")} ${pc.cyan(projectName)}`);
  console.log(`  ${pc.dim("Auth:")}    ${AUTH_LABELS[authType]}`);
  console.log(`  ${pc.dim("Package:")} ${packageManager}`);
  console.log();

  const replacements: [string, string][] = [
    ['name="my-mcp"', `name="${slug}"`],
    ['name = "mcp-template"', `name = "${projectName}"`],
  ];

  // Copy template → project/src/
  const srcDir = path.join(projectDir, "src");
  copyTemplate(templateDir, srcDir, replacements);

  // Copy shared files
  const pyprojectSrc = path.join(ROOT, "pyproject.toml");
  let pyproject = fs.readFileSync(pyprojectSrc, "utf-8");
  pyproject = pyproject.replaceAll("mcp-template", projectName);
  fs.writeFileSync(path.join(projectDir, "pyproject.toml"), pyproject);

  const sharedFiles = [".env.example", "PROJECT.md", "LICENSE"];
  for (const file of sharedFiles) {
    const filePath = path.join(ROOT, file);
    if (fs.existsSync(filePath)) {
      fs.copyFileSync(filePath, path.join(projectDir, file));
    }
  }

  // Write .gitignore (the template's .gitignore is in the repo root but
  // npm strips dotfiles from published packages, so we generate it)
  fs.writeFileSync(
    path.join(projectDir, ".gitignore"),
    [
      "__pycache__/",
      "*.py[codz]",
      ".env",
      ".venv/",
      "venv/",
      "dist/",
      "*.egg-info/",
      ".mypy_cache/",
      ".ruff_cache/",
      "",
    ].join("\n"),
  );

  installDeps(config, projectDir);

  console.log();
  console.log(pc.green("  Done! ") + "Your MCP server is ready.");
  console.log();
  console.log(`  ${pc.bold("Next steps:")}`);
  console.log(`  ${pc.dim("$")} cd ${projectName}`);
  if (authType !== "no-auth") {
    console.log(`  ${pc.dim("$")} cp .env.example .env  ${pc.dim("# add your keys")}`);
  }
  console.log(`  ${pc.dim("$")} python -m src.main`);
  console.log();
  console.log(`  ${pc.dim("Test with:")} python -m src.client`);
  console.log(`  ${pc.dim("Docs:")} https://docs.dedaluslabs.ai/dmcp`);
  console.log(`  ${pc.dim("Deploy:")} https://dedaluslabs.ai/dashboard`);
  console.log();
}

main().catch((err) => {
  console.error(pc.red(`\n  Error: ${err}\n`));
  process.exit(1);
});
