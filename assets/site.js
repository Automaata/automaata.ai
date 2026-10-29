/* Automaata — shared behaviour: navigation, theme switch, tabs, forms, filters. */
(function () {
  var root = document.documentElement;

  /* ---------- Theme switch (same logic as dellonsharma.com) ---------- */
  var toggle = document.getElementById('theme-toggle');
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t === 'dark') return true;
    if (t === 'light') return false;
    return !!(mq && mq.matches);
  }
  function renderTheme() { if (toggle) toggle.setAttribute('aria-checked', isDark() ? 'true' : 'false'); }
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      renderTheme();
    });
    if (mq && mq.addEventListener) mq.addEventListener('change', renderTheme);
    renderTheme();
  }

  /* ---------- Header: mobile toggle + mega menus ---------- */
  var nav = document.querySelector('.nav');
  var navToggle = document.getElementById('navtoggle');
  var menuButtons = Array.prototype.slice.call(document.querySelectorAll('.navlinks > li > button[aria-controls]'));
  var isDesktop = function () { return window.matchMedia('(min-width: 981px)').matches; };

  function closeAll(except) {
    menuButtons.forEach(function (b) {
      if (b === except) return;
      b.setAttribute('aria-expanded', 'false');
      var m = document.getElementById(b.getAttribute('aria-controls'));
      if (m) m.classList.remove('open');
    });
  }
  function openMenu(b) {
    closeAll(b);
    b.setAttribute('aria-expanded', 'true');
    var m = document.getElementById(b.getAttribute('aria-controls'));
    if (m) m.classList.add('open');
  }
  menuButtons.forEach(function (b) {
    var m = document.getElementById(b.getAttribute('aria-controls'));
    b.addEventListener('click', function () {
      /* Desktop: hover already opened it, so a click keeps it open (outside click / Esc closes). Mobile: toggle. */
      if (isDesktop()) { openMenu(b); return; }
      if (b.getAttribute('aria-expanded') === 'true') { closeAll(); } else { openMenu(b); }
    });
    var timer;
    var li = b.parentElement;
    li.addEventListener('mouseenter', function () { if (isDesktop()) { clearTimeout(timer); openMenu(b); } });
    li.addEventListener('mouseleave', function () { if (isDesktop()) { timer = setTimeout(closeAll, 160); } });
    if (m) {
      m.addEventListener('mouseenter', function () { clearTimeout(timer); });
      m.addEventListener('mouseleave', function () { if (isDesktop()) { timer = setTimeout(closeAll, 160); } });
    }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(); if (nav) nav.classList.remove('open'); if (navToggle) navToggle.setAttribute('aria-expanded', 'false'); } });
  document.addEventListener('click', function (e) {
    if (!nav || nav.contains(e.target)) return;
    closeAll();
  });
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      navToggle.textContent = open ? 'CLOSE' : 'MENU';
      if (!open) closeAll();
    });
  }
  /* Audience tabs inside the Platform mega menu */
  document.querySelectorAll('.mega .aud').forEach(function (group) {
    var btns = group.querySelectorAll('button');
    btns.forEach(function (bt) {
      bt.addEventListener('click', function () {
        btns.forEach(function (x) { x.setAttribute('aria-selected', x === bt ? 'true' : 'false'); });
        var mega = group.closest('.mega');
        mega.querySelectorAll('.mpane').forEach(function (p) { p.hidden = p.getAttribute('data-pane') !== bt.getAttribute('data-pane'); });
      });
    });
  });

  /* ---------- Generic tabs: .tabs button[data-tab] -> .tabpane[data-tab] ---------- */
  document.querySelectorAll('[data-tabs]').forEach(function (block) {
    var btns = block.querySelectorAll('.tabs button');
    var panes = block.querySelectorAll('.tabpane');
    btns.forEach(function (bt) {
      bt.addEventListener('click', function () {
        btns.forEach(function (x) { x.setAttribute('aria-selected', x === bt ? 'true' : 'false'); });
        panes.forEach(function (p) { p.hidden = p.getAttribute('data-tab') !== bt.getAttribute('data-tab'); });
      });
    });
  });

  /* ---------- Expandable reveal buttons: [data-reveal="id"] ---------- */
  document.querySelectorAll('[data-reveal]').forEach(function (bt) {
    bt.addEventListener('click', function () {
      var t = document.getElementById(bt.getAttribute('data-reveal'));
      if (!t) return;
      t.hidden = !t.hidden;
      bt.setAttribute('aria-expanded', t.hidden ? 'false' : 'true');
    });
  });

  /* ---------- Forms (static site: validate, then explain) ---------- */
  document.querySelectorAll('form[data-static]').forEach(function (form) {
    var msg = form.querySelector('.msg');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var missing = [];
      form.querySelectorAll('[required]').forEach(function (f) {
        if (!String(f.value || '').trim()) missing.push((f.getAttribute('data-label') || f.name || 'field').toLowerCase());
        if (f.type === 'email' && f.value && f.value.indexOf('@') < 0) missing.push('a valid email');
      });
      if (!msg) return;
      if (missing.length) { msg.textContent = 'Please add your ' + missing.join(', ') + ' before sending.'; msg.hidden = false; return; }
      var body = [];
      form.querySelectorAll('input,select,textarea').forEach(function (f) {
        if (f.type === 'checkbox') { if (f.checked) body.push((f.getAttribute('data-label') || f.name) + ': yes'); return; }
        if (f.type === 'submit' || !f.name) return;
        if (String(f.value).trim()) body.push((f.getAttribute('data-label') || f.name) + ': ' + f.value);
      });
      var subject = encodeURIComponent(form.getAttribute('data-subject') || 'Automaata request');
      var href = 'mailto:hello@automaata.ai?subject=' + subject + '&body=' + encodeURIComponent(body.join('\n'));
      msg.innerHTML = 'This site does not have a form backend yet. <a href="' + href + '">Open this request in your email app</a> or write to hello@automaata.ai with the details above.';
      msg.hidden = false;
    });
  });

  /* ---------- Copy buttons: [data-copy="id"] ---------- */
  document.querySelectorAll('[data-copy]').forEach(function (bt) {
    bt.addEventListener('click', function () {
      var el = document.getElementById(bt.getAttribute('data-copy'));
      if (!el) return;
      var text = el.textContent;
      var orig = bt.textContent;
      function done() { bt.textContent = 'Copied'; setTimeout(function () { bt.textContent = orig; }, 1600); }
      function fallback() { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
    });
  });

  /* ---------- Resource filters ---------- */
  var resList = document.querySelector('[data-resources]');
  if (resList) {
    var typeBtns = document.querySelectorAll('[data-res-type]');
    var topicChecks = document.querySelectorAll('[data-res-topic]');
    var audChecks = document.querySelectorAll('[data-res-aud]');
    var items = resList.querySelectorAll('.res-item');
    var count = document.querySelector('[data-res-count]');
    var empty = document.querySelector('[data-res-empty]');
    var reset = document.querySelector('[data-res-reset]');
    var activeType = 'all';
    function apply() {
      var topics = Array.prototype.filter.call(topicChecks, function (c) { return c.checked; }).map(function (c) { return c.getAttribute('data-res-topic'); });
      var auds = Array.prototype.filter.call(audChecks, function (c) { return c.checked; }).map(function (c) { return c.getAttribute('data-res-aud'); });
      var shown = 0;
      items.forEach(function (it) {
        var ok = activeType === 'all' || it.getAttribute('data-type') === activeType;
        if (ok && topics.length) { var t = (it.getAttribute('data-topics') || '').split(' '); ok = topics.some(function (x) { return t.indexOf(x) >= 0; }); }
        if (ok && auds.length) { var a = (it.getAttribute('data-aud') || '').split(' '); ok = auds.some(function (x) { return a.indexOf(x) >= 0; }); }
        it.hidden = !ok; if (ok) shown++;
      });
      if (count) count.textContent = shown ? ('1–' + shown + ' of ' + shown + ' results') : '0 results';
      if (empty) empty.style.display = shown ? 'none' : 'block';
    }
    typeBtns.forEach(function (b) { b.addEventListener('click', function () { activeType = b.getAttribute('data-res-type'); typeBtns.forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); }); apply(); }); });
    topicChecks.forEach(function (c) { c.addEventListener('change', apply); });
    audChecks.forEach(function (c) { c.addEventListener('change', apply); });
    if (reset) reset.addEventListener('click', function () { activeType = 'all'; typeBtns.forEach(function (x) { x.setAttribute('aria-selected', x.getAttribute('data-res-type') === 'all' ? 'true' : 'false'); }); topicChecks.forEach(function (c) { c.checked = false; }); audChecks.forEach(function (c) { c.checked = false; }); apply(); });
    var sel = document.querySelector('[data-res-select]');
    if (sel) sel.addEventListener('change', function () { activeType = sel.value; typeBtns.forEach(function (x) { x.setAttribute('aria-selected', x.getAttribute('data-res-type') === activeType ? 'true' : 'false'); }); apply(); });
    apply();
  }

  /* ---------- Module picker feeds the pricing form ---------- */
  var modChecks = document.querySelectorAll('.module input[type="checkbox"]');
  var modOut = document.getElementById('f-modules');
  if (modChecks.length && modOut) {
    var sync = function () {
      var names = Array.prototype.filter.call(modChecks, function (c) { return c.checked; }).map(function (c) { return c.getAttribute('data-name'); });
      modOut.value = names.join(', ');
    };
    modChecks.forEach(function (c) { c.addEventListener('change', sync); });
    sync();
  }

  /* ---------- Year ---------- */
  document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = String(new Date().getFullYear()); });
})();
