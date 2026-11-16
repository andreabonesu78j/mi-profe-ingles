#!/usr/bin/env python3
"""Convierte guion.md (formato de plantillas/guion.md) en lineas.tsv para voz.py, en orden de emisión.

    python3 guion_a_lineas.py contenido/<ep>/guion.md

Reconoce:
  > MAYA: ...                         gancho (solo el primero, el elegido)
  MAYA: ...                           narración (puede seguir en varias líneas)
  - LEO|MIA|CAJERA|EMPLEADO|CHOFER: EN — ES   diálogo (solo se dice el inglés)
  | n | EN (Personaje) | ES |         frase: EN lenta → ES (Maya) → EN normal
  💬 ...: "texto"  /  💬 MAYA: "texto"  nota de Miss Maya
  - MAYA: "pregunta" → (4 s) → LEO: "respuesta"   ejercicio "Tu turno"
  7 · 8 · 16 ...                      repaso: esas frases en inglés, velocidad normal
Escribe lineas.tsv junto al guion e imprime el total de caracteres.
"""
import re
import sys
from pathlib import Path

VOZ = {"leo": "leo", "mia": "mia", "maya": "maya", "cajera": "staff", "empleado": "staff",
       "empleada": "staff", "chofer": "staff"}
LENTA = {"leo": "leo_lenta", "mia": "mia_lenta", "staff": "staff"}


def main() -> None:
    guion = Path(sys.argv[1])
    texto = guion.read_text(encoding="utf-8").splitlines()
    filas, frases = [], {}
    gancho_hecho = False
    i = 0

    def add(voz, t, extra=""):
        t = t.strip().strip('"').strip()
        if t:
            filas.append((voz, t, extra))

    while i < len(texto):
        l = texto[i].rstrip()
        if l.startswith("## Estimación"):
            break
        m = re.match(r"^> MAYA: (.+)", l)
        if m:
            partes = [m.group(1)]
            while i + 1 < len(texto) and texto[i + 1].startswith("> ") and not texto[i + 1].startswith("> MAYA:"):
                i += 1; partes.append(texto[i][2:].strip())
            if not gancho_hecho:
                add("maya", " ".join(partes)); gancho_hecho = True
            i += 1; continue
        m = re.match(r"^MAYA: (.+)", l)
        if m:
            partes = [m.group(1)]
            while i + 1 < len(texto) and texto[i + 1].strip() and not re.match(r"^(\[|#|-|\||💬|>)", texto[i + 1]):
                i += 1; partes.append(texto[i].strip())
            add("maya", " ".join(partes)); i += 1; continue
        m = re.match(r"^\| (\d+) \| (.+?) \((\w+)\) \| (.+?) \|$", l)
        if m:
            n, en, quien, es = m.groups()
            v = VOZ[quien.lower()]
            frases[int(n)] = (v, en)
            add(LENTA[v], en, f"#{n} lenta"); add("maya", es, f"#{n} es"); add(v, en, f"#{n} normal")
            i += 1; continue
        m = re.match(r"^- MAYA: (\".+?\") → \(4 s\) → (\w+): (\".+\")", l)
        if m:
            add("maya", m.group(1)); filas.append(("PAUSA4", "", "")); add(VOZ[m.group(2).lower()], m.group(3))
            i += 1; continue
        m = re.match(r"^- (LEO|MIA|CAJERA|EMPLEADO|EMPLEADA|CHOFER): (.+?) — ", l)
        if m:
            add(VOZ[m.group(1).lower()], m.group(2), "diálogo"); i += 1; continue
        m = re.match(r'^💬 [^"]*"(.+)', l)
        if m:
            partes = [m.group(1)]
            while not partes[-1].rstrip().endswith('"') and i + 1 < len(texto):
                i += 1; partes.append(texto[i].strip())
            nota = " ".join(partes).rstrip('"')
            ref = re.search(r"Después de la (\d+)", l)
            pos = next((k + 1 for k, f in enumerate(filas) if ref and f[2] == f"#{ref.group(1)} normal"), None)
            if pos is None:
                add("maya", nota)
            else:
                filas.insert(pos, ("maya", nota.strip(), "nota"))
            i += 1; continue
        if re.match(r"^\d+(/\d+)? ·", l):
            for num in re.findall(r"\d+", l):
                if int(num) in frases:
                    v, en = frases[int(num)]; add(v, en, f"#{num} repaso")
            i += 1; continue
        i += 1

    salida = guion.parent / "lineas.tsv"
    with salida.open("w", encoding="utf-8") as f:
        n = 0
        for voz, t, extra in filas:
            if voz == "PAUSA4":
                f.write("# pausa 4 s\n"); continue
            n += 1
            f.write(f"{n:04d}.mp3\t{voz}\t{t}\n")
    chars = sum(len(t) for v, t, _ in filas if v != "PAUSA4")
    por_voz = {}
    for v, t, _ in filas:
        if v != "PAUSA4":
            por_voz[v] = por_voz.get(v, 0) + len(t)
    print(f"OK {salida}: {n} audios, {len(frases)} frases, {chars} caracteres")
    print("  por voz:", ", ".join(f"{k} {v}" for k, v in sorted(por_voz.items())))


if __name__ == "__main__":
    main()
