---
name: video-ingles
description: Produce un vídeo del canal sin cara de inglés para hispanohablantes, de principio a fin — tema y palabras clave, guion revisado por una persona, voces, imágenes, montaje (vídeo largo 16:9 y Shorts 9:16), título, miniatura, descripción con capítulos y borrador de subida a YouTube con vidIQ. Usar cuando pidan "haz un vídeo / una lección / un Short sobre X", "siguiente lección", "produce el episodio N" o "sube el vídeo".
---

# Producción de vídeos — canal "Inglés para la vida real"

Convierte un tema (p. ej. "En el médico — A2") en un vídeo listo para publicar.
La investigación de nicho y las palabras clave están en `docs/01-investigacion-nicho.md`: léela antes de empezar.

## Reglas que no se saltan
1. **Una persona aprueba el guion antes de gastar créditos en voces o imágenes.** Es lo que separa este canal
   del "contenido producido en masa" que YouTube desmonetiza. Para y pide la aprobación (paso 3).
2. **Nunca publiques sin aprobación explícita.** Crea un borrador, enséñalo y espera el "sí".
   La privacidad (public/unlisted/private) la elige el usuario; no la rellenes tú.
3. **Avisa del coste en créditos de vidIQ antes de cada paso de pago** (tabla al final) y no repitas
   generaciones de pago sin que te lo pidan.
4. Todos los archivos de un episodio van en `contenido/<NNN>-<slug>/` (p. ej. `contenido/003-en-el-medico/`).
   Los audios e imágenes pesados no se suben a git (ver `.gitignore`); el guion, `escenas.json` y `publicacion.md` sí.

## Flujo

### 1. Elegir tema y palabra clave
- Si el usuario no da tema, propón 3 situaciones de la vida real (médico, entrevista de trabajo, banco,
  supermercado, aeropuerto, llamar al casero…) que no estén ya en `contenido/registro.csv`.
- Valida con `vidiq_keyword_research` (mode `matching_terms`, keyword p. ej. "ingles basico", language `es`)
  y con `vidiq_outliers` (keyword del tema, language `es`, `maxSubscribers` 200000) para ver qué títulos
  y duraciones funcionan. Guarda 5-10 títulos de la competencia: se usan en el paso 6.

### 2. Escribir el guion
- Llama primero a `vidiq_before_scripts_outlines_and_edits` con la petición literal, `language: "es"`,
  `format` ("lección con diálogo") y la duración pedida. Sigue su guía.
- Escribe `guion.md` a partir de `plantillas/guion.md`. Vocabulario y gramática ajustados al nivel CEFR;
  inglés americano natural; nada de traducciones literales raras.
- Short: un solo bloque de 3-5 frases o 1 mini-diálogo, 30-60 s, gancho en el primer segundo.

### 3. ⛔ Revisión humana
Muestra el guion y pide al usuario que lo revise y corrija. No sigas hasta que lo apruebe; anota quién y
cuándo en la cabecera del guion.

### 4. Voces
- `vidiq_voiceover_list_voices` → elige (y guarda en `contenido/voces.json` para reutilizarlas siempre):
  una voz de narradora en español y dos voces en inglés americano para los personajes.
- Divide el guion en escenas: una escena = una línea hablada por una sola voz (o la frase EN lenta + normal).
  Cada llamada a `vidiq_voiceover_generate` admite como máximo 5000 caracteres.
- Para cada escena: `vidiq_voiceover_generate` → `vidiq_job_poll` hasta `completed` → descarga el MP3 con
  `curl -sSL -o audio/NNN.mp3 <audioUrl>`.
- Para las pausas de repetición basta con `pausa_entre_escenas` o con una escena extra con audio de silencio:
  `ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 4 -c:a libmp3lame audio/pausa4.mp3`.

