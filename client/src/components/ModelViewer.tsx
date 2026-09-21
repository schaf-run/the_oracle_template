import { useRef, type CSSProperties } from "react";
import { useThreeScene } from "../hooks/useThreeScene";

interface ModelViewerProps {
  modelUrl: string;
}

export function ModelViewer({ modelUrl }: ModelViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const { isLoading, error } = useThreeScene(containerRef, modelUrl);

  return (
    <div style={{ position: "relative", width: "100vw", height: "100dvh" }}>
      <div ref={containerRef} style={{ width: "100%", height: "100%", touchAction: "none" }} />
      {isLoading && !error && (
        <div style={overlayStyle}>Loading model...</div>
      )}
      {error && <div style={overlayStyle}>Failed to load model: {error}</div>}
    </div>
  );
}

const overlayStyle: CSSProperties = {
  position: "absolute",
  inset: 0,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  color: "white",
  background: "rgba(0,0,0,0.4)",
  fontFamily: "sans-serif",
};
