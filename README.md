# Vintage Apple Computing Digest

An automated weekly digest that tracks vintage Apple computing content across
forums, communities, GitHub, blogs, and archives. Runs on GitHub Actions every
Monday and commits findings to this repository.

## What It Tracks

The tracker searches for recent activity (past 7-10 days) related to:

- **Emulation**: Projects and updates for Mini vMac, Basilisk II, SheepShaver, QEMU
- **Gaming**: Classic Mac game ports, preservation, and discoveries
- **App Revivals**: Modern ports or revivals of classic Mac applications
- **Hardware**: Repairs, modifications, networking, and peripherals
- **Software**: New utilities and system extensions for classic Mac OS
- **Community Projects**: Preservation efforts, documentation, and archives

Content is focused on System 6, System 7, and Mac OS Classic (pre-OS X).

## How It Works

Every Monday at 9:00 AM UTC, a GitHub Actions workflow:

1. Runs a Python script that uses Claude's web search to find recent vintage Apple content
2. Organizes findings by category
3. Writes a markdown digest to `digest/YYYY-WNN.md` (ISO week format)
4. Commits the results to this repository

The agent uses **neutral, factual language** - no editorializing or subjective
adjectives. You decide what's interesting.

## Reading the Output

All digests are in the `digest/` directory:

```
digest/
├── 2026-W13.md
├── 2026-W14.md
└── 2026-W15.md
```

Each digest is organized by category (Emulation, Gaming, App Revivals, Hardware,
Software, Community Projects, Other) with 2-3 sentence summaries and source links.

## Running Manually

You can trigger a digest at any time:

1. Go to the **Actions** tab in this repository
2. Select **Weekly Vintage Apple Digest**
3. Click **Run workflow**

## Setup (one-time)

### 1. Create repository on GitHub

Create a new repository (public or private) and push this code.

### 2. Add Anthropic API key

1. Go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: your Anthropic API key from https://console.anthropic.com

That's it. The workflow will run automatically every Monday, or you can trigger
it manually from the Actions tab.

## Modifying Sources

The `SOURCES.md` file lists communities and sources the agent searches. This is
guidance for the agent - you can edit it to focus searches, but the agent may
also find relevant content from other vintage Apple communities.

## Cost

Anthropic API usage is approximately $2-5 per weekly run, depending on how much
content is found. Monthly cost estimate: $8-20.

## Requirements

- GitHub account (free tier sufficient)
- Anthropic API key (pay-per-use)
- Python 3.12+ (provided by GitHub Actions)

No server, no database, no local installation required.
