#!/usr/bin/env python3
"""Report broken relative Markdown links (fenced code blocks and inline code are ignored).

Usage: python3 check_links.py [PATH ...]   (default: current directory)
Exit code 1 if any link is broken.
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

LINK = re.compile(r"\]\(<?([^)#\s>]+)>?(?:\s+\"[^\"]*\")?(#[^)]*)?\)")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
INLINE = re.compile(r"`[^`\n]*`")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv"}


def files(targets):
    for t in targets:
        p = Path(t)
        if p.is_file() and p.suffix == ".md":
            yield p
        elif p.is_dir():
            yield from (f for f in p.rglob("*.md") if not SKIP_DIRS & set(f.parts))
        else:
            print(f"warning: {t} is not a Markdown file or folder", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", default=["."], help="files or folders to check")
    args = ap.parse_args()
    broken = 0
    for f in files(args.paths):
        text = INLINE.sub("", FENCE.sub("", f.read_text(encoding="utf-8")))
        for m in LINK.finditer(text):
            target = m.group(1)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            if not (f.parent / unquote(target)).resolve().exists():
                broken += 1
                print(f"{f}: -> {target}")
    print(f"Broken links: {broken}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
