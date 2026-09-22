#!/usr/bin/env python3
"""Compute training progress from the checkboxes in tracks/*.md.

Usage:
    python progress.py            # print the summary and update README.md
    python progress.py --check    # print only, leave README.md alone
    python progress.py --detail   # per-phase breakdown for every track
    python progress.py --detail 3 # per-phase breakdown for track 03 only
    python progress.py --next     # the next unchecked item in each track
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRACKS_DIR = ROOT / "tracks"
README = ROOT / "README.md"

START_MARKER = "<!-- PROGRESS:START -->"
END_MARKER = "<!-- PROGRESS:END -->"

CHECKBOX_RE = re.compile(r"^\s*-\s\[( |x|X)\]\s+(.*)$")
TRACK_TITLE_RE = re.compile(r"^#\s+(.*)$")
PHASE_RE = re.compile(r"^##\s+(.*)$")

BAR_FULL = "\u2588"  # █
BAR_EMPTY = "\u2591"  # ░
BAR_WIDTH = 20

# Windows consoles often default to cp1252, which cannot render the block glyphs.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

try:
    (BAR_FULL + BAR_EMPTY).encode(sys.stdout.encoding or "ascii")
    CONSOLE_BARS = (BAR_FULL, BAR_EMPTY)
except (UnicodeEncodeError, LookupError):
    CONSOLE_BARS = ("#", "-")


@dataclass
class Section:
    name: str
    done: int = 0
    total: int = 0
    first_open: str | None = None

    @property
    def pct(self) -> float:
        return 100.0 * self.done / self.total if self.total else 0.0


@dataclass
class Track:
    path: Path
    title: str
    sidecar: bool = False
    sections: list[Section] = field(default_factory=list)

    @property
    def done(self) -> int:
        return sum(s.done for s in self.sections)

    @property
    def total(self) -> int:
        return sum(s.total for s in self.sections)

    @property
    def pct(self) -> float:
        return 100.0 * self.done / self.total if self.total else 0.0

    @property
    def number(self) -> str:
        return self.path.name.split("-", 1)[0]

    @property
    def short_title(self) -> str:
        # "Track 03 - SQL & PostgreSQL (from SELECT to ...)" -> "SQL & PostgreSQL"
        text = re.sub(r"^Track\s+\d+\s*[\u2014\-:]\s*", "", self.title)
        return re.sub(r"\s*\(.*\)\s*$", "", text).strip()

    @property
    def first_open(self) -> str | None:
        for section in self.sections:
            if section.first_open:
                return section.first_open
        return None


def bar(pct: float, width: int = BAR_WIDTH, chars: tuple[str, str] = (BAR_FULL, BAR_EMPTY)) -> str:
    filled = int(round(width * pct / 100.0))
    return chars[0] * filled + chars[1] * (width - filled)


def cbar(pct: float, width: int = BAR_WIDTH) -> str:
    """A bar safe to print to this terminal."""
    return bar(pct, width, CONSOLE_BARS)


def parse_track(path: Path) -> Track:
    title = path.stem
    sidecar = False
    in_fence = False
    sections: list[Section] = []
    current = Section("(intro)")

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if "<!-- SIDECAR -->" in line:
            sidecar = True
            continue

        title_match = TRACK_TITLE_RE.match(line)
        if title_match:
            title = title_match.group(1).strip()
            continue

        phase_match = PHASE_RE.match(line)
        if phase_match:
            if current.total:
                sections.append(current)
            current = Section(phase_match.group(1).strip())
            continue

        box_match = CHECKBOX_RE.match(line)
        if box_match:
            current.total += 1
            if box_match.group(1).lower() == "x":
                current.done += 1
            elif current.first_open is None:
                current.first_open = box_match.group(2).strip()

    if current.total:
        sections.append(current)

    return Track(path=path, title=title, sidecar=sidecar, sections=sections)


def scored_tracks(tracks: list[Track]) -> list[Track]:
    return [t for t in tracks if not t.sidecar]


def sidecar_tracks(tracks: list[Track]) -> list[Track]:
    return [t for t in tracks if t.sidecar]


def load_tracks() -> list[Track]:
    if not TRACKS_DIR.is_dir():
        sys.exit(f"No tracks/ directory found at {TRACKS_DIR}")
    return [parse_track(p) for p in sorted(TRACKS_DIR.glob("*.md"))]


def strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def track_status(track: Track) -> str:
    if track.sidecar:
        if track.total == 0:
            return "inbox empty"
        open_count = track.total - track.done
        return f"{open_count} open" if open_count else "inbox clear"
    if track.pct >= 100:
        return "complete"
    if track.pct > 0:
        return "in progress"
    return "not started"


def table_row(track: Track) -> str:
    link = f"[{track.short_title}](tracks/{track.path.name})"
    if track.sidecar and track.total == 0:
        meter = f"`{bar(0)}`    —"
        count = "0 logged"
    else:
        meter = f"`{bar(track.pct)}` {track.pct:5.1f}%"
        count = f"{track.done}/{track.total}"
    return (
        f"| {track.number} | {link} | {meter} | {count} | {track_status(track)} |"
    )


def build_table(tracks: list[Track]) -> str:
    scored = scored_tracks(tracks)
    extras = sidecar_tracks(tracks)
    done = sum(t.done for t in scored)
    total = sum(t.total for t in scored)
    pct = 100.0 * done / total if total else 0.0

    lines = [
        f"### Overall: {done} / {total} reps complete \u2014 **{pct:.1f}%**",
        "",
        f"`{bar(pct, 40)}`",
        "",
        "| # | Track | Progress | Done | Status |",
        "|---|-------|----------|------|--------|",
    ]
    lines.extend(table_row(t) for t in scored)

    if extras:
        lines += [
            "",
            "### Off-syllabus (does not count toward overall %)",
            "",
            "| # | Track | Progress | Done | Status |",
            "|---|-------|----------|------|--------|",
        ]
        lines.extend(table_row(t) for t in extras)

    lines += ["", f"_Regenerate with_ `python progress.py`"]
    return "\n".join(lines)


def update_readme(table: str) -> bool:
    if not README.exists():
        print(f"warning: {README.name} not found, skipping update")
        return False

    text = README.read_text(encoding="utf-8")
    if START_MARKER not in text or END_MARKER not in text:
        print(f"warning: progress markers not found in {README.name}, skipping update")
        return False

    head, rest = text.split(START_MARKER, 1)
    _, tail = rest.split(END_MARKER, 1)
    new = f"{head}{START_MARKER}\n{table}\n{END_MARKER}{tail}"

    if new == text:
        return False
    README.write_text(new, encoding="utf-8")
    return True


def print_summary(tracks: list[Track]) -> None:
    scored = scored_tracks(tracks)
    extras = sidecar_tracks(tracks)
    done = sum(t.done for t in scored)
    total = sum(t.total for t in scored)
    pct = 100.0 * done / total if total else 0.0

    width = max((len(t.short_title) for t in tracks), default=10)
    print()
    for track in scored:
        print(
            f"  {track.number}  {track.short_title:<{width}}  {cbar(track.pct)} "
            f"{track.pct:5.1f}%   {track.done:>3}/{track.total}"
        )
    print()
    print(f"  {'':<{len(scored[0].number) if scored else 2}}  {'OVERALL':<{width}}  "
          f"{cbar(pct)} {pct:5.1f}%   {done:>3}/{total}")
    if extras:
        print()
        print("  Off-syllabus (not in overall %)")
        for track in extras:
            if track.total == 0:
                print(f"  {track.number}  {track.short_title:<{width}}  inbox empty")
            else:
                print(
                    f"  {track.number}  {track.short_title:<{width}}  {cbar(track.pct)} "
                    f"{track.pct:5.1f}%   {track.done:>3}/{track.total}"
                )
    print()


def print_detail(tracks: list[Track], only: str | None) -> None:
    for track in tracks:
        if only and not track.number.endswith(only.zfill(2)):
            continue
        print(f"\n{track.title}")
        print("-" * min(len(track.title), 78))
        for section in track.sections:
            print(
                f"  {cbar(section.pct, 12)} {section.pct:5.1f}%  "
                f"{section.done:>3}/{section.total:<3}  {strip_markdown(section.name)}"
            )
    print()


def print_next(tracks: list[Track]) -> None:
    print("\n  Next open rep in each track:\n")
    for track in tracks:
        nxt = track.first_open
        if nxt is None:
            label = "inbox empty" if track.sidecar else "complete"
            print(f"  {track.number}  {track.short_title}: {label}")
        else:
            print(f"  {track.number}  {track.short_title}:\n      {strip_markdown(nxt)[:150]}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="do not write README.md")
    parser.add_argument("--detail", nargs="?", const="", metavar="TRACK",
                        help="per-phase breakdown, optionally for one track number")
    parser.add_argument("--next", action="store_true", dest="show_next",
                        help="show the next unchecked item in each track")
    args = parser.parse_args()

    tracks = load_tracks()
    if not tracks:
        sys.exit("No track files found in tracks/")

    if args.detail is not None:
        print_detail(tracks, args.detail or None)
        return

    if args.show_next:
        print_next(tracks)
        return

    print_summary(tracks)

    if not args.check:
        if update_readme(build_table(tracks)):
            print("  README.md updated.\n")
        else:
            print("  README.md already up to date.\n")


if __name__ == "__main__":
    main()
