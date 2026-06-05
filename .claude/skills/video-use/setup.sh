#!/usr/bin/env bash
# Runtime setup for the vendored video-use skill.
#
# The skill files (SKILL.md + helpers/) live in the repo and persist, but the
# runtime dependencies (ffmpeg + Python libs) do NOT survive an ephemeral
# container, so they must be (re)installed per session BEFORE using the helpers.
# This script is idempotent: re-running it is cheap because it skips anything
# already installed.
#
#   bash .claude/skills/video-use/setup.sh
#
set -uo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Python dependencies -----------------------------------------------------
if python3 -c "import numpy, librosa, matplotlib, PIL, requests" >/dev/null 2>&1; then
  echo "==> Python dependencies already present"
else
  echo "==> Installing Python dependencies (requests, librosa, matplotlib, pillow, numpy)"
  if command -v uv >/dev/null 2>&1; then
    uv pip install --system requests librosa matplotlib pillow numpy
  else
    python3 -m pip install --quiet requests librosa matplotlib pillow numpy
  fi
fi

# --- ffmpeg ------------------------------------------------------------------
if command -v ffmpeg >/dev/null 2>&1; then
  echo "==> ffmpeg already on PATH"
else
  echo "==> Installing ffmpeg"
  if command -v apt-get >/dev/null 2>&1; then
    # Install directly first: this succeeds even when `apt-get update` would
    # fail on unrelated/broken third-party PPAs in the base image.
    sudo apt-get install -y -qq ffmpeg 2>/dev/null \
      || { sudo apt-get update -qq || true; sudo apt-get install -y -qq ffmpeg; }
  elif command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --noconfirm ffmpeg
  else
    echo "!! No package manager found to install ffmpeg. Install it manually." >&2
  fi
fi

# --- ElevenLabs API key (for transcription) ----------------------------------
# Most secure option: set ELEVENLABS_API_KEY as an environment variable in your
# Claude Code environment settings. If it is present, mirror it into a local,
# git-ignored .env (chmod 600) so the helpers can read it.
if [ -n "${ELEVENLABS_API_KEY:-}" ] && [ ! -f "$SKILL_DIR/.env" ]; then
  printf 'ELEVENLABS_API_KEY=%s\n' "$ELEVENLABS_API_KEY" > "$SKILL_DIR/.env"
  chmod 600 "$SKILL_DIR/.env"
  echo "==> Wrote .env from ELEVENLABS_API_KEY environment variable"
fi

if [ -f "$SKILL_DIR/.env" ] && grep -q '^ELEVENLABS_API_KEY=.\+' "$SKILL_DIR/.env"; then
  echo "==> ElevenLabs API key configured"
elif [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  echo "==> ElevenLabs API key available via environment variable"
else
  echo "!! No ELEVENLABS_API_KEY set. Transcription will not work until you add one."
  echo "   Recommended: add ELEVENLABS_API_KEY in your environment settings, OR run:"
  echo "     printf 'ELEVENLABS_API_KEY=YOUR_KEY\\n' > $SKILL_DIR/.env && chmod 600 $SKILL_DIR/.env"
  echo "   Get a key at https://elevenlabs.io/app/settings/api-keys"
fi

# --- Verify ------------------------------------------------------------------
if python3 "$SKILL_DIR/helpers/timeline_view.py" --help >/dev/null 2>&1; then
  echo "==> Helpers OK. video-use is ready."
else
  echo "!! Helpers failed to load — check the Python dependency step above." >&2
  exit 1
fi
