/* design-audit probe
 *
 * Paste the whole file into javascript_tool. Returns one JSON blob covering
 * typography, spacing, contrast, tap targets, overflow, heading order, alt text,
 * focus states, design-token drift and perceived performance.
 *
 * It deliberately SUMMARISES (counts, distinct values, worst-N offenders) rather
 * than dumping every node - a full dump would blow past the tool result limit and
 * bury the findings that matter.
 *
 * ALWAYS check `viewport` in the result first. If it is 0 the pane is not
 * compositing and every geometric number below is garbage - call resize_window
 * with an explicit width/height and run this again.
 */
(() => {
  const VW = window.innerWidth;
  const out = { viewport: VW, url: location.href };
  if (!VW) {
    out.FATAL = 'viewport is 0 - pane not compositing. Call resize_window with explicit width/height, then re-run.';
    return out;
  }

  const vis = (el) => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const loc = (el) => {
    const id = el.id ? '#' + el.id : '';
    const cls = el.className && typeof el.className === 'string'
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 60);
  };
  const txt = (el) => (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 45);

  /* ---------- colour + contrast ---------- */
  const parse = (c) => {
    const m = (c || '').match(/rgba?\(([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,/\s]+([\d.]+))?/);
    return m ? { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] } : null;
  };
  const lum = ({ r, g, b }) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (fg, bg) => {
    const a = lum(fg), b = lum(bg);
    return +(((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05))).toFixed(2);
  };
  // Composite the real backdrop. Translucent layers MUST be blended, not treated
  // as opaque - a `rgba(brand, .06)` tint over white is nearly white, and reading
  // it as solid brand colour manufactures contrast failures that do not exist.
  const over = (top, under) => ({
    r: top.r * top.a + under.r * (1 - top.a),
    g: top.g * top.a + under.g * (1 - top.a),
    b: top.b * top.a + under.b * (1 - top.a)
  });
  const bgOf = (el) => {
    const layers = [];
    let n = el;
    while (n && n !== document.documentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0.001) { layers.push(c); if (c.a >= 0.999) break; }
      n = n.parentElement;
    }
    const rootBg = parse(getComputedStyle(document.documentElement).backgroundColor);
    let base = (rootBg && rootBg.a >= 0.999) ? rootBg : { r: 255, g: 255, b: 255 };
    for (let i = layers.length - 1; i >= 0; i--) base = over(layers[i], base);
    return base;
  };

  /* ---------- collect text-bearing elements once ---------- */
  const textEls = [];
  document.querySelectorAll('body *').forEach((el) => {
    if (/^(SCRIPT|STYLE|NOSCRIPT|SVG|PATH|BR|IFRAME|VIDEO|SOURCE)$/.test(el.tagName)) return;
    const direct = [...el.childNodes]
      .filter((n) => n.nodeType === 3 && n.textContent.trim().length > 1)
      .map((n) => n.textContent.trim()).join(' ');
    if (direct && vis(el)) textEls.push({ el, text: direct });
  });

  /* ---------- typography ---------- */
  const sizes = {}, families = {}, weights = {};
  const longLines = [];
  textEls.forEach(({ el, text }) => {
    const s = getComputedStyle(el);
    const px = Math.round(parseFloat(s.fontSize));
    sizes[px] = (sizes[px] || 0) + 1;
    const fam = s.fontFamily.split(',')[0].replace(/["']/g, '').trim();
    families[fam] = (families[fam] || 0) + 1;
    weights[s.fontWeight] = (weights[s.fontWeight] || 0) + 1;

    // line length in approximate characters (0.5em average glyph width)
    if (text.length > 60) {
      const w = el.getBoundingClientRect().width;
      const ch = Math.round(w / (parseFloat(s.fontSize) * 0.5));
      if (ch > 80 || ch < 30) longLines.push({ at: loc(el), chars: ch, text: text.slice(0, 40) });
    }
  });
  out.typography = {
    distinctSizes: Object.keys(sizes).map(Number).sort((a, b) => b - a),
    sizeCount: Object.keys(sizes).length,
    families: Object.entries(families).sort((a, b) => b[1] - a[1]).slice(0, 5),
    weights: Object.keys(weights).sort(),
    smallText: Object.keys(sizes).map(Number).filter((n) => n < 14).sort((a, b) => a - b),
    lineLengthOutliers: longLines.sort((a, b) => b.chars - a.chars).slice(0, 6)
  };

  /* ---------- contrast ---------- */
  const fails = [];
  const seen = new Set();
  textEls.forEach(({ el, text }) => {
    const s = getComputedStyle(el);
    let fg = parse(s.color); if (!fg || fg.a < 0.1) return;
    const bg = bgOf(el);
    if (fg.a < 0.999) fg = over(fg, bg);   // semi-transparent text blends too
    const px = parseFloat(s.fontSize);
    const bold = +s.fontWeight >= 700;
    const large = px >= 24 || (px >= 18.66 && bold);
    const need = large ? 3 : 4.5;
    const r = ratio(fg, bg);
    if (r < need) {
      const key = s.color + '|' + Math.round(bg.r) + ',' + Math.round(bg.g) + ',' + Math.round(bg.b) + '|' + Math.round(px);
      if (seen.has(key)) return;
      seen.add(key);
      fails.push({
        at: loc(el), sample: text.slice(0, 35),
        fg: s.color, bg: `rgb(${Math.round(bg.r)}, ${Math.round(bg.g)}, ${Math.round(bg.b)})`,
        fontPx: Math.round(px), ratio: r, needs: need,
        severity: r < need * 0.7 ? 'severe' : 'marginal'
      });
    }
  });
  out.contrast = {
    textNodesChecked: textEls.length,
    failures: fails.sort((a, b) => a.ratio - b.ratio).slice(0, 12),
    failureCount: fails.length
  };

  /* ---------- tap targets (mobile matters most) ---------- */
  const small = [];
  document.querySelectorAll('a, button, input, select, textarea, [role="button"], [onclick]').forEach((el) => {
    if (!vis(el)) return;
    const r = el.getBoundingClientRect();
    if (r.width < 44 || r.height < 44) {
      small.push({
        at: loc(el), label: txt(el) || el.getAttribute('aria-label') || '(no text)',
        size: Math.round(r.width) + 'x' + Math.round(r.height)
      });
    }
  });
  out.tapTargets = { belowMin: small.slice(0, 12), belowMinCount: small.length, minimum: '44x44' };

  /* ---------- overflow ---------- */
  const over = [];
  document.querySelectorAll('body *').forEach((el) => {
    if (!vis(el)) return;
    const r = el.getBoundingClientRect();
    if (r.right > VW + 2 && r.width <= VW) return;       // merely positioned off-screen (carousels)
    if (r.width > VW + 2) over.push({ at: loc(el), width: Math.round(r.width) });
  });
  out.overflow = {
    documentScrollWidth: document.documentElement.scrollWidth,
    pageScrollsHorizontally: document.documentElement.scrollWidth > VW,
    tooWide: over.slice(0, 8)
  };

  /* ---------- heading order ---------- */
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis);
  const skips = [];
  let prev = 0;
  hs.forEach((h) => {
    const lv = +h.tagName[1];
    if (prev && lv > prev + 1) skips.push({ from: 'h' + prev, to: 'h' + lv, text: txt(h) });
    prev = lv;
  });
  out.headings = {
    h1Count: document.querySelectorAll('h1').length,
    order: hs.slice(0, 20).map((h) => h.tagName + ': ' + txt(h)),
    levelSkips: skips
  };

  /* ---------- images / alt ---------- */
  const imgs = [...document.querySelectorAll('img')];
  out.images = {
    total: imgs.length,
    missingAlt: imgs.filter((i) => !i.hasAttribute('alt')).map(loc).slice(0, 10),
    emptyAlt: imgs.filter((i) => i.getAttribute('alt') === '').length,
    noDimensions: imgs.filter((i) => !i.getAttribute('width') || !i.getAttribute('height')).map(loc).slice(0, 10),
    oversized: imgs.filter((i) => {
      const r = i.getBoundingClientRect();
      return i.naturalWidth && r.width && i.naturalWidth > r.width * 2.5;
    }).map((i) => ({ at: loc(i), natural: i.naturalWidth, rendered: Math.round(i.getBoundingClientRect().width) })).slice(0, 8)
  };

  /* ---------- focus states ---------- */
  // A keyboard user needs to see where they are. Detect interactive elements with
  // no author-defined focus style by diffing the stylesheet rules.
  let focusRules = 0;
  try {
    [...document.styleSheets].forEach((ss) => {
      let rules; try { rules = ss.cssRules; } catch (e) { return; }
      [...(rules || [])].forEach((r) => {
        if (r.selectorText && /:focus(-visible)?/.test(r.selectorText)) focusRules++;
      });
    });
  } catch (e) { /* cross-origin sheets */ }
  document.querySelectorAll('style').forEach((s) => {
    focusRules += (s.textContent.match(/:focus(-visible)?/g) || []).length;
  });
  out.focus = {
    focusRuleCount: focusRules,
    interactiveCount: document.querySelectorAll('a,button,input,select,textarea').length,
    note: focusRules === 0 ? 'NO focus styles found anywhere - keyboard users cannot see where they are' : 'focus styles present'
  };

  /* ---------- design-token drift ---------- */
  // New sections often hardcode colours instead of using the theme tokens. Compare
  // declared custom properties against raw hex/rgb literals in inline style blocks.
  const rootStyles = getComputedStyle(document.documentElement);
  const tokens = [];
  try {
    [...document.styleSheets].forEach((ss) => {
      let rules; try { rules = ss.cssRules; } catch (e) { return; }
      [...(rules || [])].forEach((r) => {
        if (r.style) for (const p of r.style) if (p.startsWith('--')) tokens.push(p);
      });
    });
  } catch (e) { /* ignore */ }
  const inlineCss = [...document.querySelectorAll('style')].map((s) => s.textContent).join('\n');
  const hexes = inlineCss.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
  const hexCount = {};
  hexes.forEach((x) => { const k = x.toLowerCase(); hexCount[k] = (hexCount[k] || 0) + 1; });
  out.tokens = {
    declaredTokens: [...new Set(tokens)].slice(0, 30),
    declaredCount: [...new Set(tokens)].length,
    hardcodedHexInStyleBlocks: Object.entries(hexCount).sort((a, b) => b[1] - a[1]).slice(0, 15),
    hardcodedHexTotal: hexes.length,
    inlineStyleAttrs: document.querySelectorAll('[style]').length,
    note: 'High hardcoded-hex or inline-style counts in newer sections = design-system drift.'
  };

  /* ---------- spacing rhythm ---------- */
  const gaps = {};
  document.querySelectorAll('section, .container, [class*="__"]').forEach((el) => {
    if (!vis(el)) return;
    const s = getComputedStyle(el);
    ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom'].forEach((p) => {
      const v = Math.round(parseFloat(s[p]) || 0);
      if (v > 0) gaps[v] = (gaps[v] || 0) + 1;
    });
  });
  out.spacing = {
    distinctValues: Object.keys(gaps).map(Number).sort((a, b) => a - b),
    distinctCount: Object.keys(gaps).length,
    mostUsed: Object.entries(gaps).sort((a, b) => b[1] - a[1]).slice(0, 8),
    note: 'Many distinct values (>12) suggests ad-hoc spacing rather than a scale.'
  };

  /* ---------- perceived performance ---------- */
  const res = performance.getEntriesByType('resource');
  const byType = {};
  res.forEach((r) => {
    const t = r.name.split('?')[0].split('.').pop().slice(0, 5).toLowerCase();
    byType[t] = (byType[t] || 0) + (r.transferSize || 0);
  });
  const nav = performance.getEntriesByType('navigation')[0];
  out.performance = {
    resourceCount: res.length,
    totalTransferKB: Math.round(res.reduce((s, r) => s + (r.transferSize || 0), 0) / 1024),
    byTypeKB: Object.entries(byType).map(([k, v]) => [k, Math.round(v / 1024)]).sort((a, b) => b[1] - a[1]).slice(0, 8),
    heaviest: res.filter((r) => r.transferSize > 120000)
      .map((r) => ({ f: r.name.split('/').pop().split('?')[0].slice(0, 45), kb: Math.round(r.transferSize / 1024) }))
      .sort((a, b) => b.kb - a.kb).slice(0, 8),
    domContentLoadedMs: nav ? Math.round(nav.domContentLoadedEventEnd) : null,
    loadMs: nav ? Math.round(nav.loadEventEnd) : null
  };

  /* ---------- above the fold ---------- */
  const fold = [];
  document.querySelectorAll('body *').forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.top < window.innerHeight && r.bottom > 0 && vis(el)) {
      if (/^(A|BUTTON)$/.test(el.tagName)) fold.push(txt(el) || '(no text)');
    }
  });
  out.aboveFold = {
    ctaCount: fold.length,
    ctas: [...new Set(fold)].slice(0, 12),
    note: 'More than ~2 competing CTAs above the fold dilutes each one.'
  };

  return out;
})()
