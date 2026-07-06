# MBM.ModsCatalog

[English](README.md) | **Русский**

Корневой каталог модов для [MBM.ModLoader](https://github.com/Tzigan/MBM.ModLoader).  
Игра во вкладке **Explore** загружает этот репозиторий и по ссылкам из `catalog.json` подтягивает `manifest.json` авторов.

**Этот репозиторий не хранит файлы модов** — только список URL на манифесты в репозиториях авторов.

## Файлы

| Файл | Назначение |
|------|------------|
| `catalog.json` | Список raw-URL на `manifest.json` авторов |
| `manifest.example.json` | Пример манифеста в репозитории мода |
| [CONTRIBUTING.ru.md](CONTRIBUTING.ru.md) | Как добавить мод через Pull Request |

## Добавить мод

1. Разместите `manifest.json` в **своём** репозитории (см. `manifest.example.json`).
2. Сделайте **Fork** этого репозитория.
3. Добавьте raw-URL в `catalog.json` → `manifests[]`.
4. Откройте **Pull Request** в `main`.
5. Дождитесь проверки и одобрения владельца каталога.

Подробности — [CONTRIBUTING.ru.md](CONTRIBUTING.ru.md).

## URL для ModLoader

```
https://raw.githubusercontent.com/Tzigan/MBM.ModsCatalog/refs/heads/main/catalog.json
```
