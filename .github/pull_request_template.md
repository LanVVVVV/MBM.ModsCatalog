## Mod / Мод

- **Mod ID (DLL name without extension) / ID мода (имя DLL без расширения):**
- **Name / Название:**
- **Mod repository / Репозиторий мода:**
- **Raw URL `manifest.json`:**

## Author checklist / Чеклист автора

- [ ] `manifest.json` opens in the browser via raw URL / открывается по прямой ссылке (raw)
- [ ] `package` points to a working `.zip` or `.rar` / ведёт на рабочий архив
- [ ] `updated` is in `dd.MM.yyyy` format (e.g. `15.06.2026`) / указан в формате `dd.MM.yyyy`
- [ ] `id` matches the mod `.dll` file name / совпадает с именем `.dll`
- [ ] Only **one** new URL added to `manifests[]` in `catalog.json` / добавлена только одна ссылка
- [ ] Categories and tags use English IDs from [CONTRIBUTING.md](../CONTRIBUTING.md) / категории и теги — ID на английском

## For reviewer / Для ревьюера

- [ ] JSON is valid; commas between `manifests` entries are correct / JSON валиден, запятые на месте
- [ ] Author manifest parses; mod installs from **Explore** / манифест парсится, установка работает
- [ ] Description and links look correct / описание и ссылки корректны
