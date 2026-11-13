#!/usr/bin/env python3
"""Genera los MP3 de un episodio con Piper (gratis, sin conexión).

Uso:
    python3 voz.py contenido/<ep>/lineas.tsv

lineas.tsv: una línea por audio, separada por tabuladores:
    <archivo>\t<voz>\t<texto>
    001.mp3\tnarradora\tHoy aprendes a hablar con el médico en inglés.
    002.mp3\ten_lenta\tI have an appointment at ten.
    003.mp3\ten_b\tWhat seems to be the problem?

Voces (definidas en contenido/voces.json): narradora, en_a, en_lenta, en_b, en_b_lenta.
Los MP3 se escriben en contenido/<ep>/audio/. Los que ya existen no se regeneran.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
MODELOS = RAIZ / ".cache" / "piper"


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
