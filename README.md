# 🎤 Transcribe
[![Python Version](https://img.shields.io/badge/python-3.11-brightgreen.svg)](https://python.org)

## Описание проекта

**Karaoke Transcription App** — это веб-приложение на Python (Flask) для загрузки аудиофайлов (MP3), автоматической расшифровки текста с точной синхронизацией по времени и воспроизведения текста в стиле караоке.

Пользователь загружает аудиофайл `.mp3`, приложение:
- Конвертирует его в формат `.wav` с правильными параметрами (PCM, Mono, 16 бит, 16000 Hz);
- Выполняет точное распознавание речи с таймкодами для каждого слова с помощью локальной модели **Vosk** (офлайн);
- Генерирует страницу с аудиоплеером и текстом песни, где слова подсвечиваются в реальном времени в момент их произнесения.

---

## Стек технологий

- **Backend:**
  - Python 3.11+
  - Flask
  - Vosk API (офлайн-распознавание речи)
  - Pydub (конвертация аудио)
  - SpeechRecognition (альтернативная поддержка)

- **Frontend:**
  - HTML5
  - Bootstrap 5
  - JavaScript (управление плеером и подсветкой текста)

---

## Основные функции

- 🎵 Загрузка MP3-файлов через удобную форму.
- 🔄 Автоматическая конвертация в WAV (PCM, Mono).
- 🧠 Распознавание речи с точными таймкодами.
- 🎤 Отображение текста и подсветка слов в момент их звучания.
- 🚀 Работа в режиме офлайн, без внешних API и интернет-зависимости.
- 🖥 Совместимость с любыми современными браузерами.

---

## Установка проекта

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/yourname/transcribe.git
   cd transcribe
    ```bash

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # для Linux/Mac
    venv\Scripts\activate     # для Windows
    pip install -r requirements.txt
    ```bash

    ```bash
        wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
        unzip vosk-model-small-en-us-0.15.zip
    ```bash
    ```bash
        /uploads/        # для загружаемых mp3
        /results/        # для обработки (если нужно)
        /static/css/     # стили
        /static/js/      # скрипты
        /templates/      # HTML-шаблоны
        /vosk-model/     # распакованная модель речи
    ```bash

## Использование

Перейдите в браузере по адресу: http://localhost:5000

Загрузите ваш MP3-файл.

Дождитесь обработки (отображается прогрессбар и статус).

После завершения проигрывайте аудио с подсветкой текста в режиме караоке!


## Возможности для улучшения
Автоматическая прокрутка текста.

Плавные анимации подсветки слов и фраз.

Поддержка мультиязычности (русский, украинский, английский).

Расширение поддержки аудиоформатов (OGG, WAV, FLAC).

Фоновые очереди обработки (через Celery + Redis).

Деплой через Docker и Docker Compose.