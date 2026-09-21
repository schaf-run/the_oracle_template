import express from "express";
import { healthRouter } from "./routes/health";
import { modelsRouter } from "./routes/models";

export const app = express();

app.use("/api", healthRouter);
app.use("/api", modelsRouter);
