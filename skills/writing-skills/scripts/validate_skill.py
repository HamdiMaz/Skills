#!/usr/bin/env python3
"""Validate a Pi agent skill directory.

Checks:
- SKILL.md exists and has frontmatter
- required name/description fields
- name format and parent directory match
- description length and basic quality
- TODO/placeholders
- broken relative Markdown links
- oversized SKILL.md
- scripts have executable bits when they have shebangs
- optional script syntax checks for Python and Node scripts
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAX_NAME = 64
MAX_DESCRIPTION = 1024
WARN_SKILL_LINES = 500
WARN_SKILL_WORDS = 3000
ALLOWED_NAME = re.compile(r"^[a-z0-9-]+$")
TODO_PATTERNS = ["TODO:", "FIXME", "TBD", "[TODO", "<TODO", "PLACEHOLDER"]
LINK_RE = re.compile(r"(?<!!)(?:\[[^\]]*\]\(([^)]+)\))")
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
    "disable-model-invocation",
}


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


def extract_frontmatter(text: str) -> tuple[str | None, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :])
    return None, text


def parse_simple_frontmatter(frontmatter: str) -> dict[str, str]:
    data: dict[str, str] = {}
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if raw[0].isspace():
            i += 1
            continue
        if ":" not in raw:
            data[f"__invalid_line_{i}"] = raw
            i += 1
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {"|", ">", "|-", ">-"}:
            block: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(block).strip()
            continue
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            value = value[1:-1]
        data[key] = value
        i += 1
    return data


def is_relative_link(target: str) -> bool:
    target = target.strip()
    if not target or target.startswith("#"):
        return False
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return False
    return True


def check_links(skill_dir: Path, path: Path, text: str, result: Result) -> None:
    for match in LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        target = raw_target.split("#", 1)[0].strip()
        if not is_relative_link(target):
            continue
        if target.startswith("<") or target.endswith(">"):
            result.error(f"{path.relative_to(skill_dir)} contains placeholder link: {raw_target}")
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(skill_dir.resolve())
        except ValueError:
            result.error(f"{path.relative_to(skill_dir)} links outside skill directory: {raw_target}")
            continue
        if not resolved.exists():
            result.error(f"{path.relative_to(skill_dir)} has broken relative link: {raw_target}")


def check_todos(skill_dir: Path, path: Path, text: str, result: Result) -> None:
    for token in TODO_PATTERNS:
        if token in text:
            result.error(f"{path.relative_to(skill_dir)} contains placeholder token: {token}")
            return


def check_frontmatter(skill_dir: Path, result: Result) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        result.error("SKILL.md not found")
        return

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    frontmatter, body = extract_frontmatter(text)
    if frontmatter is None:
        result.error("SKILL.md must start with YAML frontmatter fenced by ---")
        return

    data = parse_simple_frontmatter(frontmatter)
    invalid = [k for k in data if k.startswith("__invalid_line_")]
    if invalid:
        result.error("Frontmatter contains invalid YAML-like lines")

    unknown = sorted(set(data) - ALLOWED_FRONTMATTER - set(invalid))
    if unknown:
        result.warn("Unknown frontmatter field(s) ignored by Pi/spec: " + ", ".join(unknown))

    name = data.get("name", "").strip()
    description = data.get("description", "").strip()

    if not name:
        result.error("Missing frontmatter field: name")
    else:
        if len(name) > MAX_NAME:
            result.error(f"name is too long ({len(name)} > {MAX_NAME})")
        if not ALLOWED_NAME.match(name):
            result.error("name must use lowercase letters, digits, and hyphens only")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            result.error("name cannot start/end with hyphen or contain consecutive hyphens")
        if name != skill_dir.name:
            result.error(f"name '{name}' must match parent directory '{skill_dir.name}'")

    if not description:
        result.error("Missing frontmatter field: description")
    else:
        if len(description) > MAX_DESCRIPTION:
            result.error(f"description is too long ({len(description)} > {MAX_DESCRIPTION})")
        if "workflow" in description.lower() and any(
            word in description.lower() for word in ["baseline", "draft", "refactor", "subagent"]
        ):
            result.warn("description may summarize internal workflow; prefer what+when trigger conditions")
        if "use when" not in description.lower() and "when" not in description.lower():
            result.warn("description should include trigger conditions, e.g. 'Use when ...'")

    line_count = len(text.splitlines())
    word_count = len(re.findall(r"\w+", body))
    if line_count > WARN_SKILL_LINES:
        result.warn(f"SKILL.md is long ({line_count} lines); consider one-level references")
    if word_count > WARN_SKILL_WORDS:
        result.warn(f"SKILL.md is verbose ({word_count} body words); consider progressive disclosure")

    check_todos(skill_dir, skill_md, text, result)
    check_links(skill_dir, skill_md, text, result)


def iter_files(skill_dir: Path):
    skip_dirs = {".git", "node_modules", "__pycache__", ".pytest_cache"}
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for name in files:
            yield Path(root) / name


def check_all_markdown(skill_dir: Path, result: Result) -> None:
    for path in iter_files(skill_dir):
        if path.name == "SKILL.md":
            continue
        if path.suffix.lower() in {".md", ".txt"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            check_todos(skill_dir, path, text, result)
            if path.suffix.lower() == ".md":
                check_links(skill_dir, path, text, result)


def check_scripts(skill_dir: Path, result: Result, check_syntax: bool) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return
    for path in scripts_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        except OSError:
            result.error(f"Could not read script: {path.relative_to(skill_dir)}")
            continue
        has_shebang = bool(first and first[0].startswith("#!"))
        if has_shebang and not os.access(path, os.X_OK):
            result.error(f"Script has shebang but is not executable: {path.relative_to(skill_dir)}")
        if not check_syntax:
            continue
        rel = path.relative_to(skill_dir)
        if path.suffix == ".py":
            proc = subprocess.run([sys.executable, "-m", "py_compile", str(path)], capture_output=True, text=True)
            if proc.returncode != 0:
                result.error(f"Python syntax check failed for {rel}: {proc.stderr.strip()}")
        elif path.suffix in {".js", ".cjs", ".mjs"} and shutil.which("node"):
            proc = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
            if proc.returncode != 0:
                result.error(f"Node syntax check failed for {rel}: {proc.stderr.strip()}")


def validate(skill_dir: Path, check_syntax: bool) -> Result:
    result = Result()
    if not skill_dir.exists() or not skill_dir.is_dir():
        result.error(f"Not a directory: {skill_dir}")
        return result
    check_frontmatter(skill_dir, result)
    check_all_markdown(skill_dir, result)
    check_scripts(skill_dir, result, check_syntax)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Pi agent skill directory")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument("--check-scripts", action="store_true", help="Syntax-check Python/Node scripts when possible")
    args = parser.parse_args()

    skill_dir = Path(args.skill_path).resolve()
    result = validate(skill_dir, args.check_scripts)

    if result.ok:
        print(f"OK: {skill_dir} passed validation")
    else:
        print(f"FAIL: {skill_dir} has {len(result.errors)} error(s)")

    for msg in result.errors:
        print(f"ERROR: {msg}")
    for msg in result.warnings:
        print(f"WARN: {msg}")

    if result.ok and not result.warnings:
        print("Summary: no errors or warnings")
    elif result.ok:
        print(f"Summary: no errors, {len(result.warnings)} warning(s)")
    else:
        print(f"Summary: {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
