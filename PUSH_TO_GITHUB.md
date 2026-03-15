# GitHub-ға жүктеу

## 1-қадам: GitHub-та жаңа репозиторий құру

1. https://github.com/new сілтемесіне өтіңіз
2. **Repository name:** `ai-university` (немесе өз атыңызды)
3. **Description:** `Университет қызметі бойынша AI агент`
4. **Public** таңдаңыз
5. **"Create repository"** батырмасын басыңыз
6. Жаңа бетте **HTTPS** сілтемесін көшіріңіз (мысалы: `https://github.com/YOUR_USERNAME/ai-university.git`)

## 2-қадам: Терминалда командаларды орындаңыз

```powershell
cd "c:\Диплом 2026\Университеттің қызметі бойынша AI агент әзірлеу"

git remote add origin https://github.com/YOUR_USERNAME/ai-university.git
git branch -M main
git push -u origin main
```

**YOUR_USERNAME** орнына өз GitHub пайдаланушы атыңызды жазыңыз.

## Ескерту

- `.env` файлы жүктелмейді (API кілті қауіпсіздік үшін)
- Бірінші рет push кезінде GitHub логин/пароль сұрауы мүмкін
