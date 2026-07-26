import { escapeHtml } from './utils.js';

const PYTHON_KEYWORDS = new Set(['and','as','assert','break','class','continue','def','del','elif','else','except','False','finally','for','from','global','if','import','in','is','lambda','None','nonlocal','not','or','pass','raise','return','True','try','while','with','yield','print','input','range','int','float','str','bool','list','dict','set','tuple']);

function renderInline(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
}

function highlightPython(code) {
  const escaped = escapeHtml(code);
  return escaped
    .replace(/(#.*)$/gm, '<span class="token token-comment">$1</span>')
    .replace(/("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g, '<span class="token token-string">$1</span>')
    .replace(/\b(\d+(?:\.\d+)?)\b/g, '<span class="token token-number">$1</span>')
    .replace(/\b([A-Za-z_][A-Za-z0-9_]*)\b/g, (match) => PYTHON_KEYWORDS.has(match) ? `<span class="token token-keyword">${match}</span>` : match);
}

function renderCodeFence(block) {
  const lines = block.split('\n');
  const language = lines[0].replace(/```/, '').trim() || 'text';
  const rawCode = lines.slice(1, -1).join('\n');
  const highlighted = language === 'python' ? highlightPython(rawCode) : escapeHtml(rawCode);
  return `
    <figure class="lesson-code" data-code-language="${escapeHtml(language)}">
      <div class="lesson-code-toolbar">
        <span class="lesson-code-language">${escapeHtml(language)}</span>
        <button class="lesson-code-copy" type="button" data-copy-code>Copy</button>
      </div>
      <pre class="code-block"><code class="language-${escapeHtml(language)}">${highlighted}</code></pre>
    </figure>
  `;
}

function renderList(lines, ordered = false) {
  const tag = ordered ? 'ol' : 'ul';
  const items = lines
    .map((line) => line.replace(ordered ? /^\d+\.\s+/ : /^[-*]\s+/, ''))
    .map((line) => `<li>${renderInline(line)}</li>`)
    .join('');
  return `<${tag}>${items}</${tag}>`;
}

export function renderMarkdown(markdown = '') {
  if (!markdown) return '';
  const sections = markdown.split(/(```[\s\S]*?```)/g).filter(Boolean);
  return sections.map((section) => {
    if (section.startsWith('```')) return renderCodeFence(section);
    const lines = section.split('\n');
    const chunks = [];
    let paragraph = [];
    let listBuffer = [];
    let orderedBuffer = [];

    const flushParagraph = () => {
      if (!paragraph.length) return;
      chunks.push(`<p>${renderInline(paragraph.join(' '))}</p>`);
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
        chunks.push(`<h${level}>${renderInline(line.replace(/^#{1,4}\s+/, ''))}</h${level}>`);
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
        chunks.push(`<blockquote>${renderInline(line.replace(/^>\s+/, ''))}</blockquote>`);
        return;
      }
      paragraph.push(line.trim());
    });

    flushParagraph();
    flushList();
    return chunks.join('');
  }).join('');
}

export function enhanceRenderedMarkdown(scope = document) {
  scope.querySelectorAll('[data-copy-code]').forEach((button) => {
    if (button.dataset.bound === 'true') return;
    button.dataset.bound = 'true';
    button.addEventListener('click', async () => {
      const code = button.closest('.lesson-code')?.querySelector('code')?.textContent || '';
      try {
        await navigator.clipboard.writeText(code);
        const previous = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => { button.textContent = previous; }, 1400);
      } catch {
        button.textContent = 'Unavailable';
        setTimeout(() => { button.textContent = 'Copy'; }, 1400);
      }
    });
  });
}
