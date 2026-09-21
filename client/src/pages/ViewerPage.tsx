import { useEffect, useState, type ReactNode } from "react";
import { useParams } from "react-router-dom";
import { ModelViewer } from "../components/ModelViewer";
import { getModel } from "../lib/api";
import type { ModelRecord } from "../types";

type LoadState =
  | { status: "loading" }
  | { status: "ready"; model: ModelRecord }
  | { status: "error"; message: string };

export function ViewerPage() {
  const { id } = useParams<{ id: string }>();
  const [state, setState] = useState<LoadState>({ status: "loading" });

  useEffect(() => {
    if (!id) return;
    setState({ status: "loading" });
    getModel(id)
      .then((model) => setState({ status: "ready", model }))
      .catch((err) => setState({ status: "error", message: err instanceof Error ? err.message : "Not found" }));
  }, [id]);

  if (state.status === "loading") {
    return <CenteredMessage>Loading...</CenteredMessage>;
  }
  if (state.status === "error") {
    return <CenteredMessage>{state.message}</CenteredMessage>;
  }
  return <ModelViewer modelUrl={`/api/models/${state.model.id}/file`} />;
}

function CenteredMessage({ children }: { children: ReactNode }) {
  return (
    <div
      style={{
        width: "100vw",
        height: "100dvh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "sans-serif",
      }}
    >
      {children}
    </div>
  );
}
