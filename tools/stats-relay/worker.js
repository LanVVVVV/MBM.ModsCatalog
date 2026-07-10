/**
 * Cloudflare Worker relay for anonymous install reports.
 *
 * POST /install  { "modId": "MyMod", "version": "1.0.0" }
 *   -> repository_dispatch(mod_install) on MBM.ModsCatalog
 *
 * GET /stats
 *   -> fresh stats.json from GitHub API (no raw CDN cache)
 *
 * Secrets (wrangler):
 *   GITHUB_TOKEN  — fine-grained PAT with Contents + Actions on MBM.ModsCatalog
 *   GITHUB_OWNER  — e.g. Tzigan
 *   GITHUB_REPO   — e.g. MBM.ModsCatalog
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "GET") {
      if (url.pathname !== "/stats" && url.pathname !== "/stats.json") {
        return new Response("not found", { status: 404 });
      }

      const owner = env.GITHUB_OWNER;
      const repo = env.GITHUB_REPO;
      const token = env.GITHUB_TOKEN;
      const statsRef = env.GITHUB_STATS_REF || "stats";
      const statsPath = env.GITHUB_STATS_PATH || "stats.json";
      if (!owner || !repo || !token) {
        return new Response("relay not configured", { status: 503 });
      }

      const response = await fetch(
        `https://api.github.com/repos/${owner}/${repo}/contents/${statsPath}?ref=${statsRef}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            Accept: "application/vnd.github.raw+json",
            "User-Agent": "MBM-Stats-Relay",
            "X-GitHub-Api-Version": "2022-11-28",
          },
        }
      );

      if (!response.ok) {
        const text = await response.text();
        return new Response(text || "stats fetch failed", { status: 502 });
      }

      const body = await response.text();
      return new Response(body, {
        status: 200,
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "no-store, no-cache, must-revalidate",
          Pragma: "no-cache",
        },
      });
    }

    if (request.method !== "POST") {
      return new Response("method not allowed", { status: 405 });
    }

    if (url.pathname !== "/install" && url.pathname !== "/") {
      return new Response("not found", { status: 404 });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response("invalid json", { status: 400 });
    }

    const modId = typeof body.modId === "string" ? body.modId.trim() : "";
    if (!modId || modId.length > 128 || !/^[A-Za-z0-9._-]+$/.test(modId)) {
      return new Response("invalid modId", { status: 400 });
    }

    const version = typeof body.version === "string" ? body.version.trim().slice(0, 64) : "";

    const owner = env.GITHUB_OWNER;
    const repo = env.GITHUB_REPO;
    const token = env.GITHUB_TOKEN;
    if (!owner || !repo || !token) {
      return new Response("relay not configured", { status: 503 });
    }

    const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/dispatches`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/vnd.github+json",
        "User-Agent": "MBM-Stats-Relay",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      body: JSON.stringify({
        event_type: "mod_install",
        client_payload: { modId, version },
      }),
    });

    if (!response.ok) {
      const text = await response.text();
      return new Response(text || "dispatch failed", { status: 502 });
    }

    return new Response(null, { status: 204 });
  },
};
