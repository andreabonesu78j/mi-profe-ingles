#!/usr/bin/env python3
"""Fondos del canal en SVG (1920x1080). Uso: python3 fondos.py <carpeta_salida>"""
import sys
from pathlib import Path

FONDOS = {
    # Aula de la Profe Luz: pared clara, pizarra verde a la izquierda
    "aula": '''<rect width="1920" height="1080" fill="#F6EFE4"/>
<rect y="860" width="1920" height="220" fill="#C9A27E"/>
<rect y="850" width="1920" height="14" fill="#A7825F"/>
<rect x="110" y="140" width="1050" height="600" rx="18" fill="#7A5134"/>
<rect x="135" y="165" width="1000" height="550" rx="8" fill="#2F5D50"/>
<rect x="150" y="740" width="970" height="18" rx="6" fill="#7A5134"/>
<rect x="300" y="728" width="60" height="14" rx="4" fill="#fff"/>
<rect x="1300" y="160" width="150" height="150" rx="75" fill="#fff" stroke="#264653" stroke-width="10"/>
<path d="M1375 235 L1375 180 M1375 235 L1415 255" stroke="#264653" stroke-width="8" stroke-linecap="round"/>
<rect x="1700" y="560" width="120" height="300" rx="14" fill="#E9C46A"/>
<path d="M1760 560 Q1700 430 1640 470 M1760 560 Q1760 410 1800 440 M1760 560 Q1830 460 1880 500" stroke="#2A9D8F" stroke-width="22" fill="none" stroke-linecap="round"/>''',
    # Pasillo de un edificio de apartamentos: dos puertas
    "pasillo": '''<rect width="1920" height="1080" fill="#DCE8EE"/>
<rect y="0" width="1920" height="70" fill="#C3D5DE"/>
<rect y="860" width="1920" height="220" fill="#8C6A52"/>
<rect y="850" width="1920" height="14" fill="#6E513E"/>
<g><rect x="230" y="250" width="320" height="600" rx="10" fill="#9C5B3B"/>
<rect x="265" y="290" width="250" height="230" rx="8" fill="#B06E4C"/><rect x="265" y="560" width="250" height="250" rx="8" fill="#B06E4C"/>
<circle cx="510" cy="560" r="14" fill="#E9C46A"/><rect x="345" y="200" width="90" height="40" rx="8" fill="#264653"/>
<text x="390" y="230" font-family="DejaVu Sans" font-weight="bold" font-size="28" fill="#fff" text-anchor="middle">3A</text></g>
<g><rect x="1370" y="250" width="320" height="600" rx="10" fill="#9C5B3B"/>
<rect x="1405" y="290" width="250" height="230" rx="8" fill="#B06E4C"/><rect x="1405" y="560" width="250" height="250" rx="8" fill="#B06E4C"/>
<circle cx="1390" cy="560" r="14" fill="#E9C46A"/><rect x="1485" y="200" width="90" height="40" rx="8" fill="#264653"/>
<text x="1530" y="230" font-family="DejaVu Sans" font-weight="bold" font-size="28" fill="#fff" text-anchor="middle">3B</text></g>
<rect x="880" y="160" width="160" height="40" rx="20" fill="#FFF3C4"/>
<path d="M960 70 L960 160" stroke="#555" stroke-width="6"/>
<rect x="900" y="700" width="120" height="160" rx="12" fill="#E76F51"/>
<path d="M960 700 Q900 590 850 620 M960 700 Q960 570 1000 600 M960 700 Q1030 610 1070 640" stroke="#2A9D8F" stroke-width="20" fill="none" stroke-linecap="round"/>''',
}


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for nombre, cuerpo in FONDOS.items():
        (out / f"{nombre}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">{cuerpo}</svg>',
            encoding="utf-8")
    print(f"OK {len(FONDOS)} fondos en {out}")


if __name__ == "__main__":
    main()
