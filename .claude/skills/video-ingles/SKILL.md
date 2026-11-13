---
name: video-ingles
description: Produce un vídeo del canal sin cara de inglés para hispanohablantes, de principio a fin — tema, guion revisado por una persona, voces, montaje (vídeo largo 16:9 y Shorts 9:16), título, miniatura, descripción con capítulos y borrador de subida a YouTube. Usa las skills gratis yt-* y solo recurre a vidIQ (de pago) donde no hay alternativa. Usar cuando pidan "haz un vídeo / una lección / un Short sobre X", "siguiente lección", "produce el episodio N" o "sube el vídeo".
---

# Producción de vídeos — canal "Inglés para la vida real"

Convierte un tema (p. ej. "En el médico — A2") en un vídeo listo para publicar.
Antes de empezar lee `docs/01-investigacion-nicho.md` (nicho y palabras clave) y `.claude/youtube/voice.md`
(a quién hablamos, cómo hablamos y qué no prometemos).

## Reglas que no se saltan
1. **Gratis primero.** Cada paso indica la herramienta gratuita. vidIQ cuesta créditos: úsalo solo en los
   pasos marcados 💳, di cuánto cuesta y espera el "sí" del usuario antes de gastar.
2. **Una persona aprueba el guion** antes de generar voces. Es lo que separa el canal del "contenido
   producido en masa" que YouTube desmonetiza.
3. **Nunca publiques sin aprobación explícita.** La privacidad (public/unlisted/private) la elige el usuario.
4. Cada episodio vive en `contenido/<NNN>-<slug>/` (p. ej. `contenido/003-en-el-medico/`). El audio, las
   imágenes y los MP4 no van a git (`.gitignore`); el guion, `escenas.json` y `publicacion.md` sí.
5. Los scripts de las skills `yt-*` están en `.claude/skills/yt-*/`: llámalos con esa ruta.

## Flujo

### 1. Tema — gratis
- Si no hay tema, usa la skill **yt-plan** con `contenido/registro.csv` (lo ya publicado) y la lista de
  situaciones de `docs/01-investigacion-nicho.md` para proponer las 3 siguientes.
- Para ver qué funciona en una situación concreta, usa la skill **yt-viral** (yt-dlp sobre los canales de
  referencia del informe → `swipe.py`). Guarda los 5-10 mejores títulos en `contenido/<ep>/competencia.txt`.
- 💳 Opcional, ~5 créditos: `vidiq_keyword_research` (mode `matching_terms`, language `es`) **solo** si hace
  falta comparar volumen de búsqueda entre dos palabras clave. Es el único dato que no podemos sacar gratis.

### 2. Guion — gratis
- Usa la skill **yt-script** para el gancho: escribe 5 opciones en `ganchos.txt` y puntúalas con
  `python3 .claude/skills/yt-script/hookscore.py ganchos.txt` (adaptado al español; las 21 fórmulas siguen
  detectándose solo en inglés, así que "Unclassified" en español no es un fallo). Elige uno ≥ 55.
- Escribe `guion.md` a partir de `plantillas/guion.md`. Vocabulario según el nivel CEFR, inglés americano
  natural.
- Short: un solo bloque de 3-5 frases o un mini-diálogo de 30-60 s, con el gancho en el primer segundo.

### 3. ⛔ Revisión humana
Muestra el guion y pide al usuario que lo revise y corrija. No sigas hasta que lo apruebe; anota quién y
cuándo en la cabecera.

### 4. Voces
Divide el guion en escenas: una escena = una línea hablada por una sola voz. Guarda los audios en
`audio/NNN.mp3`.
- **Gratis (pendiente de probar en este entorno):** `edge-tts` (voces neuronales de Microsoft, sin clave),
  p. ej. `es-MX-DaliaNeural` para la narradora y `en-US-JennyNeural` / `en-US-GuyNeural` para los
  personajes. Hay que instalarlo con pip; pide permiso al usuario la primera vez.
- 💳 **vidIQ, si lo gratis no suena bien:** `vidiq_voiceover_list_voices` → `vidiq_voiceover_generate`
  (≤ 5000 caracteres por llamada; 28 créditos por cada 1000 caracteres, ≈ 500-620 por un vídeo de 25 min)
  → `vidiq_job_poll` → `curl -sSL -o audio/NNN.mp3 <audioUrl>`.
- Guarda las voces elegidas en `contenido/voces.json` y úsalas siempre (son la "voz" del canal).
- Pausa de repetición: `pausa_entre_escenas` o una escena con silencio
  (`ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 4 -c:a libmp3lame audio/pausa4.mp3`).

