import { debounce } from "./utils.js";

export function attachCodeEditor({ textarea, gutter, onChange }) {
  if (!textarea) return;

  const syncGutter = () => {
    if (!gutter) return;
    const lineCount = Math.max(1, textarea.value.split("\n").length);
    gutter.innerHTML = Array.from({ length: lineCount }, (_, index) => `<div>${index + 1}</div>`).join("");
    gutter.scrollTop = textarea.scrollTop;
  };

  textarea.addEventListener("scroll", () => {
    if (gutter) gutter.scrollTop = textarea.scrollTop;
  });

  textarea.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      event.preventDefault();
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const value = textarea.value;
      textarea.value = `${value.slice(0, start)}    ${value.slice(end)}`;
      textarea.selectionStart = textarea.selectionEnd = start + 4;
      syncGutter();
      onChange?.(textarea.value);
    }
  });

  const handleChange = debounce(() => {
    syncGutter();
    onChange?.(textarea.value);
  }, 100);

  textarea.addEventListener("input", handleChange);
  syncGutter();
}
