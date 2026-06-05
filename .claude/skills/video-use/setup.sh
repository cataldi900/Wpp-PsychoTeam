#!/usr/bin/env bash
# Runtime setup for the vendored video-use skill.
#
# The skill files (SKILL.md + helpers/) live in the repo and persist, but the
# runtime dependencies (ffmpeg + Python libs) do NOT survive an ephemeral
# container, so they must be (re)installed per session. Run this script once at
# the start of a session that needs video editing.
#
#   bash .claude/skills/video-use/setup.sh
#
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing Python dependencies (requests, librosa, matplotlib, pillow, numpy)"
if command -v uv >/dev/null 2>&1; then
  uv pip install --system requests librosa matplotlib pillow numpy
else
  python3 -m pip install --quiet requests librosa matplotlib pillow numpy
fi

echo "==> Ensuring ffmpeg is present"
if ! command -v ffmpeg >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg
  elif command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --noconfirm ffmpeg
  else
    echo "!! Could not find a package manager to install ffmpeg. Install it manually." >&2
  fi
else
  echo "    ffmpeg already on PATH"
fi

echo "==> Checking ElevenLabs API key"
if [ -f "$SKILL_DIR/.env" ] && grep -q '^ELEVENLABS_API_KEY=.\+' "$SKILL_DIR/.env"; then
  echo "    .env with ELEVENLABS_API_KEY found"
else
  echo "!! No ELEVENLABS_API_KEY set. Transcription will not work until you add one:"
  echo "     echo 'ELEVENLABS_API_KEY=sk_...' > $SKILL_DIR/.env && chmod 600 $SKILL_DIR/.env"
  echo "   Get a key at https://elevenlabs.io/app/settings/api-keys"
fi

echo "==> Verifying helpers"
python3 "$SKILL_DIR/helpers/timeline_view.py" --help >/dev/null && echo "    helpers OK"
echo "Done."
