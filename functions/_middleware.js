// Serve the 404 page on unmatched paths.
//
// A 404.html at the output root is meant to be enough, but this project answers
// misses with an empty body and no content-type, so nothing routes to it. This
// runs after the static-asset lookup and swaps in the page when that came back
// 404.
//
// Ask for /404 before /404.html: the platform strips .html and answers the
// latter with a 307, whose body is empty, which would put us right back where
// we started. Only a 200 is accepted, and any failure falls through to the
// original response - a broken error page is worse than a blank one.
export const onRequest = async (context) => {
  const response = await context.next();
  if (response.status !== 404) return response;
  try {
    const origin = new URL(context.request.url).origin;
    for (const path of ["/404", "/404.html"]) {
      const page = await context.env.ASSETS.fetch(new URL(path, origin));
      if (page && page.status === 200) {
        return new Response(page.body, {
          status: 404,
          headers: { "content-type": "text/html; charset=utf-8" },
        });
      }
    }
  } catch (e) {
    /* fall through */
  }
  return response;
};
