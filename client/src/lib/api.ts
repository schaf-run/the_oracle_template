import type { ModelRecord } from "../types";

export interface UploadResponse {
  id: string;
  filename: string;
  size: number;
  url: string;
}

// fetch has no upload-progress event; XHR's upload.onprogress is the only
// standard way to report byte-level upload progress to the UI.
export function uploadModel(file: File, onProgress: (percent: number) => void): Promise<UploadResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/models");

    xhr.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        onProgress(Math.round((event.loaded / event.total) * 100));
      }
    });

    xhr.addEventListener("load", () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        try {
          reject(new Error(JSON.parse(xhr.responseText).error ?? "Upload failed"));
        } catch {
          reject(new Error("Upload failed"));
        }
      }
    });

    xhr.addEventListener("error", () => reject(new Error("Upload failed")));

    const formData = new FormData();
    formData.append("file", file);
    xhr.send(formData);
  });
}

export async function getModel(id: string): Promise<ModelRecord> {
  const res = await fetch(`/api/models/${id}`);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error ?? "Model not found");
  }
  return res.json();
}
