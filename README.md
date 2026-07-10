# MBM.ModsCatalog

**English** | [Русский](Documentation/README.ru.md)

Root mod catalog for [MBM.ModLoader](https://github.com/Tzigan/MBM.ModLoader).  
The in-game **Explore** tab loads this repository and fetches author `manifest.json` files from URLs in `catalog.json`.

**This repository does not host mod files** — only links to manifests in author repositories.

Install/download counts are stored in [`stats.json`](stats.json) on the **`stats`** branch (updated by GitHub Actions; `main` is PR-only).

## Quick start

1. Host `manifest.json` in your mod repository — see [manifest.example.json](Documentation/manifest.example.json).
2. **Fork** this repo → add your manifest raw URL to `catalog.json` → open a **Pull Request**.

Full guide: [Documentation/CONTRIBUTING.md](Documentation/CONTRIBUTING.md) | [RU](Documentation/CONTRIBUTING.ru.md)

## ModLoader URL

```
https://raw.githubusercontent.com/Tzigan/MBM.ModsCatalog/refs/heads/main/catalog.json
```

## Documentation

| Document | Description |
|----------|-------------|
| [Documentation/CONTRIBUTING.md](Documentation/CONTRIBUTING.md) | How to add a mod (EN) |
| [Documentation/CONTRIBUTING.ru.md](Documentation/CONTRIBUTING.ru.md) | Как добавить мод (RU) |
| [Documentation/manifest.example.json](Documentation/manifest.example.json) | Example author manifest |
| [Documentation/README.ru.md](Documentation/README.ru.md) | Описание репозитория (RU) |
