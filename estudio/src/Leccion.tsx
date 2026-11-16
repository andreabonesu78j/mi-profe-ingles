import { Audio } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Easing,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

type Camara = { desde: [number, number, number]; hasta: [number, number, number] };
type Escena = {
  tipo: "frase" | "test" | "narracion";
  plano: string | null;
  imagen: string | null;
  audio: string;
  dur: number;
  pausa: number;
  espera?: number;
  n?: number;
  total?: number;
  en?: string;
  es?: string;
  habla?: string;
  paso?: "lenta" | "traduccion" | "normal";
  test?: number;
  cuenta_atras?: boolean;
  camara: Camara;
};
type Datos = { episodio: string; titulo: string; fps: number; escenas: Escena[] };
export type LeccionProps = { episodio: string; datos?: Datos };

const C = {
  crema: "#FBF3E9",
  morado: "#7B3FC4",
  azul: "#1F5FD6",
  rosa: "#E83E8C",
  turquesa: "#1FA3B5",
  mostaza: "#E9A72A",
  tinta: "#2B2340",
};
const FUENTE = "'DejaVu Sans', 'Segoe UI', sans-serif";

const segs = (e: Escena) => e.dur + e.pausa + (e.espera ?? 0);

export const calcularLeccion: CalculateMetadataFunction<LeccionProps> = async ({ props }) => {
  const res = await fetch(staticFile(`${props.episodio}/episodio.json`));
  const datos: Datos = await res.json();
  const frames = datos.escenas.reduce((t, e) => t + Math.round(segs(e) * datos.fps), 0);
  return { durationInFrames: frames + 45, fps: datos.fps, props: { ...props, datos } };
};

/** Tramos visuales: escenas seguidas con el mismo plano comparten imagen y movimiento de cámara. */
const tramos = (escenas: Escena[], fps: number) => {
  const out: { desde: number; frames: number; e: Escena }[] = [];
  let t = 0;
  escenas.forEach((e, i) => {
    const f = Math.round(segs(e) * fps);
    const prev = escenas[i - 1];
    if (prev && prev.plano === e.plano && prev.tipo === e.tipo && out.length) {
      out[out.length - 1].frames += f;
    } else {
      out.push({ desde: t, frames: f, e });
    }
    t += f;
  });
  return out;
};

