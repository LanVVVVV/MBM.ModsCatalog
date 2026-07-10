# Как добавить мод в каталог

[English](CONTRIBUTING.md) | **Русский**

Каталог **MBM.ModsCatalog** содержит только ссылки. Описание, версия, архив и changelog хранятся в **вашем** репозитории в `manifest.json`.

## 1. Подготовьте репозиторий мода

Создайте `manifest.json` в своём репозитории. Образец — [manifest.example.json](manifest.example.json).

### Обязательные поля мода

| Поле | Описание |
|------|----------|
| `id` | Имя DLL без расширения (например `MyMod`) |
| `name` | Отображаемое название |
| `version` | Версия мода |
| `package` | Прямая HTTPS-ссылка на `.zip` или `.rar` |

### Рекомендуемые поля

| Поле | Описание |
|------|----------|
| `description` | Текст во вкладке Explore |
| `updated` | Дата обновления: **`dd.MM.yyyy`** (например `15.06.2026`) |
| `modPortal` | Страница мода |
| `changelog` | Raw URL на `CHANGELOG.md` |
| `icon` | URL на PNG (до 512×512) |
| `categories` | Категории (ID на английском, см. ниже) |
| `tags` | Теги (ID на английском, см. ниже) |

### Категории (`categories`)

`Gameplay`, `Content`, `QoL`, `UI`, `Balance`, `Library`

### Теги (`tags`)

`Breeding`, `Economy`, `Characters`, `Patches`, `Localization`, `Compatibility`, `Cheats`

### Архив мода

- Поддерживаются **`.zip`** и **`.rar`**.
- Если в архиве есть папка `Mods/` с файлами — они будут установлены прямо в `Mods` игры.
- Поле `package` должно вести на **прямую** ссылку на скачивание файла.

### Статистика установок

Счётчик загрузок ведётся централизованно в [`stats.json`](../stats.json) этого репозитория.

- **Не добавляйте** поле `downloads` в авторский `manifest.json` — MBM.ModLoader сам отправляет события установки и читает счётчики из `stats.json`.
- Счётчики обновляются в ветке **`stats`** (Actions не может пушить в защищённый `main`).
- Необязательные поля корневого `catalog.json`:
  - `statsUrl` — URL файла `stats.json` (по умолчанию — ветка `stats` этого репозитория)
  - `statsReportUrl` — HTTPS-эндпоинт для отчётов об установке (см. [`tools/stats-relay`](../tools/stats-relay))

### Raw URL манифеста

Ссылка должна открывать JSON в браузере без HTML-страницы.

Примеры:

- **GitHub:** `https://raw.githubusercontent.com/User/Repo/refs/heads/main/manifest.json`
- **GitVerse:** `https://gitverse.ru/api/repos/User/Repo/raw/branch/Branch/manifest.json`

## 2. Добавьте ссылку в каталог

1. Нажмите **Fork** репозитория [MBM.ModsCatalog](https://github.com/Tzigan/MBM.ModsCatalog).
2. В своём форке откройте `catalog.json`.
3. Добавьте **одну строку** в массив `manifests` — raw URL вашего `manifest.json`.

```json
{
  "version": 1,
  "manifests": [
    "https://gitverse.ru/api/repos/Author/ExistingMod/raw/branch/main/manifest.json",
    "https://raw.githubusercontent.com/YourName/YourMod/refs/heads/main/manifest.json"
  ]
}
```

**Важно:** между URL нужна **запятая**. После последнего элемента запятой нет.

4. Закоммитьте и откройте **Pull Request** в ветку `main`.

## 3. Pull Request

При создании PR заполните шаблон: ID мода, ссылки, чеклист.

Автоматическая проверка (CI):

- валидный JSON в `catalog.json`;
- все URL — `https://`;
- манифесты открываются и содержат хотя бы один мод с `id` и `package`.

## 4. Ревью и слияние

Владелец каталога проверяет PR и **сам выполняет Merge** после одобрения.  
Прямой push в `main` для сторонних авторов недоступен.

## Частые ошибки

| Ошибка | Решение |
|--------|---------|
| `unexpected character` в JSON | Пропущена запятая между URL в `manifests` |
| Мод не виден в Explore | Неверный raw URL или манифест без `package` |
| Сортировка по дате не работает | Поле `updated` не в формате `dd.MM.yyyy` |
| Фильтры не срабатывают | `categories` / `tags` — только ID из списка выше (англ.) |

## Вопросы

Откройте [Issue](https://github.com/Tzigan/MBM.ModsCatalog/issues) в этом репозитории.
