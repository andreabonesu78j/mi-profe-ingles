#!/usr/bin/env python3
"""Crea animacion.json (para arte/animar.py) a partir de lineas.tsv, con textos y pausas de repetición.

    python3 lineas_a_animacion.py contenido/<ep>/lineas.tsv [--fondo RUTA] [--sprites DIR]

Reconoce el patrón de frase  <voz>_lenta EN · maya ES · <voz> EN  → muestra EN + ES y deja 3 s para repetir,
y "# pausa 4 s" (ejercicio Tu turno). La narración de Miss Maya no lleva texto en pantalla.
Personajes en escena: Miss Maya (izquierda), Leo (centro), Mia (derecha).
"""
import json
import sys
from pathlib import Path

HABLA = {"maya": "maya", "leo": "leo", "leo_lenta": "leo", "mia": "mia", "mia_lenta": "mia", "staff": None}


def main() -> None:
    tsv = Path(sys.argv[1]).resolve()
    args = sys.argv[2:]
    fondo = args[args.index("--fondo") + 1] if "--fondo" in args else "../../characters/_preview/fondo.png"
    sprites = args[args.index("--sprites") + 1] if "--sprites" in args else "../../characters/_preview"
    filas, pausa_sig = [], False
    for l in tsv.read_text(encoding="utf-8").splitlines():
        if l.startswith("# pausa"):
            filas[-1]["pausa"] = 4.0
            continue
        if not l.strip() or l.startswith("#"):
            continue
        archivo, voz, texto = l.split("\t", 2)
        filas.append({"audio": f"audio/{archivo}", "voz": voz, "texto": texto})
    lineas, i = [], 0
    while i < len(filas):
        f = filas[i]
        trio = filas[i:i + 3]
        if (len(trio) == 3 and f["voz"].endswith("_lenta") and trio[1]["voz"] == "maya"
                and trio[2]["texto"] == f["texto"]):
            en, es = f["texto"], trio[1]["texto"]
            for k, g in enumerate(trio):
                lineas.append({"habla": HABLA[g["voz"]] or "maya", "audio": g["audio"],
                               "texto_en": en, "texto_es": es, "pausa": 3.0 if k == 2 else 0.4})
            i += 3
            continue
        ln = {"habla": HABLA.get(f["voz"]) or "maya", "audio": f["audio"], "pausa": f.get("pausa", 0.5)}
        if f["voz"] != "maya":
            ln["texto_en"] = f["texto"]
        lineas.append(ln)
        i += 1
    spec = {"salida": "episodio-preliminar.mp4", "fps": 24, "personajes_dir": sprites,
            "planos": [{"fondo": fondo,
                        "personajes": {"maya": {"x": 330, "escala": 1.0}, "leo": {"x": 960, "escala": 1.0},
                                       "mia": {"x": 1590, "escala": 1.0}},
                        "lineas": lineas}]}
    out = tsv.parent / "animacion.json"
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK {out}: {len(lineas)} líneas")


if __name__ == "__main__":
    main()
