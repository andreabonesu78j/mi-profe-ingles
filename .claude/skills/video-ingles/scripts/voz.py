#!/usr/bin/env python3
"""Genera los MP3 de un episodio con ElevenLabs (motor "elevenlabs") o Piper (motor "piper", gratis).

Uso:
    python3 voz.py contenido/<ep>/lineas.tsv

lineas.tsv: una línea por audio, separada por tabuladores:
    <archivo>\t<voz>\t<texto>
    001.mp3\tnarradora\tHoy aprendes a hablar con el médico en inglés.
    002.mp3\ten_lenta\tI have an appointment at ten.
    003.mp3\ten_b\tWhat seems to be the problem?

Voces: las claves de contenido/voces.json (maya, leo, leo_lenta, mia, mia_lenta…).
La clave de ElevenLabs la inyecta el proxy del entorno (no hace falta variable).
Los MP3 se escriben en contenido/<ep>/audio/. Los que ya existen no se regeneran.
"""
import json
import urllib.request
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
MODELOS = RAIZ / ".cache" / "piper"


def elevenlabs(cfg: dict, texto: str, destino: Path) -> None:
    ajustes = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.3}
    ajustes.update(cfg.get("ajustes", {}))
    if cfg.get("velocidad"):
        ajustes["speed"] = cfg["velocidad"]
    cuerpo = json.dumps({"text": texto, "model_id": cfg.get("modelo", "eleven_multilingual_v2"),
                         "voice_settings": ajustes}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice_id']}?output_format=mp3_44100_128",
        data=cuerpo, method="POST",
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    with urllib.request.urlopen(req, timeout=120) as r:
        destino.write_bytes(r.read())


def main() -> None:
    tsv = Path(sys.argv[1]).resolve()
    voces = json.loads((RAIZ / "contenido" / "voces.json").read_text(encoding="utf-8"))
    salida = tsv.parent / "audio"
    salida.mkdir(exist_ok=True)
    hechos = 0
    for n, linea in enumerate(tsv.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip() or linea.startswith("#"):
            continue
        archivo, voz, texto = linea.split("\t", 2)
        destino = salida / archivo
        if destino.exists():
            continue
        cfg = voces[voz]
        if cfg.get("motor") == "elevenlabs":
            elevenlabs(cfg, texto, destino)
            hechos += 1
            continue
        modelo = MODELOS / f"{cfg['modelo']}.onnx"
        if not modelo.exists():
            sys.exit(f"Falta {modelo}: ejecuta scripts/preparar.sh")
        with tempfile.NamedTemporaryFile(suffix=".wav") as wav:
            subprocess.run(
                [sys.executable, "-m", "piper", "-m", str(modelo), "-f", wav.name,
                 "--length-scale", str(cfg.get("velocidad", 1.0))],
                input=texto, text=True, check=True, capture_output=True)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav.name,
                            "-c:a", "libmp3lame", "-q:a", "3", str(destino)], check=True)
        hechos += 1
    print(f"OK {hechos} audios nuevos en {salida}")


if __name__ == "__main__":
    main()
