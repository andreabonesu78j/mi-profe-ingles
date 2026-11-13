# Prompts para crear los personajes (Google Flow / LM Arena)

Los prompts van en inglés porque los modelos de imagen y vídeo rinden mejor así. Las explicaciones están
en español. Copia cada bloque tal cual.

## Cómo trabajar (importante para que los personajes no cambien de cara)
1. **Primero la imagen maestra** de cada personaje (prompt A). Genera 4-8 variantes y quédate con la mejor.
2. **Después, todas las demás imágenes se hacen EDITANDO la imagen maestra** (subirla como referencia o
   "ingrediente" en Flow, o como imagen de entrada en un modelo de edición de LM Arena). Nunca vuelvas a
   generar desde cero: la cara cambiaría.
3. **Mismo encuadre siempre**: para animarlos yo necesito que las variantes (boca abierta, ojos cerrados…)
   estén en la misma posición exacta. Por eso todos los prompts de edición dicen "same framing".
4. **Fondo verde liso** (#00FF00) en los personajes: así yo los recorto automáticamente y los pongo sobre
   cualquier escenario.
5. Descarga en PNG a la máxima resolución y guárdalos con estos nombres (yo los cargo con el script):
   `sofia_neutral.png`, `sofia_boca1.png`, `sofia_boca2.png`, `sofia_ojos_cerrados.png`, `sofia_feliz.png`…

---

## Estilo común (va dentro de cada prompt A)
```
Modern high-end 3D animated feature film style, stylized but believable proportions, expressive large eyes,
detailed skin with subtle subsurface scattering, soft cinematic studio lighting with warm key light and cool
rim light, realistic hair strands and fabric textures, friendly and warm mood, sharp focus, 4K render.
```
Si prefieres algo más realista, cambia la primera línea por:
`Photorealistic digital human, natural skin texture, shot on 85mm lens, shallow depth of field,`

---

## 1. Sofía — la alumna (recién llegada a EE. UU.)

**A. Imagen maestra**
```
Character portrait of Sofía, a 28-year-old Latina woman from Mexico who just moved to the United States.
Warm medium-tan skin, long wavy dark-brown hair with soft caramel highlights, big expressive brown eyes,
friendly hopeful smile, small gold hoop earrings. Wearing a mustard-yellow knit cardigan over a teal t-shirt.
Medium shot from the waist up, facing the camera, shoulders slightly turned, centered, looking at the viewer.
Modern high-end 3D animated feature film style, stylized but believable proportions, expressive large eyes,
detailed skin with subtle subsurface scattering, soft cinematic studio lighting with warm key light and cool
rim light, realistic hair strands and fabric textures, friendly and warm mood, sharp focus, 4K render.
Plain solid pure green background (#00FF00), no shadows on the background, no text, no logo.
```

## 2. Mike — el vecino y compañero de trabajo estadounidense

**A. Imagen maestra**
```
Character portrait of Mike, a 35-year-old American man, friendly neighbor and coworker. Light skin with a
few freckles, short tousled chestnut-brown hair, well-groomed short beard, blue-gray eyes, relaxed confident
grin. Wearing a dark navy hoodie with white drawstrings over a gray t-shirt.
Medium shot from the waist up, facing the camera, centered, looking at the viewer.
Modern high-end 3D animated feature film style, stylized but believable proportions, expressive large eyes,
detailed skin with subtle subsurface scattering, soft cinematic studio lighting with warm key light and cool
rim light, realistic hair strands and fabric textures, friendly and warm mood, sharp focus, 4K render.
Plain solid pure green background (#00FF00), no shadows on the background, no text, no logo.
```

## 3. Profe Luz — la narradora (explica en español)

**A. Imagen maestra**
```
Character portrait of Profe Luz, a 40-year-old Afro-Latina English teacher, warm and encouraging.
Deep brown skin, natural curly black hair gathered in a high bun with a few loose curls, stylish round
tortoiseshell glasses, bright smile, small silver earrings. Wearing a plum-purple blazer over a white blouse,
holding a small tablet.
Medium shot from the waist up, facing the camera, centered, looking at the viewer.
Modern high-end 3D animated feature film style, stylized but believable proportions, expressive large eyes,
detailed skin with subtle subsurface scattering, soft cinematic studio lighting with warm key light and cool
rim light, realistic hair strands and fabric textures, friendly and warm mood, sharp focus, 4K render.
Plain solid pure green background (#00FF00), no shadows on the background, no text, no logo.
```

---

## B. Variantes para animar (editando la imagen maestra)
Sube la imagen maestra y usa estos prompts uno por uno. Cambia `[NAME]` por Sofía, Mike o Profe Luz.

| Archivo | Prompt de edición |
|---|---|
| `_boca1.png` | `Edit this image: keep exactly the same character, pose, framing, lighting and green background. Only change the mouth: slightly open, as if saying "eh", teeth barely visible.` |
| `_boca2.png` | `Edit this image: keep exactly the same character, pose, framing, lighting and green background. Only change the mouth: wide open, as if saying "ah" while talking, upper teeth and tongue visible.` |
| `_ojos_cerrados.png` | `Edit this image: keep exactly the same character, pose, framing, lighting and green background. Only change the eyes: fully closed, relaxed, mid-blink. Mouth closed with a soft smile.` |
| `_feliz.png` | `Edit this image: keep the same character, framing, lighting and green background. Expression: big genuine laugh, eyes slightly squinted with joy, cheeks raised.` |
| `_sorprendida.png` | `Edit this image: keep the same character, framing, lighting and green background. Expression: pleasantly surprised, eyebrows raised, eyes wide, mouth in a small "oh".` |
| `_pensando.png` | `Edit this image: keep the same character, framing, lighting and green background. Expression: thinking, looking up to the side, one hand touching the chin, lips pressed.` |
| `_preocupada.png` | `Edit this image: keep the same character, framing, lighting and green background. Expression: slightly worried and confused, eyebrows pulled together, small nervous smile.` |
| `_saluda.png` | `Edit this image: keep the same character, framing, lighting and green background. Pose: waving hello with the right hand at shoulder height, friendly smile.` |

Para la Profe Luz añade además:
- `_explica.png`: `... Pose: explaining, right hand open palm up at chest height, encouraging smile.`
- `_bien.png`: `... Pose: thumbs up with the right hand, proud smile.`

**Mínimo para empezar:** neutral + boca1 + boca2 + ojos cerrados de cada personaje (12 imágenes).
Las expresiones las uso en momentos concretos del guion (Sofía preocupada antes de una frase, feliz al
entenderla…).

---

## C. Escenarios (16:9, sin personajes)
Estilo común para pegar al final de cada uno:
```
Modern high-end 3D animated feature film style, soft warm cinematic lighting, rich details, slight depth of
field, no people, no text, no logos, 16:9, 4K.
```

| Archivo | Prompt |
|---|---|
| `aula.png` | `Cozy modern English classroom for adults, large clean green chalkboard on the left half of the frame, empty, warm wooden shelves with books and plants on the right, big window with afternoon sunlight.` |
| `pasillo.png` | `Hallway of a friendly mid-rise apartment building in the United States, two wooden apartment doors labeled 3A and 3B, warm wall lights, a potted plant, carpeted floor, eye-level camera.` |
| `supermercado.png` | `Aisle of a bright American supermarket, colorful shelves with groceries, checkout counter visible in the background, eye-level camera.` |
| `banco.png` | `Modern bank branch lobby in the United States, teller counter with a glass partition, waiting chairs, plants, eye-level camera.` |
| `parada_bus.png` | `City bus stop on a sunny American street, bench with a shelter, bus route map, trees and brick buildings in the background, eye-level camera.` |
| `consultorio.png` | `Reception desk of a small medical clinic in the United States, clean and modern, waiting area chairs, eye-level camera.` |
| `oficina.png` | `Small modern warehouse office in the United States, desk with computer, safety posters without readable text, large window to the warehouse floor.` |

Para la **lección 1 (Tu primera semana en EE. UU.)** bastan: `aula`, `pasillo`, `supermercado`, `banco` y `parada_bus`.

---

## D. Opcional: clips animados con Veo (Google Flow)
Flow puede hacer clips de 8 s con los personajes moviéndose y hablando con voz propia. Son caros en
créditos y la voz puede cambiar de un clip a otro, así que úsalos solo para **la intro y el diálogo
principal**. El resto del vídeo (frases, repeticiones y repaso) lo animo yo con las imágenes de arriba.

Usa las imágenes maestras como "ingredientes" y este tipo de prompt:
```
Animated 3D feature-film style scene in the apartment hallway (doors 3A and 3B). Mike (from the reference)
opens the door of 3B and waves at Sofía (from the reference), who is holding a moving box. Mike says in a
friendly American voice: "Hi! I'm Mike. I live in 3B." Sofía smiles and answers with a slight Mexican
accent: "Nice to meet you, Mike. I'm Sofía. I just moved in." Natural lip-sync, warm lighting, medium shot,
eye-level camera, no subtitles, no music.
```
```
Animated 3D feature-film style scene in a bright English classroom. Profe Luz (from the reference) stands
next to an empty green chalkboard, smiles at the camera and says warmly in Mexican Spanish:
"¡Hola! Soy la Profe Luz. Bienvenidos a Inglés para la vida real." Natural lip-sync, gentle hand gesture,
medium shot, no subtitles, no music.
```

---

## Cuando los tengas
Súbelos al chat o al repositorio en `contenido/_comun/personajes_v2/` y `contenido/_comun/fondos_v2/`.
Yo me encargo de:
1. Quitar el fondo verde y alinear las variantes.
2. Adaptar la animación: boca sincronizada con la voz, parpadeo, cambio de expresión según el guion y un
   leve movimiento de cámara (zoom lento) para que se sienta vivo.
3. Hacer de nuevo el vídeo de presentación con los personajes nuevos, antes de escribir el guion completo.