const Fondo: React.FC<{ e: Escena; frames: number }> = ({ e, frames }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, frames], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) });
  const [s0, x0, y0] = e.camara.desde;
  const [s1, x1, y1] = e.camara.hasta;
  const s = s0 + (s1 - s0) * p;
  const ox = (x0 + (x1 - x0) * p) * 100;
  const oy = (y0 + (y1 - y0) * p) * 100;
  const opacidad = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  const estilo: React.CSSProperties = {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    transform: `scale(${s})`,
    transformOrigin: `${ox}% ${oy}%`,
  };
  if (e.imagen) {
    return (
      <AbsoluteFill style={{ opacity: opacidad }}>
        <Img src={staticFile(e.imagen)} style={estilo} />
      </AbsoluteFill>
    );
  }
  // Marcador provisional hasta que llegue la ilustración de Flow
  const color = [C.turquesa, C.azul, C.rosa, C.morado, C.mostaza][((e.n ?? e.test ?? 0) + (e.plano?.length ?? 0)) % 5];
  const quien = e.tipo === "test" ? "maya" : e.habla && e.habla !== "staff" ? e.habla : "maya";
  return (
    <AbsoluteFill style={{ opacity: opacidad, background: `radial-gradient(circle at 30% 40%, ${C.crema} 0%, ${color} 140%)` }}>
      <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${ox}% ${oy}%` }}>
        <Img
          src={staticFile(`personajes/${quien}.png`)}
          style={{ position: "absolute", height: 900, bottom: -40, left: 1150 - (quien === "maya" ? 60 : 0) }}
        />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 40, bottom: 30, fontFamily: FUENTE, fontSize: 26, color: "#0006" }}>
        {e.plano ?? "—"} · imagen provisional
      </div>
    </AbsoluteFill>
  );
};

const Insignia: React.FC<{ n: number; total: number; color: string }> = ({ n, total, color }) => (
  <div style={{ background: color, color: "white", borderRadius: 22, padding: "10px 22px", fontSize: 40, fontWeight: 800 }}>
    {String(n).padStart(2, "0")}
    <span style={{ opacity: 0.7, fontSize: 28 }}>/{total}</span>
  </div>
);

const Cabecera: React.FC<{ e: Escena }> = ({ e }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entra = spring({ frame, fps, config: { damping: 18 } });
  const etiqueta = e.paso === "lenta" ? "🐢 Despacio" : e.paso === "traduccion" ? "🇪🇸 Significa" : "🔁 ¡Repite!";
  const color = e.habla === "mia" ? C.rosa : e.habla === "maya" ? C.morado : C.azul;
  return (
    <div
      style={{
        position: "absolute",
        top: 40,
        left: 60,
        right: 60,
        display: "flex",
        gap: 24,
        alignItems: "center",
        transform: `translateY(${(1 - entra) * -160}px)`,
        fontFamily: FUENTE,
      }}
    >
      <Insignia n={e.n ?? 0} total={e.total ?? 0} color={color} />
      <div style={{ background: "#FFFFFFF2", borderRadius: 28, padding: "18px 32px", boxShadow: "0 10px 30px #0003", flex: 1 }}>
        <div style={{ fontSize: 62, fontWeight: 800, color: C.tinta, lineHeight: 1.1 }}>{e.en}</div>
        <div style={{ fontSize: 40, color: C.morado, marginTop: 6 }}>{e.es}</div>
      </div>
      <div style={{ background: C.mostaza, color: C.tinta, borderRadius: 18, padding: "10px 18px", fontSize: 30, fontWeight: 700 }}>
        {etiqueta}
      </div>
    </div>
  );
};

const BarraPausa: React.FC<{ desde: number; frames: number; color: string; texto: string }> = ({ desde, frames, color, texto }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [desde, desde + frames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  if (frame < desde) return null;
  return (
    <div style={{ position: "absolute", bottom: 60, left: 460, right: 460, fontFamily: FUENTE, textAlign: "center" }}>
      <div style={{ fontSize: 44, fontWeight: 800, color: "white", textShadow: "0 3px 10px #000a", marginBottom: 12 }}>{texto}</div>
      <div style={{ height: 18, background: "#FFFFFF66", borderRadius: 9 }}>
        <div style={{ width: `${p * 100}%`, height: "100%", background: color, borderRadius: 9 }} />
      </div>
    </div>
  );
};

const Test: React.FC<{ e: Escena }> = ({ e }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const espera = Math.round((e.espera ?? 3) * fps);
  const revelado = frame >= espera;
  const entra = spring({ frame, fps, config: { damping: 15 } });
  const segundos = Math.max(0, Math.ceil((espera - frame) / fps));
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", fontFamily: FUENTE }}>
      <div
        style={{
          background: "#FFFFFFF5",
          borderRadius: 40,
          padding: "40px 70px",
          width: 1300,
          textAlign: "center",
          boxShadow: "0 20px 60px #0004",
          transform: `scale(${0.85 + 0.15 * entra})`,
        }}
      >
        <div style={{ fontSize: 34, fontWeight: 800, color: C.rosa, letterSpacing: 4 }}>MINI-TEST {e.test} · ¿CÓMO SE DICE?</div>
        <div style={{ fontSize: 66, fontWeight: 700, color: C.tinta, margin: "24px 0" }}>{e.es}</div>
        {revelado ? (
          <div style={{ fontSize: 72, fontWeight: 800, color: C.azul }}>{e.en}</div>
        ) : (
          <div style={{ fontSize: 90, fontWeight: 800, color: C.mostaza }}>{segundos}</div>
        )}
      </div>
    </AbsoluteFill>
  );
};

const Titulo: React.FC<{ texto: string }> = ({ texto }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entra = spring({ frame, fps, config: { damping: 14 } });
  const sale = interpolate(frame, [75, 90], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 70, opacity: sale }}>
      <div
        style={{
          fontFamily: FUENTE,
          background: C.morado,
          color: "white",
          fontSize: 64,
          fontWeight: 800,
          textAlign: "center",
          padding: "20px 48px",
          borderRadius: 30,
          transform: `scale(${entra})`,
          boxShadow: "0 12px 40px #0005",
        }}
      >
        <div style={{ fontSize: 30, opacity: 0.8, fontWeight: 600 }}>{texto.split(" — ")[0]}</div>
        <div>{(texto.split(" — ")[1] ?? texto).replace(/ \(.*\)$/, "")}</div>
      </div>
    </AbsoluteFill>
  );
};

export const Leccion: React.FC<LeccionProps> = ({ datos }) => {
  const { fps } = useVideoConfig();
  if (!datos) return null;
  const visual = tramos(datos.escenas, fps);
  let t = 0;
  return (
    <AbsoluteFill style={{ background: C.crema }}>
      {visual.map((v, i) => (
        <Sequence key={`v${i}`} from={v.desde} durationInFrames={v.frames} name={`Plano ${v.e.plano ?? "-"}`}>
          <Fondo e={v.e} frames={v.frames} />
          {i > 0 ? <Audio src={staticFile("sfx/cambio.mp3")} volume={0.25} /> : null}
        </Sequence>
      ))}
      {datos.escenas.map((e, i) => {
        const frames = Math.round(segs(e) * fps);
        const desde = t;
        t += frames;
        const espera = Math.round((e.espera ?? 0) * fps);
        const finAudio = Math.round((e.dur + (e.espera ?? 0)) * fps);
        return (
          <Sequence key={`e${i}`} from={desde} durationInFrames={frames} name={`${e.tipo} ${e.n ?? ""}`}>
            {e.tipo === "frase" ? <Cabecera e={e} /> : null}
            {e.tipo === "frase" && e.paso === "normal" ? (
              <BarraPausa desde={finAudio} frames={frames - finAudio} color={C.mostaza} texto="Tu turno: ¡repítelo!" />
            ) : null}
            {e.tipo === "test" ? <Test e={e} /> : null}
            {e.tipo === "test" ? (
              <Sequence from={espera} layout="none">
                <Audio src={staticFile("sfx/campana.mp3")} volume={0.5} />
              </Sequence>
            ) : null}
            {e.tipo === "narracion" && e.en ? (
              <div style={{ position: "absolute", bottom: 150, width: "100%", textAlign: "center", fontFamily: FUENTE }}>
                <span style={{ background: "#000a", color: "white", fontSize: 54, fontWeight: 800, padding: "10px 28px", borderRadius: 18 }}>
                  {e.en}
                </span>
              </div>
            ) : null}
            {e.cuenta_atras ? (
              <BarraPausa desde={finAudio} frames={frames - finAudio} color={C.rosa} texto="Piensa tu respuesta…" />
            ) : null}
            <Sequence from={espera} layout="none">
              <Audio src={staticFile(e.audio)} />
            </Sequence>
          </Sequence>
        );
      })}
      <Sequence from={0} durationInFrames={90}>
        <Titulo texto={datos.titulo} />
      </Sequence>
    </AbsoluteFill>
  );
};
