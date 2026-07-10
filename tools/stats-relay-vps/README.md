# Install stats relay (VPS)

For regions where **Cloudflare Workers** is unavailable, run this tiny relay on any VPS with HTTPS in front (nginx + Let's Encrypt). Works on Russian hosts (Timeweb, Selectel, REG.RU, Yandex Cloud VM, etc.).

Same contract as [../stats-relay/worker.js](../stats-relay/worker.js):

```
POST /install
Content-Type: application/json

{"modId": "MyMod", "version": "1.0.0"}
```

Response: **204** on success.

## 1. Copy files to the server

```bash
sudo mkdir -p /opt/mbm-stats-relay
sudo cp relay.py /opt/mbm-stats-relay/
```

## 2. Secrets (not in git)

```bash
sudo tee /etc/mbm-stats-relay.env <<'EOF'
GITHUB_OWNER=Tzigan
GITHUB_REPO=MBM.ModsCatalog
GITHUB_TOKEN=github_pat_...
PORT=8787
EOF
sudo chmod 600 /etc/mbm-stats-relay.env
```

**Important:** one variable per line, ASCII only. No comments on the same line as the token (`#` is not a comment in systemd env files).

## 3. systemd

```bash
sudo cp mbm-stats-relay.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mbm-stats-relay
```

## 4. nginx (HTTPS)

```nginx
server {
    listen 443 ssl;
    server_name stats.example.com;

    location /install {
        proxy_pass http://127.0.0.1:8787/install;
        proxy_set_header Host $host;
    }
}
```

Issue a certificate (e.g. `certbot --nginx`). Players and ModLoader must use **HTTPS**.

## 5. catalog.json

```json
{
  "version": 1,
  "statsReportUrl": "https://stats.example.com/install",
  "manifests": [ "..." ]
}
```

## Test

```bash
curl -i -X POST "https://stats.example.com/install" \
  -H "Content-Type: application/json" \
  -d '{"modId":"MoreGraphicAttachments","version":"1.0.0"}'
```

Then check **GitHub Actions → Update install stats** and `stats.json`.

## No server at all

Use **Actions → Update install stats → Run workflow** (manual `modId`) — see [update-stats.yml](../../.github/workflows/update-stats.yml). Game clients will not auto-report until `statsReportUrl` points to a reachable relay.
