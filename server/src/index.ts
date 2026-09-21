import { app } from "./app";
import { env } from "./env";

app.listen(env.port, () => {
  console.log(`server listening on http://localhost:${env.port}`);
});
