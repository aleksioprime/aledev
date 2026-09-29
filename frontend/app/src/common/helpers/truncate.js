// Обрезает текст до указанной длины, добавляя многоточие
export function truncate(text, max = 140) {
  if (!text) return "";
  return text.length > max ? `${text.slice(0, max).trimEnd()}…` : text;
}
