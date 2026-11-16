# Cómo hace sus vídeos la competencia (análisis visual con vidIQ, 2026-11-16)

Vídeos analizados de principio a fin:
- **Inglés Express — "50 Most Used Phrases at Work"** (341 K vistas, su vídeo más visto; personajes 3D fijos y un gato mascota).
- **Escucha y Habla Inglés — "Un día en la vida de una ama de casa"** (141 K vistas, 10× la media de su canal).

## Lo que descubrimos
**Ninguno usa animación completa.** No hay movimiento de labios ni de cuerpo. La sensación de "vídeo animado" sale de:
1. **Muchas ilustraciones distintas.** Cada situación tiene su propia imagen (personaje explicando, encogiéndose de
   hombros, en la cocina, en la caja…). Los personajes "actúan" porque **cambian de pose y de escena**.
2. **Cortes cada 3-5 segundos** entre ilustraciones, primeros planos y tarjetas.
3. **Movimiento de cámara** sobre cada imagen: zoom lento, paneo, deslizamiento (efecto Ken Burns).
4. **Gráficos encima**: cabecera con número y frase ("01. Can I ask you something?"), etiqueta de categoría
   arriba a la derecha, tarjetas de capítulo, transiciones de "pasar página".
5. **Sonido**: música lo-fi suave todo el vídeo, sonido de página y una campanita en los tests.
6. **Mascota recurrente** (el gato gruñón) que da personalidad.

## Estructura didáctica que repiten
- Gancho de 7-15 s con el problema ("cuando alguien te habla rápido en el trabajo y no sabes qué decir").
- Cada frase en pantalla 8-12 s: traducción → inglés normal → inglés lento → "Repeat after me".
- **Mini-test cada 5 frases**: aparece la frase en español, 3 s de silencio para recordarla, campanita y respuesta.
- Repaso inverso al final (inglés → español).
- Variante del otro canal: **modos de escucha** (sin subtítulos → con subtítulos → frase a frase → test) y
  subtítulos dobles (inglés destacado en color, español encima en blanco), con la palabra que suena resaltada.

## Qué cambiamos en nuestro canal
| Antes (vídeo preliminar) | Ahora |
|---|---|
| 1 imagen fija de los 3 personajes durante 4 min | **1 ilustración por frase o situación** (unas 25 por episodio), con los personajes actuando |
| Sin movimiento | Zoom/paneo lento en cada imagen y corte en cada frase |
| Solo subtítulos | Cabecera "01/20 + frase", etiqueta de tema, tarjetas de sección |
| Sin tests | **Mini-test cada 5 frases** (español → pausa → respuesta) |
| Sin música | Música suave + sonidos de página y campanita |
| — | Mascota del canal (por decidir) |

Las ilustraciones salen de **Google Flow** con las hojas de personajes como referencia (lista de planos y
prompts en `contenido/<ep>/planos.md`). El montaje (cámara, cortes, rótulos, tests y sonido) lo hago yo con
Remotion y FFmpeg. Para momentos clave (intro y diálogo) se pueden añadir 2-3 clips de vídeo de 8 s hechos
con Veo en Flow, donde los personajes sí se mueven y hablan.
