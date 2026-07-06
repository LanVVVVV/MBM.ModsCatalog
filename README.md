# MBM.ModsCatalog

**English** | [Русский](README.ru.md)

Root mod catalog for [MBM.ModLoader](https://github.com/Tzigan/MBM.ModLoader).  
The in-game **Explore** tab loads this repository and fetches each author's `manifest.json` from URLs listed in `catalog.json`.

**This repository does not host mod files** — only URLs to manifests in author repositories.

## Files

| File | Purpose |
|------|---------|
| `catalog.json` | List of raw URLs to author `manifest.json` files |
| `manifest.example.json` | Example manifest for your mod repository |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add a mod via Pull Request |

## Add a mod

1. Host `manifest.json` in **your** repository (see `manifest.example.json`).
2. **Fork** this repository.
3. Add your raw URL to `catalog.json` → `manifests[]`.
4. Open a **Pull Request** to `main`.
5. Wait for review and approval by the catalog owner.

Details — [CONTRIBUTING.md](CONTRIBUTING.md).

## ModLoader URL

```
https://raw.githubusercontent.com/Tzigan/MBM.ModsCatalog/refs/heads/main/catalog.json
```
