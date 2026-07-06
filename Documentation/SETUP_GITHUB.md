# Настройка GitHub для MBM.ModsCatalog

Один раз настройте репозиторий [github.com/Tzigan/MBM.ModsCatalog](https://github.com/Tzigan/MBM.ModsCatalog).

## 1. Структура репозитория

```
catalog.json
README.md
CONTRIBUTING.md
.github/
Documentation/
  manifest.example.json
  ...
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
| Lock branch (опционально) | по желанию |
| Allow force pushes | ❌ |
| Allow deletions | ❌ |

## 3. CODEOWNERS

В `.github/CODEOWNERS` указан `@Tzigan`. Замените на ваш GitHub-логин, если отличается.

## 4. Actions

**Settings → Actions → General** — разрешите workflows.

При PR с изменением `catalog.json` запустится **Validate catalog**.

## 5. Проверка

1. Fork с другого аккаунта → PR с новой строкой в `catalog.json`.
2. CI зелёный, merge только после вашего **Approve**.

## Workflow владельца

1. PR → зелёный CI.
2. Проверить raw URL манифеста и мод.
3. **Approve** → **Merge**.
