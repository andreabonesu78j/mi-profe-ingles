import { Composition } from "remotion";
import { calcularLeccion, Leccion } from "./Leccion";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Leccion"
        component={Leccion}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ episodio: "s01e01-hello-my-name-is" }}
        calculateMetadata={calcularLeccion}
      />
    </>
  );
};
