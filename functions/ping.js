// Temporary probe: if /ping answers, Pages Functions run on this project.
export const onRequest = () =>
  new Response("functions-are-running", {
    headers: { "content-type": "text/plain; charset=utf-8" },
  });
