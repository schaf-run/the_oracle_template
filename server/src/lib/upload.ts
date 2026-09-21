import busboy from "busboy";
import { randomUUID } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import type { Request } from "express";
import { env } from "../env";

export interface UploadResult {
  id: string;
  filename: string;
  filepath: string;
  size: number;
}

export type UploadOutcome =
  | { ok: true; result: UploadResult }
  | { ok: false; status: 400 | 413 | 500; error: string };

const OBJ_EXTENSION = /\.obj$/i;

export function handleUpload(req: Request): Promise<UploadOutcome> {
  return new Promise((resolve) => {
    let settled = false;
    const settle = (outcome: UploadOutcome) => {
      if (settled) return;
      settled = true;
      resolve(outcome);
    };

    const bb = busboy({
      headers: req.headers,
      limits: { files: 1, fileSize: env.maxUploadBytes },
    });

    let sawFile = false;
    let writeTarget: { id: string; filename: string; targetPath: string } | null = null;
    let writeStream: fs.WriteStream | null = null;

    const unlinkPartialFile = () => {
      if (writeTarget) {
        fs.unlink(writeTarget.targetPath, () => {});
      }
    };

    // fs.createWriteStream opens the file asynchronously, so destroying it
    // and unlinking immediately races the still-pending open() and can leave
    // an orphaned empty file. Waiting for 'close' guarantees the fd lifecycle
    // (open-then-closed, or destroyed-before-open-completed) has settled.
    const destroyAndCleanup = () => {
      if (!writeStream) return;
      writeStream.once("close", unlinkPartialFile);
      writeStream.destroy();
    };

    bb.on("file", (_fieldname, stream, info) => {
      sawFile = true;

      if (!OBJ_EXTENSION.test(info.filename)) {
        settle({ ok: false, status: 400, error: "Only .obj files are supported" });
        stream.resume(); // drain without saving
        return;
      }

      const id = randomUUID();
      const targetPath = path.join(env.storageDir, `${id}.obj`);
      writeTarget = { id, filename: info.filename, targetPath };
      writeStream = fs.createWriteStream(targetPath);

      stream.on("limit", () => {
        destroyAndCleanup();
        settle({ ok: false, status: 413, error: "File exceeds 500MB limit" });
      });

      writeStream.on("finish", () => {
        // Write stream 'finish' guarantees data is flushed to disk — busboy's
        // own 'finish' can fire before this and would race a premature stat.
        if (settled) return;
        fs.stat(targetPath, (err, stats) => {
          if (err) {
            settle({ ok: false, status: 500, error: "Upload failed" });
            return;
          }
          settle({
            ok: true,
            result: { id, filename: info.filename, filepath: targetPath, size: stats.size },
          });
        });
      });

      writeStream.on("error", () => {
        destroyAndCleanup();
        settle({ ok: false, status: 500, error: "Upload failed" });
      });

      stream.pipe(writeStream);
    });

    bb.on("error", (err) => {
      destroyAndCleanup();
      settle({ ok: false, status: 500, error: "Upload failed" });
      // eslint-disable-next-line no-console
      console.error("upload error:", err);
    });

    bb.on("finish", () => {
      if (settled) return; // resolved elsewhere (400/413), or write stream will settle it

      if (!sawFile) {
        settle({ ok: false, status: 400, error: "No file provided" });
      }
      // If a valid file was seen, wait for writeStream's 'finish' above —
      // don't settle here, it may not have flushed yet.
    });

    req.on("aborted", () => {
      destroyAndCleanup();
    });

    req.pipe(bb);
  });
}
