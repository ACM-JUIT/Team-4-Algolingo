import { escapeHtml } from "./utils.js";

function renderInline(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

function renderCodeFence(block) {
  const lines = block.split("\n");
  const language = lines[0].replace(/```/, "").trim();
  const code = escapeHtml(lines.slice(1, -1).join("\n"));
  return `
    <pre class="code-block"><code class="language-${escapeHtml(language || 'text')}">${code}</code></pre>
  `;
}

function renderList(lines, ordered = false) {
  const tag = ordered ? "ol" : "ul";
  const items = lines
    .map((line) => line.replace(ordered ? /^\d+\.\s+/ : /^[-*]\s+/, ""))
    .map((line) => `<li>${renderInline(line)}</li>`)
    .join("");
  return `<${tag}>${items}</${tag}>`;
}

export function renderMarkdown(markdown = "") {
  if (!markdown) return "";

  const sections = markdown.split(/(```[\s\S]*?```)/g).filter(Boolean);
  return sections
    .map((section) => {
      if (section.startsWith("```")) {
        return renderCodeFence(section);
      }

      const lines = section.split("\n");
      const chunks = [];
      let paragraph = [];
      let listBuffer = [];
      let orderedBuffer = [];

      const flushParagraph = () => {
        if (!paragraph.length) return;
        chunks.push(`<p>${renderInline(paragraph.join(" "))}</p>`);
        paragraph = [];
      };

      const flushList = () => {
        if (listBuffer.length) {
          chunks.push(renderList(listBuffer, false));
          listBuffer = [];
        }
        if (orderedBuffer.length) {
          chunks.push(renderList(orderedBuffer, true));
          orderedBuffer = [];
        }
      };

      lines.forEach((rawLine) => {
        const line = rawLine.trimEnd();
        if (!line.trim()) {
          flushParagraph();
          flushList();
          return;
        }

        if (/^#{1,4}\s+/.test(line)) {
          flushParagraph();
          flushList();
          const level = line.match(/^#+/)[0].length;
          chunks.push(`<h${level}>${renderInline(line.replace(/^#{1,4}\s+/, ""))}</h${level}>`);
          return;
        }

        if (/^[-*]\s+/.test(line)) {
          flushParagraph();
          orderedBuffer.length = 0;
          listBuffer.push(line);
          return;
        }

        if (/^\d+\.\s+/.test(line)) {
          flushParagraph();
          listBuffer.length = 0;
          orderedBuffer.push(line);
          return;
        }

        if (/^>\s+/.test(line)) {
          flushParagraph();
          flushList();
          chunks.push(`<blockquote>${renderInline(line.replace(/^>\s+/, ""))}</blockquote>`);
          return;
        }

        paragraph.push(line.trim());
      });

      flushParagraph();
      flushList();
      return chunks.join("");
    })
    .join("");
}
