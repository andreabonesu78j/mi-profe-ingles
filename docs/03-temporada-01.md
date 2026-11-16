# Temporada 1 — "Inglés para la vida real" (A1, inglés americano)

Plan de 10 episodios propuesto con ChatGPT, adaptado al público adulto del canal y a los personajes que ya
existen (Miss Maya, Leo y Mia). Los personajes nuevos de ese plan (Alex, Sophie, Nico, Clara, Ben) se
quedan como "solo voz" hasta que tengan hoja de personaje y voz propias.

## Reglas de producción
- **≤ 2.500 caracteres de ElevenLabs por episodio** (unos 5-6 min de vídeo) → 4 episodios caben en 10.000
  caracteres. Se comprueba con `python3 .claude/skills/video-ingles/scripts/guion_a_lineas.py <guion.md>`.
- 20 frases por episodio: inglés lento → traducción de Miss Maya → inglés normal → pausa.
- Cada episodio termina anunciando el siguiente.

## Episodios
| # | Título | Tema | Personajes | Estado |
|---|---|---|---|---|
| 01 | Hello! My name is… | 20 frases básicas para cualquier lugar | Maya, Leo, Mia | ✅ guion (2.092 car.) |
| 02 | Numbers and Age | números 1-100, edad, teléfono, dirección | Maya, Leo | ✏️ por escribir |
| 03 | At the Hotel | registrarse, pedir cosas, quejarse | Leo + recepcionista (voz; futuro Alex) | ✏️ por escribir |
| 04 | At the Supermarket | encontrar productos, pagar en la caja | Leo, Mia + cajera (voz; futura Sophie) | ✅ guion (2.225 car.) |
| 05 | My Family | presentar a tu familia, estado civil, hijos | Maya, Leo (futuro Nico) | ✏️ por escribir |
| 06 | At the Restaurant | pedir mesa, pedir comida, la cuenta | Mia + mesero (voz; futuro Ben) | ✏️ por escribir |
| 07 | At the Hospital | qué te duele, citas, farmacia | Leo + recepcionista (voz; futura Clara) | ✏️ por escribir |
| 08 | Colors and Objects | colores y objetos de casa y trabajo | Maya, Leo | ✏️ por escribir |
| 09 | Asking for Directions | autobús, direcciones, perderse | Leo, Mia + chofer (voz) | ✅ guion (2.196 car.) |
| 10 | My First English Conversation | conocer a tu vecina, el edificio | Leo, Mia | ✅ guion (2.428 car.) |

Los cuatro guiones listos salen de la antigua lección 1 (100 frases), dividida en partes. El bloque del
**banco** queda guardado para la temporada 2 en `contenido/_reserva/banco.md`.

## Presupuesto de voz
| Lote | Episodios | Caracteres |
|---|---|---|
| Ya escritos | 01, 04, 09, 10 | 8.941 |
| Siguiente lote | 02, 03, 05, 06 | ~9.000 (estimado) |
| Último lote | 07, 08 | ~4.500 (estimado) |

**Orden de publicación recomendado:** 01 → 02 → 03 → … → 10. Conviene producir ya el 01 y escribir el
02 y el 03 mientras tanto, para publicar en orden.
