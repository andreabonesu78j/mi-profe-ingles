#!/usr/bin/env python3
"""Personajes del canal dibujados en SVG (originales, sin coste) y sus estados para animar.

    python3 personajes.py <carpeta_salida>

Escribe un SVG por personaje y estado: <id>_<ojos>_<boca>.svg
  ojos: a (abiertos) | c (cerrados)      boca: 0 (cerrada) | 1 (media) | 2 (abierta)
Luego render.js los convierte en PNG transparentes.
"""
import sys
from pathlib import Path

W, H = 500, 620

PERSONAJES = {
    "sofia": {
        "nombre": "Sofía", "rol": "Recién llegada a EE. UU. Aprende contigo.",
        "piel": "#C68B59", "piel_sombra": "#A9713F", "pelo": "#2B1B14", "iris": "#5B3A1E",
        "ropa": "#2A9D8F", "ropa2": "#E9C46A", "peinado": "largo", "extra": "aretes",
    },
    "mike": {
        "nombre": "Mike", "rol": "Vecino y compañero de trabajo estadounidense.",
        "piel": "#F1C7A5", "piel_sombra": "#D9A784", "pelo": "#7A4B2A", "iris": "#3C6E91",
        "ropa": "#264653", "ropa2": "#F4F1DE", "peinado": "corto", "extra": "barba",
    },
    "luz": {
        "nombre": "Profe Luz", "rol": "La narradora: explica en español.",
        "piel": "#8D5524", "piel_sombra": "#6F4019", "pelo": "#1A1110", "iris": "#2E1A0F",
        "ropa": "#7B2D8E", "ropa2": "#FFFFFF", "peinado": "mono", "extra": "gafas",
    },
}


def pelo_detras(p):
    c = p["pelo"]
    if p["peinado"] == "largo":
        return (f'<path d="M140 235 Q125 95 250 92 Q375 95 360 235 Q382 370 345 445 '
                f'L155 445 Q118 370 140 235 Z" fill="{c}"/>')
    if p["peinado"] == "mono":
        return f'<circle cx="250" cy="92" r="52" fill="{c}"/>'
    return ""


def pelo_delante(p):
    c = p["pelo"]
    if p["peinado"] == "largo":
        return (f'<path d="M143 228 Q145 105 252 104 Q356 106 357 228 Q338 165 268 150 '
                f'Q210 182 143 228 Z" fill="{c}"/>')
    if p["peinado"] == "corto":
        return (f'<path d="M146 205 Q140 100 252 96 Q362 100 354 205 Q345 150 300 140 '
                f'Q255 160 200 140 Q160 150 146 205 Z" fill="{c}"/>')
    # mono: pelo recogido con raya al lado
    return (f'<path d="M145 225 Q140 112 250 108 Q360 112 355 225 Q345 160 290 148 '
            f'Q230 150 185 170 Q160 190 145 225 Z" fill="{c}"/>')


def ojos(p, estado):
    out = []
    for cx in (210, 290):
        if estado == "c":
            out.append(f'<path d="M{cx-18} 238 Q{cx} 249 {cx+18} 238" stroke="#2B1B14" '
                       f'stroke-width="4" fill="none" stroke-linecap="round"/>')
        else:
            out.append(
                f'<ellipse cx="{cx}" cy="236" rx="17" ry="20" fill="#fff"/>'
                f'<circle cx="{cx+2}" cy="239" r="11" fill="{p["iris"]}"/>'
                f'<circle cx="{cx+2}" cy="239" r="6" fill="#111"/>'
                f'<circle cx="{cx+6}" cy="234" r="3.5" fill="#fff"/>')
    return "".join(out)


