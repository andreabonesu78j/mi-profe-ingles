#!/usr/bin/env python3
"""Prepara un episodio para el estudio de Remotion (estudio/): línea de tiempo, audios, imágenes y mini-tests.

    python3 construir_episodio.py contenido/<ep> [--test-cada 5]

Lee:
  contenido/<ep>/lineas.tsv          audios en orden (de guion_a_lineas.py)
  contenido/<ep>/audio/NNNN.mp3      voces ya generadas
  contenido/<ep>/planos.md           tabla de planos (P01…): qué imagen va en cada momento
  contenido/<ep>/planos/PNN.png      ilustraciones (si falta alguna, se usa un marcador provisional)
Escribe:
  estudio/public/<ep>/…              copia de audios e imágenes
  estudio/public/<ep>/episodio.json  escenas con tiempos, textos, cámara y mini-tests (props de Remotion)

Reglas de planos (de la columna "Momento" de planos.md):
  "Gancho" → primera narración · "Presentación" → segunda · "N · …" → frase N (y "N · … / M · …")
  "Mini-test K" → test tras la frase K*test_cada · "Cierre" → última narración · "Tu turno" → ejercicios
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
HABLA = {"maya": "maya", "leo": "leo", "leo_lenta": "leo", "mia": "mia", "mia_lenta": "mia", "staff": "staff"}
CAMARAS = [((1.0, 0.5, 0.5), (1.12, 0.45, 0.45)), ((1.12, 0.55, 0.5), (1.0, 0.5, 0.5)),
           ((1.05, 0.4, 0.5), (1.12, 0.6, 0.5)), ((1.08, 0.5, 0.6), (1.15, 0.5, 0.4))]


def dur(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(p)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def leer_planos(md: Path) -> dict:
    planos = {"frase": {}, "test": {}}
    for l in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (P\d+) \| (.+?) \|", l)
        if not m:
            continue
        pid, momento = m.group(1), m.group(2)
        if "Gancho" in momento:
            planos["gancho"] = pid
        elif "Presentación" in momento:
            planos["presentacion"] = pid
        elif "Cierre" in momento:
            planos["cierre"] = pid
        elif "Mini-test" in momento:
            k = int(re.search(r"Mini-test\*?\*? ?(\d+)", momento.replace("*", "")).group(1))
            planos["test"][k] = pid
            if "Tu turno" in momento:
                planos["turno"] = pid
        for n in re.findall(r"(\d+) ·", momento):
            planos["frase"][int(n)] = pid
    return planos


def main() -> None:
    ep = Path(sys.argv[1]).resolve()
    args = sys.argv[2:]
    cada = int(args[args.index("--test-cada") + 1]) if "--test-cada" in args else 5
    planos = leer_planos(ep / "planos.md")
    pub = RAIZ / "estudio" / "public" / ep.name
    (pub / "audio").mkdir(parents=True, exist_ok=True)
    (pub / "planos").mkdir(parents=True, exist_ok=True)

    filas = []
    for l in (ep / "lineas.tsv").read_text(encoding="utf-8").splitlines():
        if l.startswith("# pausa"):
            filas[-1]["pausa"] = 4.0
            continue
        if not l.strip() or l.startswith("#"):
            continue
        archivo, voz, texto = l.split("\t", 2)
        filas.append({"archivo": archivo, "voz": voz, "texto": texto})

    # agrupar en bloques: frase (lenta+es+normal) o línea suelta
    bloques, i, n_frase = [], 0, 0
    while i < len(filas):
        f, trio = filas[i], filas[i:i + 3]
        if (len(trio) == 3 and f["voz"].endswith("_lenta") and trio[1]["voz"] == "maya"
                and trio[2]["texto"] == f["texto"]):
            n_frase += 1
            bloques.append({"tipo": "frase", "n": n_frase, "en": f["texto"], "es": trio[1]["texto"], "lineas": trio})
            i += 3
            continue
        bloques.append({"tipo": "linea", "lineas": [f]})
        i += 1
    total = n_frase

    narraciones = [k for k, b in enumerate(bloques) if b["tipo"] == "linea" and b["lineas"][0]["voz"] == "maya"]
    escenas, frase_actual, frases = [], 0, {}

    def img(pid):
        src = ep / "planos" / f"{pid}.png"
        if src.exists():
            shutil.copy2(src, pub / "planos" / src.name)
            return f"{ep.name}/planos/{src.name}"
        return None  # marcador provisional

    def audio(fila):
        src = ep / "audio" / fila["archivo"]
        shutil.copy2(src, pub / "audio" / src.name)
        return f"{ep.name}/audio/{src.name}", dur(src)

    def camara(k):
        a, b = CAMARAS[k % len(CAMARAS)]
        return {"desde": a, "hasta": b}

    for k, b in enumerate(bloques):
        if b["tipo"] == "frase":
            frase_actual = b["n"]
            frases[b["n"]] = b
            pid = planos["frase"].get(b["n"], "P??")
            for j, fila in enumerate(b["lineas"]):
                a, d = audio(fila)
                escenas.append({"tipo": "frase", "plano": pid, "imagen": img(pid), "audio": a, "dur": d,
                                "pausa": 3.0 if j == 2 else 0.35, "n": b["n"], "total": total,
                                "en": b["en"], "es": b["es"], "habla": HABLA[fila["voz"]],
                                "paso": ["lenta", "traduccion", "normal"][j], "camara": camara(b["n"])})
            if b["n"] % cada == 0:
                kt = b["n"] // cada
                pid_t = planos["test"].get(kt, "P??")
                for m in range(b["n"] - cada + 1, b["n"] + 1):
                    fr = frases[m]
                    a, d = audio(fr["lineas"][2])
                    escenas.append({"tipo": "test", "plano": pid_t, "imagen": img(pid_t), "audio": a, "dur": d,
                                    "espera": 3.0, "pausa": 0.8, "n": m, "total": total, "test": kt,
                                    "en": fr["en"], "es": fr["es"], "camara": camara(kt)})
            continue
        fila = b["lineas"][0]
        if k == narraciones[0]:
            pid = planos.get("gancho")
        elif len(narraciones) > 1 and k == narraciones[1]:
            pid = planos.get("presentacion")
        elif k == narraciones[-1]:
            pid = planos.get("cierre")
        elif fila.get("pausa") or (k > 0 and bloques[k - 1]["lineas"][-1].get("pausa")):
            pid = planos.get("turno")
        else:
            pid = planos["frase"].get(frase_actual)  # nota de Miss Maya: se queda en el plano de su frase
        a, d = audio(fila)
        esc = {"tipo": "narracion", "plano": pid, "imagen": img(pid) if pid else None, "audio": a, "dur": d,
               "pausa": fila.get("pausa", 0.5), "habla": HABLA[fila["voz"]], "camara": camara(k)}
        if fila["voz"] != "maya":
            esc["en"] = fila["texto"]
        if fila.get("pausa"):
            esc["cuenta_atras"] = True
        escenas.append(esc)

    titulo = (ep / "guion.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ").split(" — Nivel")[0]
    datos = {"episodio": ep.name, "titulo": titulo, "fps": 30, "escenas": escenas,
             "personajes": "personajes", "sfx": "sfx"}
    (pub / "episodio.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    seg = sum(e["dur"] + e["pausa"] + e.get("espera", 0) for e in escenas)
    faltan = sorted({e["plano"] for e in escenas if e.get("plano") and not e.get("imagen")})
    print(f"OK {pub/'episodio.json'}: {len(escenas)} escenas, {seg/60:.1f} min, frases {total}, "
          f"tests {total // cada}")
    if faltan:
        print("  imágenes que faltan (se verá un marcador provisional):", ", ".join(faltan))


if __name__ == "__main__":
    main()
