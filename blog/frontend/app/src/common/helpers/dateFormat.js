export function formatDate(dateStr, mode = "auto", locale = "ru") {
  if (!dateStr) return "";

  const date = new Date(dateStr);

  if (isNaN(date)) return dateStr;

  // Автоматический режим: если только год, если есть месяц, если есть день
  if (mode === "auto") {
    if (date.getDate() === 1 && date.getMonth() === 0) {
      // Если это 1 января (часто для хранения только года)
      return date.getFullYear();
    } else if (date.getDate() === 1) {
      // Если только месяц и год
      return date.toLocaleDateString(locale, { month: "long", year: "numeric" });
    } else {
      // Полная дата
      return date.toLocaleDateString(locale, {
        day: "numeric",
        month: "long",
        year: "numeric",
      });
    }
  }

  // Явно указанный режим
  switch (mode) {
    case "year":
      return date.getFullYear();
    case "month-year":
      return date.toLocaleDateString(locale, { month: "long", year: "numeric" });
    case "full":
      return date.toLocaleDateString(locale, {
        day: "numeric",
        month: "long",
        year: "numeric",
      });
    default:
      return dateStr;
  }
}