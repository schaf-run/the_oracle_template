interface UploadProgressProps {
  percent: number;
}

export function UploadProgress({ percent }: UploadProgressProps) {
  return (
    <div>
      <progress value={percent} max={100} style={{ width: "100%" }} />
      <span>{percent}%</span>
    </div>
  );
}