### 5. Imágenes y montaje
- Imágenes de escena: `vidiq_generate_thumbnail` con `purpose: "image"`, `orientation` `landscape`
  (o `portrait` para Shorts). Crea primero una imagen de los personajes y pásala en `referenceImages`
  en las demás para que se mantengan iguales. Basta con 4-8 imágenes por vídeo (una por lugar o momento).
  Descarga cada `imageUrl` a `img/`.
- Opcional: música con `vidiq_generate_music`, guardada como `musica.mp3`.
- Rellena `escenas.json` (ver `plantillas/escenas.ejemplo.json`): cada escena lleva `imagen`, `audio`,
  `texto_en` y/o `texto_es` en pantalla y, si empieza un bloque, `capitulo`.
- Monta: `python3 .claude/skills/video-ingles/scripts/montar_video.py contenido/<ep>/escenas.json`
  → `video.mp4`, `subtitulos.srt` y `capitulos.txt`.
- Shorts: copia el JSON con `"formato": "vertical"`, `"salida": "short-1.mp4"` y solo 3-6 escenas del
  bloque 1 (≤ 60 s). Saca 3-5 Shorts por vídeo largo.
- Comprueba el resultado: saca 2-3 fotogramas con `ffmpeg -ss <t> -i video.mp4 -frames:v 1 f.png`
  y míralos; revisa con `ffprobe` que la duración cuadra.

### 6. Título, miniatura y descripción
- `vidiq_generate_titles` (`language: "es"`, `regionCode: "MX"`, `numTitles: 5`, `competitorTitles` del
  paso 1, `previousTitles` del registro) → compara con `vidiq_score_title` → elige con el usuario.
  Patrón que funciona: situación + promesa + nivel, p. ej. "Inglés para el MÉDICO 🩺 Frases y diálogo
  para principiantes (A2)".
- Miniatura: `vidiq_generate_thumbnail` (landscape, con `title`) usando el estilo de miniaturas
  anteriores en `referenceImages`; enséñala con `vidiq_youtube_preview`.
- Escribe `publicacion.md` con: título, descripción (2 líneas con la palabra clave, lista de frases,
  `capitulos.txt` pegado, enlace a la lista de reproducción del nivel, aviso "Voces generadas con IA;
  guion escrito y revisado por nuestro equipo"), 10-15 etiquetas y lista de reproducción.

### 7. Subida (borrador) y publicación
- `vidiq_video_upload` con `localFile` (path, sizeBytes de `wc -c`, `video/mp4`) → ejecuta el comando que
  devuelve → vuelve a llamar con `uploadId` hasta que esté listo. Igual para cada Short.
- Miniatura: súbela con `vidiq_upload_image` y usa su id como `thumbnailImageId`.
- `vidiq_social_account_list` (platform `YOUTUBE`, `canPublishOnly`) → `vidiq_social_post_draft_create`
  con destino YOUTUBE: `title`, `text` (descripción), `tags`, `categoryId` 27 (Educación),
  `thumbnailImageId`, `publishAt` si quiere programarlo y `privacyStatus` **preguntado al usuario**.
- Enseña el borrador. Solo con su aprobación: `vidiq_social_post_publish`.
- Si no hay ningún canal conectado: `vidiq_connect_youtube_channel` y espera a que el usuario autorice.

### 8. Registro
Añade una línea a `contenido/registro.csv`:
`numero,slug,nivel,palabra_clave,titulo,formato,fecha_publicacion,video_id`

## Costes orientativos (créditos vidIQ)
| Paso | Coste |
|---|---|
| Investigación (keyword research, outliers, títulos, score) | 5 por llamada |
| Voz | 28 por cada 1000 caracteres (guion de 25 min ≈ 18-22 K caracteres ≈ 500-620) |
| Imagen o miniatura | 22 por imagen |
| `vidiq_compose` (no hace falta: montamos con ffmpeg) | 1 por cada 4 s |
| Subida, borrador, publicación en YouTube | 0 |

Consulta el saldo con `vidiq_balance` antes de un episodio completo.
