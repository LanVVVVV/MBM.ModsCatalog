# Настройка GitHub для MBM.ModsCatalog

Один раз настройте репозиторий [github.com/Tzigan/MBM.ModsCatalog](https://github.com/Tzigan/MBM.ModsCatalog).

## 1. Загрузите файлы из этой папки

Скопируйте содержимое `MBM.ModsCatalog/` в корень репозитория на GitHub (через git push или веб-интерфейс):

```
.github/CODEOWNERS
.github/pull_request_template.md
.github/workflows/validate-catalog.yml
.github/scripts/validate_catalog.py
README.md
CONTRIBUTING.md
catalog.json
manifest.example.json
```

## 2. Защита ветки main

**Settings → Branches → Add branch protection rule**

| Параметр | Значение |
|----------|----------|
| Branch name pattern | `main` |
| Require a pull request before merging | ✅ |
| Required approvals | **1** |
| Require review from Code Owners | ✅ |
| Dismiss stale pull request approvals when new commits are pushed | ✅ |
| Restrict who can push to matching branches | ✅ — только вы |
| Allow force pushes | ❌ |
| Allow deletions | ❌ |

## 3. CODEOWNERS

В `.github/CODEOWNERS` указан `@Tzigan`. Замените на ваш GitHub-логин, если отличается.

После первого push GitHub начнёт запрашивать ваш approve на каждый PR.

## 4. Actions

**Settings → Actions → General** — разрешите workflows (по умолчанию для public repo).

При PR с изменением `catalog.json` запустится **Validate catalog**.

## 5. Проверка

1. Создайте тестовый fork от другого аккаунта (или второго браузера).
2. Добавьте строку в `catalog.json` → PR.
3. Убедитесь: CI зелёный, без вашего **Approve** кнопка Merge недоступна (при включённом Code Owners).

## Ваш workflow

1. Открыть PR → дождаться зелёного CI.
2. Открыть raw URL манифеста, проверить мод.
3. **Files changed** — одна новая строка в `catalog.json`.
4. **Approve** → **Merge pull request**.
