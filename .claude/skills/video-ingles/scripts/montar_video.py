#!/usr/bin/env python3
"""Monta un vídeo (largo 16:9 o Short 9:16) a partir de escenas: imagen + audio + texto.

Uso:
    python3 montar_video.py contenido/<slug>/escenas.json

Lee las rutas relativas a la carpeta del JSON y escribe en esa misma carpeta:
    video.mp4 (o short.mp4), subtitulos.srt y capitulos.txt

Formato de escenas.json: ver plantillas/escenas.ejemplo.json
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FUENTE_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FORMATOS = {"landscape": (1920, 1080), "vertical": (1080, 1920)}


def duracion(ruta: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(ruta)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def ts_srt(seg: float) -> str:
    ms = int(round(seg * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def ts_capitulo(seg: float) -> str:
    seg = int(seg)
    h, r = divmod(seg, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"


def envolver(texto: str, ancho: int) -> str:
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        if len(actual) + len(p) + 1 > ancho and actual:
            lineas.append(actual)
            actual = p
        else:
            actual = f"{actual} {p}".strip()
    if actual:
        lineas.append(actual)
    return "\n".join(lineas)


def drawtext(archivo: Path, fuente: str, tam: int, color: str, y: str) -> str:
    return (f"drawtext=fontfile={fuente}:textfile='{archivo}':fontsize={tam}:"
            f"fontcolor={color}:line_spacing=12:x=(w-text_w)/2:y={y}:"
            f"box=1:boxcolor=black@0.55:boxborderw=24")


def main() -> None:
    cfg_path = Path(sys.argv[1]).resolve()
    base = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    formato = cfg.get("formato", "landscape")
    ancho, alto = FORMATOS[formato]
    pausa = float(cfg.get("pausa_entre_escenas", 0.6))
    vertical = formato == "vertical"
    chars = 26 if vertical else 42
    t_en, t_es = (64, 48) if vertical else (68, 50)

    tmp = Path(tempfile.mkdtemp(prefix="montaje_"))
    segmentos, srt, capitulos, t = [], [], [], 0.0

    for i, esc in enumerate(cfg["escenas"], 1):
        audio = base / esc["audio"]
        imagen = base / esc["imagen"]
        dur = duracion(audio) + pausa
        filtros = [f"scale={ancho}:{alto}:force_original_aspect_ratio=increase",
                   f"crop={ancho}:{alto}", "setsar=1"]
        if esc.get("texto_en"):
            f = tmp / f"{i:03}_en.txt"
            f.write_text(envolver(esc["texto_en"], chars), encoding="utf-8")
            y = "h*0.52" if vertical else "h*0.62"
            filtros.append(drawtext(f, FUENTE, t_en, "white", y))
        if esc.get("texto_es"):
            f = tmp / f"{i:03}_es.txt"
            f.write_text(envolver(esc["texto_es"], chars + 6), encoding="utf-8")
            y = "h*0.68" if vertical else "h*0.80"
            filtros.append(drawtext(f, FUENTE_REG, t_es, "yellow", y))
        seg = tmp / f"{i:03}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(imagen),
             "-i", str(audio), "-vf", ",".join(filtros),
             "-af", f"apad=pad_dur={pausa}", "-t", f"{dur:.3f}",
             "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k", str(seg)],
            check=True)
        segmentos.append(seg)
        texto_sub = " / ".join(x for x in (esc.get("texto_en"), esc.get("texto_es")) if x)
        if texto_sub:
            srt.append(f"{len(srt) + 1}\n{ts_srt(t)} --> {ts_srt(t + dur - pausa)}\n{texto_sub}\n")
        if esc.get("capitulo"):
            capitulos.append(f"{ts_capitulo(t)} {esc['capitulo']}")
        t += dur

    lista = tmp / "lista.txt"
    lista.write_text("".join(f"file '{s}'\n" for s in segmentos), encoding="utf-8")
    nombre = cfg.get("salida", "short.mp4" if vertical else "video.mp4")
    sin_musica = tmp / "sin_musica.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lista), "-c", "copy", str(sin_musica)], check=True)

    salida = base / nombre
    musica = cfg.get("musica")
    if musica:
        vol = float(cfg.get("volumen_musica", 0.10))
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(sin_musica),
             "-stream_loop", "-1", "-i", str(base / musica),
             "-filter_complex",
             f"[1:a]volume={vol}[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
             str(salida)], check=True)
    else:
        sin_musica.replace(salida)

    (base / "subtitulos.srt").write_text("\n".join(srt), encoding="utf-8")
    if capitulos and not capitulos[0].startswith("0:00"):
        capitulos.insert(0, "0:00 Introducción")
    (base / "capitulos.txt").write_text("\n".join(capitulos) + "\n", encoding="utf-8")
    print(f"OK {salida} ({ts_capitulo(t)}, {len(segmentos)} escenas, {salida.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
