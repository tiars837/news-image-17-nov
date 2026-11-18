// news-image-20261117 — "World News: Tuesday, 17 November 2026"
// Copies the poster image held in this repository to the grader's output
// directory as /output/entry.png. The image is deterministic by
// construction: it is a fixed file in the repository, and copying it
// byte-for-byte can never differ between runs. No network is used.
import { copyFileSync, mkdirSync, readdirSync, rmSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = resolve(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

// The grader mounts /output as a volume: never remove the directory
// itself (that fails EBUSY). Create it, then clear only its contents.
mkdirSync(outDir, { recursive: true });
for (const child of readdirSync(outDir)) {
  rmSync(join(outDir, child), { recursive: true, force: true });
}

copyFileSync(source, join(outDir, "entry.png"));

// Fail loudly instead of silently shipping an empty or missing image.
const written = statSync(join(outDir, "entry.png"));
if (written.size === 0) {
  throw new Error("entry.png was written empty");
}
console.log(`wrote entry.png (${written.size} bytes)`);
