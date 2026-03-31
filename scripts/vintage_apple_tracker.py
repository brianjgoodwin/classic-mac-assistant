#!/usr/bin/env python3
"""Weekly tracking run: find recent vintage Apple computing content."""

import os
import sys

from utils import (
    get_client,
    call_with_search,
    read_file,
    write_file,
    today,
    week_id,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- System prompt ---

TRACKER_SYSTEM = """\
You are a research assistant tracking vintage Apple computing content for a Mac enthusiast.
Your user is interested in classic Macintosh systems (System 6, System 7, Mac OS Classic),
emulation projects, classic Mac gaming, and modern revivals of classic Mac applications.

Search for recent activity (past 7-10 days) across vintage Apple computing communities,
forums, GitHub projects, blogs, and other relevant sources.

Look for:
- New emulation projects or major updates to existing emulators
- Classic Mac game ports, discoveries, or preservation efforts
- Modern revivals or ports of classic Mac applications
- Hardware projects (repairs, modifications, networking)
- Software releases (utilities, system extensions, applications for classic Mac OS)
- Community projects and collaborative efforts
- Technical discussions or documentation that uncover new information
- Archive discoveries or newly digitized materials

**Important tone guidelines:**
- Use NEUTRAL, FACTUAL language only
- NO subjective adjectives like "interesting", "exciting", "fascinating", "impressive"
- NO value judgments about quality or importance
- State what happened, who did it, and relevant technical details
- Let the facts speak for themselves

Output a markdown document organized by category with this structure:

# Vintage Apple Computing Digest — {week_id}

Week ending {date}

## Emulation

(Projects, updates, or discussions related to emulating classic Mac systems)

### [Topic Title]
[2-3 sentence factual summary]

**Source:** [Link](URL)

## Gaming

(Classic Mac games, ports, preservation, or gameplay discussions)

### [Topic Title]
...

## App Revivals

(Modern ports or revivals of classic Mac applications)

### [Topic Title]
...

## Hardware

(Hardware repairs, modifications, networking, or peripherals)

### [Topic Title]
...

## Software

(New software, utilities, or system extensions for classic Mac OS)

### [Topic Title]
...

## Community Projects

(Collaborative efforts, documentation, archives, or preservation)

### [Topic Title]
...

## Other

(Anything else relevant that doesn't fit the above categories)

### [Topic Title]
...

---

If a category has no findings, omit that section entirely.
Do not fabricate information. If searches return minimal results, report what you found
and note that activity was light this week."""


def run():
    date = today()
    wid = week_id()
    print(f"Vintage Apple tracker run: {date} ({wid})")

    # Read sources file for context
    sources_path = os.path.join(REPO_ROOT, "SOURCES.md")
    sources_text = read_file(sources_path)
    if not sources_text:
        print("SOURCES.md not found. Continuing without source guidance.")
        sources_text = ""

    client = get_client()

    # Single search phase - let the agent do broad searching
    print("\nSearching for vintage Apple computing activity...")

    sources_context = ""
    if sources_text:
        sources_context = f"\n\nSource guidance:\n---\n{sources_text}\n---\n"

    user_msg = (
        f"Today's date: {date}\n"
        f"Week ID: {wid}\n"
        f"Search for vintage Apple computing content from the past 7-10 days.\n"
        f"Focus on: System 6, System 7, Mac OS Classic, emulation (Mini vMac, Basilisk II, "
        f"SheepShaver, QEMU), classic Mac gaming, modern app revivals, hardware projects, "
        f"and community preservation efforts."
        f"{sources_context}"
    )

    try:
        result = call_with_search(client, TRACKER_SYSTEM, user_msg)
    except Exception as e:
        print(f"Search failed: {e}")
        raise SystemExit(1)

    # Write digest
    digest_path = os.path.join(REPO_ROOT, "digest", f"{wid}.md")
    try:
        write_file(digest_path, result + "\n")
        print(f"\nDone. Digest written to digest/{wid}.md")
    except Exception as e:
        print(f"Failed to write digest: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    run()
