# Preset: ProductHunt Hunter Outreach Pipeline

**Preset ID:** `ph_hunter_outreach_pipeline`  
**Version:** 1.0 | **Date:** April 2026  
**GitHub:** https://github.com/progprogect/producthunt-scraper

---

## Что делает пресет

Автоматически собирает и квалифицирует **хантеров с ProductHunt** для аутрич-кампаний.

**На входе:** Тема/ниша (например: 'AI automation', 'SaaS tools') + ключ GetXAPI  
**На выходе:** Excel-файл с ранжированными хантерами — имя, LinkedIn, Twitter, подписчики, скор

---

## Сценарий работы

```
Пользователь вводит тему ('AI automation')
         down
[1] Скрапинг ProductHunt Topics
    => /topics/artificial-intelligence
    => 55 сек ожидания React-рендеринга
    => Параллельно (3-6 браузеров) посещает страницы продуктов
    => Собирает username-ы хантеров
    Результат: 50-170 уникальных username-ов

[2] Обогащение профилей
    => Параллельно (6 браузеров) открывает каждый профиль
    => JS-парсинг: followers, hunted, LinkedIn, Twitter, website
    => Кэширует (можно прервать и продолжить)
    Результат: ~58% с LinkedIn, ~44% с Twitter

[3] X/Twitter followers (опционально)
    => REST API через getxapi.com
    => Без браузера, ~0.5 сек/профиль

[4] Скоринг 0-100
    Topic Fit 29% + PH Followers 28% + Hunts 17% + X Followers 11% + Activity 15%

[5] Excel-экспорт
    => Все профили в файле (никто не удаляется)
    => Зелёный = Priority (>=50), Жёлтый = Secondary (>=25), Серый = ниже порога
    => Файл: PH-Hunters -- {Topic} -- Topics -- {Date} -- {N} people.xlsx
```

---

## Эксперты пресета

| Эксперт | Назначение | Тип |
|---------|-----------|-----|
| `ph_fast_pipeline_v2` | **Главный оркестратор** — полный прогон | Основной |
| `ph_enrich_and_export_incremental` | Пошаговый режим, каждые 20 профилей | Большие объёмы |
| `ph_scrape_parallel_fast` | Параллельный скрапинг (21x быстрее) | Шаг 1 |
| `ph_enrich_parallel_fast` | Параллельное обогащение (14-27x быстрее) | Шаг 2 |
| `ph_patch_x_followers` | X/Twitter followers без браузера | Шаг 3 |
| `ph_filter_hunters` | Фильтрация по gates | Утилита |
| `ph_score_hunters` | Скоринг 0-100 | Утилита |
| `ph_export_to_excel` | Экспорт в Excel | Утилита |
| `ph_make_filename` | Генератор имени файла | Утилита |
| `cleanup_chrome_temp` | Очистка Chrome temp (важно!) | Обслуживание |
| `ph_benchmark_sources` | Сравнение источников | Опциональный |
| `ph_forums_add_and_compare` | Добавить Forums к бенчмарку | Опциональный |

---

## Требования

### GetXAPI ключ (для X/Twitter followers)
1. Зайти на getxapi.com
2. Зарегистрироваться (есть бесплатный план)
3. Скопировать API key (вида `get-x-api-xxxxx...`)

**Зачем:** X/Twitter followers = 11% скора. Без него пайплайн работает, скор чуть ниже.

### Chrome браузер
- Обязательно `headless=False` (Cloudflare блокирует headless)

### Extella API token
- Нужен для `ph_fast_pipeline_v2`

---

## Быстрый старт

```python
# Полный прогон (~20 мин)
ph_fast_pipeline_v2(
    days_back=3,
    max_products_per_day=8,
    headless=False,  # ОБЯЗАТЕЛЬНО
    topic_slug='artificial-intelligence',
    fit_categories='AI,developer tools,SaaS,productivity',
    api_token='ваш-extella-token',
    getxapi_key_value='get-x-api-xxxxx'
)

# Добавить X followers позже
ph_patch_x_followers(getxapi_key_value='get-x-api-xxxxx')
```

---

## Бенчмарк источников

| Источник | Профилей | Avg Score | LinkedIn % | Рекомендация |
|----------|---------|-----------|------------|-------------|
| **Topics** /topics/{slug} | 50 | 22.5 | **58%** | Рекомендуется |
| Search /search?q={query} | 40 | 21.2 | 55% | Для точных запросов |
| Forums /forums/search | 19 | 21.6 | 26% | Только как дополнение |

---

## Именование файлов

```
PH-Hunters -- {Topic} -- {Source} -- {YYYY-MM-DD} -- {N} people.xlsx
```

---

## Troubleshooting

| Проблема | Решение |
|---------|--------|
| No space left on device | Запустить `cleanup_chrome_temp` |
| Failed to connect to browser | Снизить `max_concurrent` до 4-5 |
| X followers = 0 | Пополнить баланс getxapi (HTTP 402) |
| Cloudflare блокирует | Убедиться что `headless=False` |

---

## Активирующий промпт

```
Запусти пресет ProductHunt Hunter Outreach Pipeline.
Тема: [УКАЖИ НИШУ, например 'AI automation']
Минимум подписчиков: [1000]
GetXAPI ключ: [ключ или 'нет']
```
