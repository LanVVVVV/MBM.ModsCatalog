# Install stats relay

MBM.ModLoader reports Explore installs with an anonymous `POST` request. The game client cannot hold a GitHub token, so a small relay triggers `repository_dispatch` on **MBM.ModsCatalog**.

## Flow

1. Loader `POST`s `{ "modId": "MyMod", "version": "1.0.0" }` to `statsReportUrl` from `catalog.json`.
2. This worker calls GitHub `repository_dispatch` (`mod_install`).
3. Workflow [`.github/workflows/update-stats.yml`](../../.github/workflows/update-stats.yml) bumps `stats.json`.
4. Loader reads `stats.json` on the next catalog refresh.

## Deploy (Cloudflare Workers)

1. Create a Worker from `worker.js`.
2. Set secrets:
   - `GITHUB_OWNER` — catalog owner (e.g. `Tzigan`)
   - `GITHUB_REPO` — `MBM.ModsCatalog`
   - `GITHUB_TOKEN` — fine-grained PAT with **Contents: Read and write** and **Actions: Read and write** on this repo
3. Route: `POST https://<your-worker>/install`
4. Add to root `catalog.json`:

```json
{
  "version": 1,
  "statsReportUrl": "https://<your-worker>/install",
  "manifests": [ "..." ]
}
```

Optional `statsUrl` overrides the default raw URL of `stats.json` in this repository.

Until `statsReportUrl` is set, install counts stay at `0` and only manual edits to `stats.json` change them.
