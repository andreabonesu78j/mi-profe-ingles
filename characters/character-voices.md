# Voces de los personajes (inglés americano)

Motor principal: **ElevenLabs** (modelo `eleven_multilingual_v2`, habla español e inglés con la misma voz).
La clave está guardada en el entorno; el proxy la añade sola. Respaldo gratis: Piper.

| Personaje | Voz ElevenLabs (candidata) | voice_id | Clave en `contenido/voces.json` |
|---|---|---|---|
| Miss Maya | Matilda | `XrExE9yKIg1WjnnlVkGX` | `maya` |
| Leo | Liam (alternativa: Will `bIHbv24MWmeRgasZH58o`) | `TX3LPaxmHKxFdv7VOQHJ` | `leo`, `leo_lenta` |
| Mia | Jessica (alternativa: Laura `FGY2WhTYpPnrIDTdsKH5`) | `cgSgspJ2msm6clMCkdW9` | `mia`, `mia_lenta` |
| Personal (cajera, banco, chofer), solo voz | George (provisional) | `JBFqnCBsd6RMkjVDRZzb` | `staff` |

`_lenta` = velocidad 0,8 para la versión de "repite conmigo".
Una vez elegidas, **no se cambian**: la voz es parte de la identidad del personaje.

## Límites de la clave actual
- Puede generar audio con las voces estándar de ElevenLabs.
- No tiene permiso para listar voces (`voices_read`) ni para leer la suscripción.
- Las voces de la biblioteca de la comunidad piden un plan de pago (la prueba con una devolvió `paid_plan_required`).
- Revisa el plan: para un canal monetizado hace falta un plan con licencia comercial, y un episodio de
  25 min son unos 20-25 mil caracteres.