### 5. Montaje — gratis
- Rellena `escenas.json` (ver `plantillas/escenas.ejemplo.json`). `imagen` es opcional: sin ella la escena
  usa un fondo de color liso con el texto encima, que es gratis y basta para la mayoría de escenas.
- 💳 Opcional: imágenes de personajes o lugares con `vidiq_generate_thumbnail` (`purpose: "image"`,
  22 créditos cada una). Como mucho 2-4 por vídeo y reutilízalas entre episodios (`contenido/_comun/img/`).
- Monta: `python3 .claude/skills/video-ingles/scripts/montar_video.py contenido/<ep>/escenas.json`
  → `video.mp4`, `subtitulos.srt` y `capitulos.txt`.
- Shorts: usa la skill **yt-shorts** sobre `subtitulos.srt` para elegir 3-5 momentos; para cada uno, copia
  sus escenas a `short-N.json` con `"formato": "vertical"` y `"salida": "short-N.mp4"` (≤ 60 s) y monta.
- Comprueba: saca 2-3 fotogramas (`ffmpeg -ss <t> -i video.mp4 -frames:v 1 f.png`), míralos y revisa la
  duración con `ffprobe`.

### 6. Título, miniatura y descripción — gratis salvo la miniatura
- Título y texto de la miniatura con la skill **yt-package**: valida con
  `python3 .claude/skills/yt-package/title.py --title "..." --thumb "..."` (≤ 60 caracteres, que el título y
  la miniatura no digan lo mismo). Patrón: situación + promesa + nivel, p. ej.
  "Inglés para el MÉDICO 🩺 Frases para principiantes (A2)".
- Capítulos: comprueba `capitulos.txt` con la skill **yt-chapters** (≥ 3 capítulos, el primero 0:00, cada
  uno de ≥ 10 s).
- Descripción y etiquetas con la skill **yt-seo**, dirigidas a la búsqueda real (p. ej. "ingles basico",
  "como hablar ingles"). Incluye los capítulos y el aviso "Voces generadas con IA; guion escrito y revisado
  por nuestro equipo". Todo va a `publicacion.md`.
- Miniatura:
  - Gratis: fotograma del vídeo con texto grande, hecho con ffmpeg (`drawtext` sobre una imagen de 1280x720).
  - 💳 vidIQ (22 créditos), recomendado para los primeros vídeos, donde la miniatura pesa más:
    `vidiq_generate_thumbnail` (landscape, con `title`), siguiendo el estilo de las anteriores.

### 7. Subida
- **Gratis y sin depender de vidIQ:** el usuario sube `video.mp4`, la miniatura y los Shorts en YouTube
  Studio copiando `publicacion.md` (título, descripción, etiquetas y capítulos), y sube `subtitulos.srt` como
  subtítulos. Son unos 5 minutos.
- Con vidIQ (0 créditos, pero necesita la cuenta de vidIQ con el canal conectado): `vidiq_video_upload`
  (`localFile`) → `vidiq_social_account_list` → `vidiq_social_post_draft_create` (YOUTUBE, `categoryId` 27,
  `privacyStatus` preguntado al usuario) → enséñalo → `vidiq_social_post_publish` solo con su "sí".

### 8. Registro y mejora
- Añade una línea a `contenido/registro.csv`:
  `numero,slug,nivel,palabra_clave,titulo,formato,fecha_publicacion,video_id`.
- A los 7 días: pide al usuario la exportación de retención de YouTube Studio y usa la skill **yt-retention**
  con `subtitulos.srt` para ver en qué segundo se va la gente. Apunta la lección en `docs/aprendizajes.md`.
- Comentarios: skill **yt-comment**. Revisión del canal cada mes: skill **yt-audit**.

## Qué hace cada herramienta
| Necesidad | Gratis | 💳 vidIQ (solo si hace falta) |
|---|---|---|
| Qué publicar | yt-plan, yt-viral | — |
| Volumen de búsqueda | — | keyword_research (5) |
| Gancho y guion | yt-script | — |
| Voces | edge-tts (pendiente de probar) | voiceover (28 por cada 1000 caracteres) |
| Imágenes | fondo liso con texto | generate_thumbnail con purpose image (22) |
| Montaje y Shorts | montar_video.py + yt-shorts | — |
| Título, SEO y capítulos | yt-package, yt-seo, yt-chapters | — |
| Miniatura | ffmpeg | generate_thumbnail (22) |
| Subida | YouTube Studio a mano | upload y borrador (0, con cuenta) |
| Análisis | yt-retention, yt-audit, yt-comment | — |
