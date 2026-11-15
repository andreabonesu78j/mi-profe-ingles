# Prompts para los assets de animación (Google Flow / LM Arena)

Las hojas que ya tenemos son perfectas como **referencia**, pero son muy pequeñas para vídeo (cada cara mide
~100 px). Para animar necesito imágenes sueltas y grandes. Adjunta SIEMPRE la hoja del personaje
(`characters/<id>/hoja-ref.png` o la hoja completa) como referencia.

## 0. Primero: Leo y Mia como adultos (el canal es para adultos)
Adjunta la hoja actual del personaje como referencia y usa:
```
[GLOBAL VISUAL STYLE de characters/master-style.md]
Using the supplied reference, redesign this character as an adult in their mid-20s, keeping the same
recognizable face, hairstyle, skin tone, eye color and personality, and exactly the same official outfit
and colors. Adult proportions: taller body, longer limbs, adult facial structure, no childlike features.
Full body, front view, neutral standing pose, plain light beige background, no text, no logos.
```
Cuando te guste el resultado, guárdalo como `characters/<id>/reference.png`: será la nueva referencia oficial
para todo lo demás (también para hacer su hoja de giro y expresiones con los prompts de ChatGPT).

## 1. Imagen base de animación (una por personaje)
```
[GLOBAL VISUAL STYLE de characters/master-style.md]
[Prompt de identidad de characters/<id>/identity.md]
Using the supplied reference, render this exact character from the waist up, facing the camera,
centered, relaxed natural pose, arms down, mouth closed with a soft smile, eyes open looking at the viewer.
Plain solid pure green background (#00FF00), no shadow on the background, high resolution.
```
Guárdala como `characters/<id>/anim/<id>_base_neutral.png`.

## 2. Variantes para hablar y parpadear (EDITANDO la imagen base, no generando de nuevo)
| Archivo | Prompt de edición |
|---|---|
| `<id>_base_boca1.png` | `Edit this image. Keep exactly the same character, pose, framing, lighting and green background. Only change the mouth: slightly open, as if saying "eh".` |
| `<id>_base_boca2.png` | `Edit this image. Keep exactly the same character, pose, framing, lighting and green background. Only change the mouth: wide open, as if saying "ah" while talking.` |
| `<id>_base_ojos.png` | `Edit this image. Keep exactly the same character, pose, framing, lighting and green background. Only change the eyes: fully closed, mid-blink.` |

## 3. Expresiones de reacción (misma imagen base, editada)
`feliz`, `sorpresa`, `confundido`, `pensando`, `preocupado`, `celebra`:
```
Edit this image. Keep the same character, outfit, framing, lighting and green background.
Change the expression to: [happy and laughing | very surprised | confused, one eyebrow raised |
thinking with one hand on the chin | worried | celebrating with both fists up].
```
Nombres: `<id>_base_feliz.png`, `<id>_base_sorpresa.png`…

## 4. Mínimo para el primer episodio
4 imágenes por personaje (neutral, boca1, boca2, ojos) = **12 imágenes**. Las expresiones pueden llegar después.

## 5. Escenarios (16:9, sin personajes)
```
[GLOBAL VISUAL STYLE] Empty [classroom with a large green chalkboard on the left half | school hallway
with lockers | kitchen of a family home | small supermarket aisle | city park], eye-level camera, soft
depth of field, no people, no text, 16:9, high resolution.
```
Guárdalos en `locations/<nombre>.png`.
