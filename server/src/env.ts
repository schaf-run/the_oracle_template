import "dotenv/config";
import path from "node:path";

export const env = {
  port: Number(process.env.PORT ?? 3001),
  storageDir: path.resolve(process.cwd(), process.env.STORAGE_DIR ?? "./storage"),
  // 500 MB default, matches .env.example
  maxUploadBytes: Number(process.env.MAX_UPLOAD_BYTES ?? 524288000),
};
