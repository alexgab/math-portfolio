from __future__ import annotations

from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
TEXTS_DIR = ROOT / "texts"
WORKS_DIR = ROOT / "works"


WORKS = [
    {
        "slug": "graduate-work",
        "category": "Ключевая работа",
        "title": "Выпускная работа",
        "summary": "Специфика применения инструментов искусственного интеллекта в учебном процессе по предмету «Математика».",
        "download": "graduate-work.docx",
        "text": "graduate-work.txt",
    },
    {
        "slug": "appendix-ai-tools",
        "category": "Приложение",
        "title": "Сравнительная таблица ИИ-инструментов",
        "summary": "Приложение с обзором возможностей, ограничений и примеров эффективных промтов для учителя математики.",
        "download": "appendix-ai-tools.docx",
        "text": "appendix-ai-tools.txt",
    },
    {
        "slug": "specialized-platforms",
        "category": "Методика",
        "title": "Использование специализированных платформ",
        "summary": "Материал о применении образовательных платформ для мотивации, индивидуализации и обратной связи.",
        "download": "specialized-platforms.docx",
        "text": "specialized-platforms.txt",
    },
    {
        "slug": "modern-tools-post",
        "category": "Цифровая трансформация",
        "title": "Современные инструменты педагога",
        "summary": "Рекламный пост о начале работы математического кружка с использованием современных цифровых инструментов.",
        "download": "modern-tools-post.docx",
        "text": "modern-tools-post.txt",
    },
    {
        "slug": "internet-safety",
        "category": "Безопасность",
        "title": "Безопасность в сети Интернет",
        "summary": "Памятка с правилами цифровой безопасности и примерами безопасного поведения в сети.",
        "download": "internet-safety.docx",
        "text": "internet-safety.txt",
    },
    {
        "slug": "online-tools",
        "category": "Онлайн-обучение",
        "title": "Инструменты для занятий в онлайн-формате",
        "summary": "Краткий обзор сервисов для дистанционного обучения и цифровой коммуникации с учащимися.",
        "download": "online-tools.docx",
        "text": "online-tools.txt",
    },
    {
        "slug": "online-format",
        "category": "Опыт преподавания",
        "title": "Особенности реализации образовательного процесса в онлайн-формате",
        "summary": "Личный опыт применения онлайн-формата в преподавании математики, его преимущества и ограничения.",
        "download": "online-format.docx",
        "text": "online-format.txt",
    },
    {
        "slug": "lesson-dihedral-angle",
        "category": "Разработка урока",
        "title": "Тема «Двугранный угол»",
        "summary": "Конспект урока по геометрии с интерактивными сервисами, визуализацией и практическими заданиями.",
        "download": "lesson-dihedral-angle.docx",
        "text": "lesson-dihedral-angle.txt",
        "image": "dihedral-angle.png",
        "image_alt": "Иллюстрация к теме двугранного угла",
    },
]


UPPER_HEADING_RE = re.compile(r"^[A-ZА-ЯЁ0-9 .,:;()\"«»\-–—]+$")


def normalize_line(line: str) -> str:
    line = line.replace("\f", "").replace("\t", " ").strip()
    line = re.sub(r"\s+", " ", line)
    return line


def is_heading(line: str) -> bool:
    if not line:
        return False
    if line.startswith(("ГЛАВА ", "ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ", "СПИСОК ", "ОГЛАВЛЕНИЕ", "ПРИЛОЖЕНИЕ ")):
        return True
    if re.match(r"^\d+(\.\d+)+\.", line):
        return True
    if UPPER_HEADING_RE.fullmatch(line) and len(line) > 5:
        return True
    return False


def is_subheading(line: str) -> bool:
    if not line:
        return False
    if re.match(r"^\d+\.\s+[А-ЯA-ZЁ]", line) and len(line) < 110:
        return True
    if re.match(r"^\d+\)", line):
        return True
    if line.endswith(":") and len(line) < 120:
        return True
    if line.startswith(("Тип урока:", "Цель:", "Ход урока", "Домашнее задание:", "Вопросы:")):
        return True
    return False


def bullet_text(line: str) -> str | None:
    for prefix in ("•", "-", "–", "—", "*"):
        if line.startswith(prefix):
            return line[1:].strip()
    if re.match(r"^\d+\.\s+", line):
        return re.sub(r"^\d+\.\s+", "", line).strip()
    return None


def render_text(text: str) -> str:
    lines = [normalize_line(line) for line in text.splitlines()]
    blocks: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []

    def flush_paragraph() -> None:
      nonlocal paragraph
      if paragraph:
          blocks.append(f"<p>{escape(' '.join(paragraph))}</p>")
          paragraph = []

    def flush_bullets() -> None:
      nonlocal bullets
      if bullets:
          items = "".join(f"<li>{escape(item)}</li>" for item in bullets)
          blocks.append(f"<ul>{items}</ul>")
          bullets = []

    for line in lines:
        if not line:
            flush_paragraph()
            flush_bullets()
            continue

        if is_heading(line):
            flush_bullets()
            flush_paragraph()
            blocks.append(f"<h3>{escape(line)}</h3>")
            continue

        if is_subheading(line):
            flush_bullets()
            flush_paragraph()
            blocks.append(f"<h4>{escape(line)}</h4>")
            continue

        bullet = bullet_text(line)
        if bullet is not None:
            flush_paragraph()
            bullets.append(bullet)
            continue

        flush_bullets()

        paragraph.append(line)

    flush_paragraph()
    flush_bullets()
    return "\n        ".join(blocks)


def build_page(item: dict[str, str]) -> str:
    text = (TEXTS_DIR / item["text"]).read_text(encoding="utf-8").strip()
    content_html = render_text(text)

    image_block = ""
    if "image" in item:
        image_block = f"""
      <aside class="side-card">
        <h2>Иллюстрация</h2>
        <img src="../{item['image']}" alt="{escape(item['image_alt'])}">
      </aside>"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(item['title'])} | Портфолио</title>
  <meta name="description" content="{escape(item['summary'])}">
  <link rel="stylesheet" href="../viewer.css">
</head>
<body>
  <div class="viewer-shell">
    <header class="viewer-header">
      <a class="back-link" href="../index.html">Вернуться на главную</a>
      <div class="viewer-intro">
        <p class="viewer-kicker">{escape(item['category'])}</p>
        <h1>{escape(item['title'])}</h1>
        <p class="viewer-summary">{escape(item['summary'])}</p>
      </div>
      <div class="viewer-actions">
        <a class="button button-primary" href="../{item['download']}" download>Скачать DOCX</a>
        <a class="button button-secondary" href="../index.html#works">Ко всем работам</a>
      </div>
    </header>

    <main class="viewer-layout">
      <section class="content-card">
        <article class="document-content">
        {content_html}
        </article>
      </section>{image_block}
    </main>
  </div>
</body>
</html>
"""


def main() -> None:
    WORKS_DIR.mkdir(exist_ok=True)
    for item in WORKS:
        output = WORKS_DIR / f"{item['slug']}.html"
        output.write_text(build_page(item), encoding="utf-8")


if __name__ == "__main__":
    main()
