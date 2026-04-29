(function() {
  'use strict';
  const cfg = window.docPageConfig || {};
  const locale = cfg.locale || 'zh';
  const dt = cfg.documentType || '';
  const route = cfg.route || '';
  const template = cfg.templatePath || '';
  const whenToUse = cfg.whenToUse || '';
  const isSlides = dt === 'slides';
  const pageName = cfg.pageName || dt.replace(/_/g, ' ');

  const zhNames = {
    one_pager: '单页摘要', long_doc: '长文', letter: '信件',
    portfolio: '作品集', resume: '简历', slides: '幻灯片',
    equity_report: '个股研报', changelog: '更新日志',
    process_flow: '流程图', timeline: '时间线', faq_page: '常见问题',
    case_study: '案例拆解', research_summary: '研究摘要',
    stats_report: '数据报告', infographic: '信息图'
  };
  const enNames = {
    one_pager: 'One Pager', long_doc: 'Long Doc', letter: 'Letter',
    portfolio: 'Portfolio', resume: 'Resume', slides: 'Slides',
    equity_report: 'Equity Report', changelog: 'Changelog',
    process_flow: 'Process Flow', timeline: 'Timeline', faq_page: 'FAQ',
    case_study: 'Case Study', research_summary: 'Research Summary',
    stats_report: 'Stats Report', infographic: 'Infographic'
  };
  const displayName = locale === 'zh' ? (zhNames[dt] || pageName) : (enNames[dt] || pageName);

  // Inject nav + meta styles
  const style = document.createElement('style');
  style.textContent = `
    .site-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-4);
      margin-bottom: var(--space-5);
      padding: var(--space-3) var(--space-4);
      border: 1px solid rgba(216, 210, 196, 0.9);
      border-radius: var(--radius-lg);
      background: rgba(250, 248, 244, 0.94);
      box-shadow: var(--shadow-soft);
    }
    .site-nav a {
      color: var(--brand);
      font-size: 13px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .site-nav a:hover { text-decoration: underline; }
    .site-nav .nav-group { display: flex; align-items: center; gap: var(--space-4); }
    .site-nav .nav-sep { color: var(--line); }
    .meta-bar {
      margin-top: var(--space-5);
      padding: var(--space-5) var(--space-6);
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: var(--space-5);
    }
    .meta-item .meta-title { margin-bottom: 8px; }
    .meta-item code {
      font-family: var(--data);
      font-size: 13px;
      color: var(--brand);
      background: rgba(220, 231, 242, 0.5);
      padding: 2px 6px;
      border-radius: 4px;
    }
    .meta-item p {
      margin: 8px 0 0;
      color: var(--ink-subtle);
      font-size: 14px;
      line-height: 1.6;
    }
    .locale-switch {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(250, 248, 244, 0.8);
      font-size: 13px;
    }
  `;
  document.head.appendChild(style);

  const shell = document.querySelector('.page-shell');
  if (!shell) return;

  // Build nav
  const nav = document.createElement('nav');
  nav.className = 'site-nav reveal';
  const otherLocale = locale === 'zh' ? 'en' : 'zh';
  const otherPath = '../' + otherLocale + '/' + location.pathname.split('/').pop();
  const homePath = '../index.html';
  const diagramsPath = '../diagrams.html';

  const homeLabel = locale === 'zh' ? '首页' : 'Home';
  const diagramsLabel = locale === 'zh' ? '图示库' : 'Diagrams';
  const switchLabel = locale === 'zh' ? 'English' : '中文';

  let linksHtml = '';
  if (isSlides && template) {
    const pyPath = locale === 'zh' ? '../../templates/slides.py' : '../../templates/slides-en.py';
    const pyLabel = locale === 'zh' ? 'Python 模板' : 'Python Template';
    linksHtml = `<a href="${pyPath}">${pyLabel}</a><span class="nav-sep">|</span>`;
  }

  nav.innerHTML = `
    <div class="nav-group">
      <a href="${homePath}">${homeLabel}</a>
      <span class="nav-sep">/</span>
      <a href="${diagramsPath}">${diagramsLabel}</a>
    </div>
    <div class="nav-group">
      ${linksHtml}
      <a class="locale-switch" href="${otherPath}">${switchLabel}</a>
    </div>
  `;
  shell.insertBefore(nav, shell.firstChild);

  // Build meta bar after hero
  const hero = shell.querySelector('.frame.hero, .hero');
  if (hero && (dt || route || template)) {
    const meta = document.createElement('section');
    meta.className = 'frame meta-bar reveal';
    const whenLabel = locale === 'zh' ? '适用场景' : 'Best For';
    const routeLabel = locale === 'zh' ? '内部路由' : 'Internal Route';
    const typeLabel = locale === 'zh' ? '文档类型' : 'Document Type';
    const tmplLabel = locale === 'zh' ? '模板路径' : 'Template Path';
    meta.innerHTML = `
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-title">${typeLabel}</div>
          <code>${dt}</code>
        </div>
        <div class="meta-item">
          <div class="meta-title">${routeLabel}</div>
          <code>${route}</code>
        </div>
        <div class="meta-item">
          <div class="meta-title">${tmplLabel}</div>
          <code>${template}</code>
        </div>
        <div class="meta-item">
          <div class="meta-title">${whenLabel}</div>
          <p>${whenToUse}</p>
        </div>
      </div>
    `;
    hero.parentNode.insertBefore(meta, hero.nextSibling);
  }

  // Build footer
  const footer = document.createElement('footer');
  footer.innerHTML = locale === 'zh'
    ? `<span>Momo Paper / 文档与可视叙事的路由设计系统</span><span>${displayName} · ${route}</span>`
    : `<span>Momo Paper / A routed design system for documents and visual narratives.</span><span>${displayName} · ${route}</span>`;
  shell.appendChild(footer);
})();