def boca(estado):
    if estado == "0":
        return ('<path d="M226 302 Q250 320 274 302" stroke="#5A1E1E" stroke-width="5" '
                'fill="none" stroke-linecap="round"/>')
    alto = 336 if estado == "1" else 362
    return (f'<path d="M222 298 Q250 {alto} 278 298 Q250 304 222 298 Z" fill="#5A1E1E"/>'
            f'<path d="M232 300 Q250 304 268 300 L266 305 Q250 308 234 305 Z" fill="#fff"/>'
            f'<ellipse cx="250" cy="{(298 + alto) // 2 + 4}" rx="{9 if estado == "1" else 14}" '
            f'ry="{4 if estado == "1" else 7}" fill="#E07A7A"/>')


def extra(p):
    e = p["extra"]
    if e == "barba":
        return (f'<path d="M150 250 Q158 352 250 360 Q342 352 350 250 Q338 318 250 324 '
                f'Q162 318 150 250 Z" fill="{p["pelo"]}"/>'
                f'<path d="M218 288 Q250 276 282 288 Q250 296 218 288 Z" fill="{p["pelo"]}"/>')
    if e == "gafas":
        return ('<g stroke="#222" stroke-width="5" fill="#ffffff22">'
                '<rect x="182" y="212" width="56" height="48" rx="16"/>'
                '<rect x="262" y="212" width="56" height="48" rx="16"/>'
                '<path d="M238 232 Q250 224 262 232" fill="none"/></g>')
    if e == "aretes":
        return ('<circle cx="146" cy="282" r="9" fill="#E9C46A"/>'
                '<circle cx="354" cy="282" r="9" fill="#E9C46A"/>')
    return ""


def ropa(p):
    c, c2 = p["ropa"], p["ropa2"]
    torso = f'<path d="M60 620 Q70 425 250 405 Q430 425 440 620 Z" fill="{c}"/>'
    if p["extra"] == "barba":  # sudadera con capucha y cordones
        return (torso + f'<path d="M175 418 Q250 470 325 418 Q300 400 250 398 Q200 400 175 418 Z" fill="#1d3640"/>'
                f'<path d="M228 450 L224 520 M272 450 L276 520" stroke="{c2}" stroke-width="5" stroke-linecap="round"/>')
    if p["extra"] == "gafas":  # blusa blanca y chaqueta
        return (torso + f'<path d="M195 408 L250 515 L305 408 Q250 398 195 408 Z" fill="{c2}"/>'
                f'<path d="M195 408 L250 515 L215 620 M305 408 L250 515 L285 620" '
                f'stroke="#5c1f6b" stroke-width="5" fill="none"/>')
    return (torso + f'<path d="M205 410 Q250 455 295 410" stroke="{c2}" stroke-width="12" fill="none"/>')


def svg(pid, ojo, bo):
    p = PERSONAJES[pid]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{pelo_detras(p)}
{ropa(p)}
<rect x="215" y="320" width="70" height="95" rx="30" fill="{p["piel_sombra"]}"/>
<ellipse cx="146" cy="250" rx="18" ry="26" fill="{p["piel"]}"/>
<ellipse cx="354" cy="250" rx="18" ry="26" fill="{p["piel"]}"/>
<ellipse cx="250" cy="235" rx="105" ry="122" fill="{p["piel"]}"/>
<ellipse cx="190" cy="282" rx="18" ry="10" fill="#E76F51" opacity="0.25"/>
<ellipse cx="310" cy="282" rx="18" ry="10" fill="#E76F51" opacity="0.25"/>
{pelo_delante(p)}
<path d="M188 205 Q210 194 232 203 M268 203 Q290 194 312 205" stroke="{p["pelo"]}" stroke-width="7" fill="none" stroke-linecap="round"/>
{ojos(p, ojo)}
<path d="M250 250 Q240 276 254 282" stroke="{p["piel_sombra"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
{extra(p)}
{boca(bo)}
</svg>'''


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for pid in PERSONAJES:
        for o in "ac":
            for b in "012":
                (out / f"{pid}_{o}_{b}.svg").write_text(svg(pid, o, b), encoding="utf-8")
    print(f"OK {len(PERSONAJES) * 6} SVG en {out}")


if __name__ == "__main__":
    main()
