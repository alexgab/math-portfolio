const works = {
  "graduate-work": {
    category: "Ключевая работа",
    title: "Выпускная работа",
    summary: "Специфика применения инструментов искусственного интеллекта в учебном процессе по предмету «Математика».",
    textFile: "texts/graduate-work.txt",
    downloadFile: "graduate-work.docx"
  },
  "appendix-ai-tools": {
    category: "Приложение",
    title: "Сравнительная таблица ИИ-инструментов",
    summary: "Приложение с обзором возможностей, ограничений и примеров эффективных промтов для учителя математики.",
    textFile: "texts/appendix-ai-tools.txt",
    downloadFile: "appendix-ai-tools.docx"
  },
  "specialized-platforms": {
    category: "Методика",
    title: "Использование специализированных платформ",
    summary: "Материал о применении образовательных платформ для мотивации, индивидуализации и обратной связи.",
    textFile: "texts/specialized-platforms.txt",
    downloadFile: "specialized-platforms.docx"
  },
  "modern-tools-post": {
    category: "Цифровая трансформация",
    title: "Современные инструменты педагога",
    summary: "Рекламный пост о начале работы математического кружка с использованием современных цифровых инструментов.",
    textFile: "texts/modern-tools-post.txt",
    downloadFile: "modern-tools-post.docx"
  },
  "internet-safety": {
    category: "Безопасность",
    title: "Безопасность в сети Интернет",
    summary: "Памятка с правилами цифровой безопасности и примерами безопасного поведения в сети.",
    textFile: "texts/internet-safety.txt",
    downloadFile: "internet-safety.docx"
  },
  "online-tools": {
    category: "Онлайн-обучение",
    title: "Инструменты для занятий в онлайн-формате",
    summary: "Краткий обзор сервисов для дистанционного обучения и цифровой коммуникации с учащимися.",
    textFile: "texts/online-tools.txt",
    downloadFile: "online-tools.docx"
  },
  "online-format": {
    category: "Опыт преподавания",
    title: "Особенности реализации образовательного процесса в онлайн-формате",
    summary: "Личный опыт применения онлайн-формата в преподавании математики, его преимущества и ограничения.",
    textFile: "texts/online-format.txt",
    downloadFile: "online-format.docx"
  },
  "lesson-dihedral-angle": {
    category: "Разработка урока",
    title: "Тема «Двугранный угол»",
    summary: "Конспект урока по геометрии с интерактивными сервисами, визуализацией и практическими заданиями.",
    textFile: "texts/lesson-dihedral-angle.txt",
    downloadFile: "lesson-dihedral-angle.docx",
    image: "dihedral-angle.png",
    imageAlt: "Иллюстрация к теме двугранного угла"
  }
};

const params = new URLSearchParams(window.location.search);
const workId = params.get("work");
const work = works[workId];

const titleElement = document.getElementById("work-title");
const categoryElement = document.getElementById("work-category");
const summaryElement = document.getElementById("work-summary");
const textElement = document.getElementById("document-text");
const downloadLink = document.getElementById("download-link");
const previewCard = document.getElementById("preview-card");
const previewImage = document.getElementById("preview-image");

if (!work) {
  document.title = "Материал не найден";
  titleElement.textContent = "Материал не найден";
  summaryElement.textContent = "Выбранная работа отсутствует. Вернитесь на главную страницу и выберите материал снова.";
  textElement.textContent = "Не удалось открыть материал.";
  downloadLink.removeAttribute("href");
  downloadLink.setAttribute("aria-disabled", "true");
  downloadLink.textContent = "Файл недоступен";
} else {
  document.title = `${work.title} | Портфолио`;
  categoryElement.textContent = work.category;
  titleElement.textContent = work.title;
  summaryElement.textContent = work.summary;
  downloadLink.href = work.downloadFile;

  if (work.image) {
    previewCard.hidden = false;
    previewImage.src = work.image;
    previewImage.alt = work.imageAlt || "";
  }

  fetch(work.textFile)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Не удалось загрузить текст материала.");
      }
      return response.text();
    })
    .then((text) => {
      textElement.textContent = text.trim();
    })
    .catch(() => {
      textElement.textContent = "Текст материала пока недоступен. Вы можете скачать исходный файл DOCX.";
    });
}
