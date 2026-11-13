#!/usr/bin/env bash
# Instala las herramientas gratis del canal y descarga las voces de Piper (una sola vez por máquina).
# Uso: bash .claude/skills/video-ingles/scripts/preparar.sh
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../../../.." && pwd)"
VOCES="$RAIZ/.cache/piper"
pip install -q piper-tts yt-dlp
mkdir -p "$VOCES"
cd "$VOCES"
for v in es_MX-claude-high en_US-amy-medium en_US-ryan-high; do
  [ -f "$v.onnx" ] || python3 -m piper.download_voices "$v"
done
echo "Listo: voces en $VOCES"
