import { useState } from "react";
import { UploadForm } from "../components/UploadForm";
import { UploadProgress } from "../components/UploadProgress";
import { ShareLink } from "../components/ShareLink";
import { uploadModel } from "../lib/api";

type UploadState =
  | { status: "idle" }
  | { status: "uploading"; percent: number }
  | { status: "success"; id: string }
  | { status: "error"; message: string };

export function UploadPage() {
  const [state, setState] = useState<UploadState>({ status: "idle" });

  const handleSubmit = async (file: File) => {
    setState({ status: "uploading", percent: 0 });
    try {
      const result = await uploadModel(file, (percent) => setState({ status: "uploading", percent }));
      setState({ status: "success", id: result.id });
    } catch (err) {
      setState({ status: "error", message: err instanceof Error ? err.message : "Upload failed" });
    }
  };

  return (
    <div style={{ maxWidth: 480, margin: "4rem auto", padding: "0 1rem" }}>
      <h1>Upload a 3D model</h1>
      <p>.obj files up to 500MB</p>
      <UploadForm onSubmit={handleSubmit} disabled={state.status === "uploading"} />
      {state.status === "uploading" && <UploadProgress percent={state.percent} />}
      {state.status === "success" && <ShareLink id={state.id} />}
      {state.status === "error" && <p style={{ color: "crimson" }}>{state.message}</p>}
    </div>
  );
}
