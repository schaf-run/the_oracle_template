import { Router } from "express";
import fs from "node:fs";
import { prisma } from "../db";
import { handleUpload } from "../lib/upload";

export const modelsRouter = Router();

modelsRouter.post("/models", async (req, res) => {
  const outcome = await handleUpload(req);

  if (!outcome.ok) {
    res.status(outcome.status).json({ error: outcome.error });
    return;
  }

  const { id, filename, filepath, size } = outcome.result;
  await prisma.model.create({ data: { id, filename, filepath, size } });

  res.status(201).json({ id, filename, size, url: `/model/${id}` });
});

modelsRouter.get("/models/:id", async (req, res) => {
  const model = await prisma.model.findUnique({ where: { id: req.params.id } });
  if (!model) {
    res.status(404).json({ error: "Model not found" });
    return;
  }
  res.json({
    id: model.id,
    filename: model.filename,
    size: model.size,
    createdAt: model.createdAt,
  });
});

modelsRouter.get("/models/:id/file", async (req, res) => {
  const model = await prisma.model.findUnique({ where: { id: req.params.id } });
  if (!model) {
    res.status(404).json({ error: "Model not found" });
    return;
  }

  res.setHeader("Content-Type", "text/plain");
  res.setHeader("Content-Length", String(model.size));

  const stream = fs.createReadStream(model.filepath);
  stream.on("error", (err: NodeJS.ErrnoException) => {
    if (err.code === "ENOENT") {
      res.status(404).json({ error: "Model not found" });
    } else if (!res.headersSent) {
      res.status(500).json({ error: "Failed to read file" });
    }
  });
  stream.pipe(res);
});
