#!/usr/bin/env python3
"""Anima escenas con los personajes del canal: boca sincronizada con el audio, parpadeo y balanceo.

    python3 animar.py contenido/<ep>/animacion.json

animacion.json (rutas relativas a su carpeta):
{
  "salida": "animacion.mp4",
  "fps": 24,
  "personajes_dir": "../_comun/personajes",
  "pausa": 0.35,
  "planos": [
    {
      "fondo": "../_comun/fondos/aula.png",
      "pizarra": "Lección 1\\nTu primera semana",      (opcional, solo para el fondo "aula")
      "personajes": {"luz": {"x": 1450, "escala": 1.35}},   x = centro; se apoyan en el borde inferior
      "lineas": [
        {"habla": "luz", "audio": "audio/001.mp3", "texto_es": "...", "texto_en": "..."}
      ]
    }
  ]
}
Los PNG de personajes se llaman <id>_<ojos a|c>_<boca 0|1|2>.png (ver personajes.py y render.js).
"""
import json
import math
import random
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ANCHO, ALTO, SR = 1920, 1080, 24000
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CAJA_PIZARRA = (165, 195, 1105, 685)


def leer_audio(ruta: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ruta), "-f", "s16le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16)


def envolver(draw, texto, fuente, ancho_max):
    lineas = []
    for parrafo in texto.split("\n"):
        actual = ""
        for palabra in parrafo.split():
            prueba = f"{actual} {palabra}".strip()
            if draw.textlength(prueba, font=fuente) > ancho_max and actual:
                lineas.append(actual)
                actual = palabra
            else:
                actual = prueba
        lineas.append(actual)
    return lineas


def texto_centrado(img, texto, fuente, color, y, caja=True, ancho_max=1600):
    d = ImageDraw.Draw(img)
    lineas = envolver(d, texto, fuente, ancho_max)
    alto_linea = fuente.size + 12
    for i, l in enumerate(lineas):
        w = d.textlength(l, font=fuente)
        x = (ANCHO - w) / 2
        yy = y + i * alto_linea
        if caja:
            d.rounded_rectangle((x - 22, yy - 10, x + w + 22, yy + fuente.size + 14),
                                radius=14, fill=(0, 0, 0, 170))
        d.text((x, yy), l, font=fuente, fill=color)
    return y + len(lineas) * alto_linea


def fondo_plano(base: Path, plano: dict) -> Image.Image:
    img = Image.open(base / plano["fondo"]).convert("RGBA").resize((ANCHO, ALTO))
    if plano.get("pizarra"):
        d = ImageDraw.Draw(img)
        x0, y0, x1, y1 = CAJA_PIZARRA
        lineas = plano["pizarra"].split("\n")
        tam = [72] + [54] * (len(lineas) - 1)
        y = y0 + 30
        for l, t in zip(lineas, tam):
            f = ImageFont.truetype(F_BOLD if t == 72 else F_REG, t)
            for sub in envolver(d, l, f, x1 - x0 - 60):
                d.text((x0 + 40, y), sub, font=f, fill=(245, 245, 235))
                y += t + 22
            y += 10
    return img


def main() -> None:
    spec_path = Path(sys.argv[1]).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    fps = int(spec.get("fps", 24))
    pausa = float(spec.get("pausa", 0.35))
    pdir = base / spec.get("personajes_dir", "../_comun/personajes")
    rnd = random.Random(7)

    # 1) Pista de audio completa y línea de tiempo
    pistas, eventos, t = [], [], 0.0
    for ip, plano in enumerate(spec["planos"]):
        for linea in plano["lineas"]:
            a = leer_audio(base / linea["audio"])
            dur = len(a) / SR
            # nivel de voz por fotograma, normalizado por línea
            paso = SR // fps
            n = max(1, len(a) // paso)
            rms = np.array([np.sqrt(np.mean(a[i * paso:(i + 1) * paso].astype(np.float32) ** 2))
                            for i in range(n)])
            ref = np.percentile(rms, 90) or 1.0
            eventos.append({"plano": ip, "ini": t, "fin": t + dur, "linea": linea, "nivel": rms / ref})
            pistas += [a, np.zeros(int(SR * pausa), dtype=np.int16)]
            t += dur + pausa
    audio = np.concatenate(pistas)
    total = len(audio) / SR
    wav = base / "_animacion_audio.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes())

    # 2) Recursos por plano
    fondos = [fondo_plano(base, p) for p in spec["planos"]]
    cache = {}

    def sprite(pid, ojos, boca, escala):
        k = (pid, ojos, boca, escala)
        if k not in cache:
            im = Image.open(pdir / f"{pid}_{ojos}_{boca}.png").convert("RGBA")
            cache[k] = im.resize((int(im.width * escala), int(im.height * escala)), Image.LANCZOS)
        return cache[k]

    parpadeos = {}
    for p in spec["planos"]:
        for pid in p["personajes"]:
            if pid not in parpadeos:
                tiempos, x = [], rnd.uniform(0.8, 2.5)
                while x < total:
                    tiempos.append(x)
                    x += rnd.uniform(2.2, 4.8)
                parpadeos[pid] = tiempos

    f_en = ImageFont.truetype(F_BOLD, 60)
    f_es = ImageFont.truetype(F_REG, 50)

    salida = base / spec.get("salida", "animacion.mp4")
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{ANCHO}x{ALTO}", "-r", str(fps), "-i", "-", "-i", str(wav),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", str(salida)], stdin=subprocess.PIPE)

    n_frames = int(math.ceil(total * fps))
    ev_i = 0
    for f in range(n_frames):
        ts = f / fps
        while ev_i + 1 < len(eventos) and ts >= eventos[ev_i + 1]["ini"]:
            ev_i += 1
        ev = eventos[ev_i]
        plano = spec["planos"][ev["plano"]]
        frame = fondos[ev["plano"]].copy()
        hablando = ev["ini"] <= ts < ev["fin"]
        for k, (pid, pos) in enumerate(plano["personajes"].items()):
            boca = "0"
            if hablando and ev["linea"]["habla"] == pid:
                idx = int((ts - ev["ini"]) * fps)
                nv = ev["nivel"][min(idx, len(ev["nivel"]) - 1)]
                boca = "2" if nv > 0.55 else "1" if nv > 0.18 else "0"
            ojos = "c" if any(b <= ts < b + 0.13 for b in parpadeos[pid]) else "a"
            esc = float(pos.get("escala", 1.0))
            im = sprite(pid, ojos, boca, esc)
            bob = 5 * math.sin(2 * math.pi * ts / 3.2 + k * 1.7)
            x = int(pos["x"] - im.width / 2)
            y = int(ALTO - im.height + 40 + bob + pos.get("dy", 0))
            frame.alpha_composite(im, (x, y))
        if hablando:
            capa = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            ln = ev["linea"]
            y = 835 if ln.get("texto_en") and ln.get("texto_es") else 900
            if ln.get("texto_en"):
                y = texto_centrado(capa, ln["texto_en"], f_en, (255, 255, 255), y) + 8
            if ln.get("texto_es"):
                texto_centrado(capa, ln["texto_es"], f_es, (255, 214, 10), y)
            frame.alpha_composite(capa)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    wav.unlink()
    print(f"OK {salida} ({total:.1f} s, {n_frames} fotogramas)")


if __name__ == "__main__":
    main()
