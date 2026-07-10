# How to add a mod to the catalog

**English** | [Русский](CONTRIBUTING.ru.md)

The **MBM.ModsCatalog** repository contains links only. Description, version, archive, and changelog live in **your** repository's `manifest.json`.

## 1. Prepare your mod repository

Create `manifest.json` in your repository. See [manifest.example.json](manifest.example.json).

### Required mod fields

| Field | Description |
|-------|-------------|
| `id` | DLL file name without extension (e.g. `MyMod`) |
| `name` | Display name |
| `version` | Mod version |
| `package` | Direct HTTPS link to a `.zip` or `.rar` archive |

### Recommended fields

| Field | Description |
|-------|-------------|
| `description` | Text shown in the Explore tab |
| `updated` | Update date: **`dd.MM.yyyy`** (e.g. `15.06.2026`) |
| `modPortal` | Mod page URL |
| `changelog` | Raw URL to `CHANGELOG.md` |
| `icon` | PNG URL (up to 512×512) |
| `categories` | Category IDs in English (see below) |
| `tags` | Tag IDs in English (see below) |

### Categories (`categories`)

`Gameplay`, `Content`, `QoL`, `UI`, `Balance`, `Library`

### Tags (`tags`)

`Breeding`, `Economy`, `Characters`, `Patches`, `Localization`, `Compatibility`, `Cheats`

### Mod archive

- **`.zip`** and **`.rar`** are supported.
- If the archive contains a `Mods/` folder, files are installed directly into the game's `Mods` folder.
- The `package` field must be a **direct** download link.

### Install statistics

Download counts are maintained centrally in [`stats.json`](../stats.json) in this repository.

- **Do not** add `downloads` to your author `manifest.json` — MBM.ModLoader reports installs automatically and reads counts from `stats.json`.
- Install counters are updated on the **`stats`** branch (GitHub Actions cannot push to protected `main`).
- Optional root `catalog.json` fields:
  - `statsUrl` — override URL for `stats.json` (default: `stats` branch in this repo)
  - `statsReportUrl` — HTTPS endpoint for install reports (see [`tools/stats-relay`](../tools/stats-relay))

### Raw manifest URL

The link must return JSON in the browser (not an HTML page).

Examples:

- **GitHub:** `https://raw.githubusercontent.com/User/Repo/refs/heads/main/manifest.json`
- **GitVerse:** `https://gitverse.ru/api/repos/User/Repo/raw/branch/Branch/manifest.json`

## 2. Add a link to the catalog

1. **Fork** [MBM.ModsCatalog](https://github.com/Tzigan/MBM.ModsCatalog).
2. In your fork, open `catalog.json`.
3. Add **one line** to the `manifests` array — the raw URL of your `manifest.json`.

```json
{
  "version": 1,
  "manifests": [
    "https://gitverse.ru/api/repos/Author/ExistingMod/raw/branch/main/manifest.json",
    "https://raw.githubusercontent.com/YourName/YourMod/refs/heads/main/manifest.json"
  ]
}
```

**Important:** URLs must be separated by a **comma**. No trailing comma after the last entry.

4. Commit and open a **Pull Request** to `main`.

## 3. Pull Request

Fill in the PR template: mod ID, links, checklist.

Automated checks (CI):

- valid JSON in `catalog.json`;
- all URLs use `https://`;
- manifests are reachable and contain at least one mod with `id` and `package`.

## 4. Review and merge

The catalog owner reviews the PR and **merges** after approval.  
External authors cannot push directly to `main`.

## Common mistakes

| Issue | Fix |
|-------|-----|
| `unexpected character` in JSON | Missing comma between URLs in `manifests` |
| Mod not visible in Explore | Invalid raw URL or manifest without `package` |
| Date sort does not work | `updated` is not in `dd.MM.yyyy` format |
| Filters do not match | `categories` / `tags` must use English IDs from the list above |

## Questions

Open an [Issue](https://github.com/Tzigan/MBM.ModsCatalog/issues) in this repository.
