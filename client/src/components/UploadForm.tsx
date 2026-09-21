import { useState } from "react";

interface UploadFormProps {
  onSubmit: (file: File) => void;
  disabled: boolean;
}

export function UploadForm({ onSubmit, disabled }: UploadFormProps) {
  const [file, setFile] = useState<File | null>(null);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (file) onSubmit(file);
      }}
    >
      <input
        type="file"
        accept=".obj"
        disabled={disabled}
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      <button type="submit" disabled={disabled || !file}>
        Upload
      </button>
    </form>
  );
}
