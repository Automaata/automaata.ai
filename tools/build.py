#!/usr/bin/env python3
"""Build automaata.ai: wraps page bodies in tools/pages/ with the shared head, nav and footer.

    python3 tools/build.py

Page fragments start with a front-matter comment:
    <!-- title: Platform | desc: One line. | nav: platform -->
Articles under tools/pages/resources/ add: type, date, topics, aud, summary.
"""
import re, pathlib, datetime, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / 'tools' / 'pages'
SITE = 'https://automaata.ai'
TODAY = datetime.date.today().isoformat()

# ------------------------------------------------------------------ helpers
def meta(fragment):
    m = re.match(r'\s*<!--(.*?)-->', fragment, re.S)
    d = {}
    if m:
        for part in m.group(1).split('|'):
            if ':' in part:
                k, v = part.split(':', 1)
                d[k.strip()] = v.strip()
        fragment = fragment[m.end():]
    return d, fragment.strip()

def base_for(depth):
    return '../' * depth if depth else ''

MARK = '<svg class="mark" viewBox="0 0 28 28" aria-hidden="true"><rect x="2" y="2" width="24" height="24" rx="6" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="18" cy="10" r="3.2" fill="#F2A900"/><path d="M8 20l5-10 2.6 5.2" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def head(title, desc, path, depth, extra_head=''):
    b = base_for(depth)
    canon = SITE + path
    full = 'Automaata' if title == 'Automaata' else f'{title} · Automaata'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="author" content="Automaata">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121C29" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Automaata">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Automaata — automaata.ai">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(full)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}/og.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{b}assets/site.css">
<script>
  (function () {{
    try {{
      var t = localStorage.getItem('theme');
      if (t === 'dark' || t === 'light') document.documentElement.setAttribute('data-theme', t);
    }} catch (e) {{}}
  }})();
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Automaata",
  "url": "{SITE}/",
  "logo": "{SITE}/apple-touch-icon.png",
  "email": "hello@automaata.ai",
  "foundingDate": "2026",
  "founder": {{ "@type": "Person", "name": "Dellon Sharma" }},
  "description": "AI-first security workforce management software for contract guard companies and in-house corporate security teams.",
  "address": {{ "@type": "PostalAddress", "addressLocality": "San Francisco", "addressRegion": "CA", "addressCountry": "US" }}
}}
</script>
{extra_head}
</head>
<body data-base="{b}">
<a class="skip" href="#main">Skip to content</a>
"""

def nav(active, depth):
    b = base_for(depth)
    def cur(n): return ' aria-current="page"' if n == active else ''
    def L(href, text, small=None):
        s = f'<small>{small}</small>' if small else ''
        return f'<a href="{b}{href}">{text}{s}</a>'
    return f"""
<div class="announce"><div class="wrap"><span class="tag">New</span><span>Jessica, Automaata's AI assistant, is live on every page, 24/7.</span><a href="#" data-jessica>Say hello →</a></div></div>
<header class="nav" id="top">
  <div class="wrap">
    <a class="brand" href="{b}index.html" aria-label="Automaata home">{MARK}automaata<small>.ai</small></a>
    <button class="navtoggle" id="navtoggle" aria-expanded="false" aria-controls="navlinks">MENU</button>
    <ul class="navlinks" id="navlinks">
      <li><button type="button" aria-expanded="false" aria-controls="mega-platform"{(' class="on"' if active=='platform' else '')}>Platform</button>
        <div class="mega" id="mega-platform"><div class="wrap">
          <div>
            <div class="aud" role="tablist"><button type="button" role="tab" aria-selected="true" data-pane="firms">Security &amp; guarding providers</button><button type="button" role="tab" aria-selected="false" data-pane="inhouse">In-house security teams</button></div>
            <div class="mpane" data-pane="firms"><div class="cols">
              <div><h4>Field operations</h4>{L('platform/#tours','Checkpoint tours')}{L('platform/#incidents','Incident reporting')}{L('platform/#dar','Daily activity reports')}{L('platform/#postorders','Post orders')}{L('platform/#dispatch','Live map &amp; dispatch')}{L('platform/#lone','Lone worker safety')}{L('platform/#app','Officer App')}</div>
              <div><h4>Run the business</h4>{L('platform/#scheduling','Scheduling')}{L('platform/#time','Time &amp; attendance')}{L('platform/#credentials','Credentials &amp; training')}{L('platform/#billing','Billing &amp; contracts')}{L('platform/#reconciliation','Reconciliation')}{L('platform/#portal','Client portal')}{L('platform/#console','Ops Console')}</div>
              <div><h4>Data and AI</h4>{L('platform/#levels','Automation levels')}{L('platform/#jessica','Jessica, AI assistant')}{L('platform/#api','API &amp; integrations')}{L('company/#trust','Trust &amp; security')}</div>
            </div></div>
            <div class="mpane" data-pane="inhouse" hidden><div class="cols">
              <div><h4>Protect</h4>{L('solutions/#inhouse','Multi-site operations')}{L('platform/#incidents','One incident taxonomy')}{L('platform/#dispatch','Dispatch &amp; SOC view')}{L('platform/#lone','Lone worker safety')}</div>
              <div><h4>Oversee</h4>{L('solutions/#inhouse','Contractor oversight')}{L('platform/#portal','Vendor reporting into your portal')}{L('platform/#credentials','Compliance records')}{L('platform/#reconciliation','Invoice verification')}</div>
              <div><h4>Own the data</h4>{L('platform/#api','API &amp; exports')}{L('platform/#levels','Automation levels')}{L('company/#trust','Trust &amp; security')}</div>
            </div></div>
          </div>
          <div class="side">
            <a class="feat" href="{b}resources/automated-scheduling-and-california-admt-rules/"><span class="eyebrow">Featured guide</span><b>Automated scheduling and California's ADMT rules</b><span>Notice, review and records when software proposes who works.</span></a>
            <div class="badges"><span>Offline-first</span><span>AI text labeled</span><span>No training on client data</span><span>SOC 2 roadmap</span></div>
            <a class="btn btn-primary btn-sm" href="{b}pricing/#request">Get a demo</a>
          </div>
        </div></div>
      </li>
      <li><button type="button" aria-expanded="false" aria-controls="mega-solutions">Solutions</button>
        <div class="mega" id="mega-solutions"><div class="wrap">
          <div class="cols">
            <div><h4>By business need</h4>{L('solutions/#operations','Streamline operations')}{L('solutions/#safety','Safety &amp; incident response')}{L('solutions/#margin','Protect margin &amp; billing')}{L('solutions/#payroll','Automate payroll &amp; workforce')}{L('solutions/#compliance','Stay compliant')}{L('solutions/#roi','Prove ROI &amp; visibility')}</div>
            <div><h4>By organization type</h4>{L('solutions/#firms','Security firms')}{L('solutions/#inhouse','In-house security teams')}</div>
            <div><h4>By industry</h4>{L('solutions/#industries','Event &amp; venue security')}{L('solutions/#industries','Corporate campuses')}{L('solutions/#industries','Hospitality')}{L('solutions/#industries','Residential communities')}{L('solutions/#industries','Logistics &amp; industrial')}{L('solutions/#industries','Healthcare')}</div>
          </div>
          <div class="side">
            <a class="feat" href="{b}resources/duty-free-rest-breaks-in-california/"><span class="eyebrow">Featured guide</span><b>Duty-free rest breaks in California</b><span>What Augustus v. ABM requires of a guard schedule.</span></a>
            <a class="btn btn-primary btn-sm" href="{b}pricing/#request">Get a demo</a>
          </div>
        </div></div>
      </li>
      <li><button type="button" aria-expanded="false" aria-controls="mega-support">Support</button>
        <div class="mega" id="mega-support"><div class="wrap">
          <div class="cols two">
            <div><h4>Get help</h4>{L('support/','Support overview')}<a href="#" data-jessica>Jessica, AI assistant<small>Available 24/7</small></a>{L('support/#email','Email a specialist')}{L('support/#faq','Knowledge base')}</div>
            <div><h4>Learn</h4>{L('support/#academy','Automaata Academy')}{L('support/#status','System status')}{L('resources/','Guides &amp; articles')}</div>
          </div>
          <div class="side">
            <a class="feat" href="#" data-jessica><span class="eyebrow">24/7</span><b>Ask Jessica anything about Automaata</b><span>Instant answers, with an in-browser AI model you can switch on.</span></a>
            <a class="btn btn-primary btn-sm" href="{b}support/#email">Contact support</a>
          </div>
        </div></div>
      </li>
      <li><button type="button" aria-expanded="false" aria-controls="mega-resources">Resources</button>
        <div class="mega" id="mega-resources"><div class="wrap">
          <div class="cols two">
            <div><h4>Library</h4>{L('resources/','All resources')}{L('resources/#guides','Guides')}{L('resources/#blog','Blog articles')}{L('resources/#updates','Product updates')}</div>
            <div><h4>More</h4>{L('resources/#cases','Case studies')}{L('support/#academy','Automaata Academy')}</div>
          </div>
          <div class="side">
            <a class="feat" href="{b}resources/checkpoint-verification-nfc-qr-gps/"><span class="eyebrow">Featured guide</span><b>Checkpoint verification: NFC, QR or GPS?</b><span>Where each method is reliable and how to mix them on one tour.</span></a>
            <a class="btn btn-primary btn-sm" href="{b}pricing/#request">Get a demo</a>
          </div>
        </div></div>
      </li>
      <li><button type="button" aria-expanded="false" aria-controls="mega-company">Company</button>
        <div class="mega" id="mega-company"><div class="wrap">
          <div>
            <p style="font-family:var(--display);font-weight:700;font-size:18px;margin-bottom:14px">Built in San Francisco for the people who protect people.</p>
            <div class="badges" style="margin-bottom:18px"><span>Founded 2026</span><span>San Francisco</span><span>4 automation levels</span><span>AI, disclosed</span></div>
            <div class="cols">
              <div><h4>Company</h4>{L('company/','About Automaata')}{L('company/#values','What we believe')}{L('company/#leadership','Leadership')}</div>
              <div><h4>Work with us</h4>{L('company/#careers','Careers')}{L('support/#email','Contact')}</div>
              <div><h4>Trust</h4>{L('company/#trust','Trust &amp; security')}{L('legal/#ai','AI use disclosure')}</div>
            </div>
          </div>
          <div class="side">
            <a class="feat" href="{b}resources/the-four-automation-levels-explained/"><span class="eyebrow">Featured article</span><b>The four automation levels, explained</b><span>How Automaata decides what to do on its own.</span></a>
            <a class="btn btn-primary btn-sm" href="{b}pricing/#request">Get a demo</a>
          </div>
        </div></div>
      </li>
      <li><a href="{b}pricing/"{cur('pricing')}>Pricing</a></li>
      <li class="tt"><button class="theme-toggle" id="theme-toggle" type="button" role="switch" aria-checked="false" title="Dark mode"><span class="sr">Dark mode</span></button></li>
      <li class="cta"><a class="btn btn-primary btn-sm" href="{b}pricing/#request">Get a demo</a></li>
    </ul>
  </div>
</header>
<main id="main">
"""

def footer(depth):
    b = base_for(depth)
    def L(href, text): return f'<li><a href="{b}{href}">{text}</a></li>'
    return f"""
</main>
<footer>
  <div class="wrap top">
    <div class="about">
      <a class="brand" href="{b}index.html">{MARK}automaata<small>.ai</small></a>
      <p>AI-first security workforce management for contract guard companies and in-house security teams. Field operations, back office and client reporting on one record.</p>
      <div class="mini"><span>Founded 2026 · San Francisco</span><span>AI text labeled</span><span>No training on client data</span></div>
    </div>
    <div><h4>Platform</h4><ul>{L('platform/','Platform overview')}{L('platform/#app','Officer App')}{L('platform/#console','Ops Console')}{L('platform/#portal','Client Portal')}{L('platform/#tours','Checkpoint tours')}{L('platform/#incidents','Incident reporting')}{L('platform/#scheduling','Scheduling')}{L('platform/#time','Time &amp; attendance')}{L('platform/#billing','Billing')}{L('platform/#levels','Automation levels')}{L('platform/#jessica','Jessica AI')}{L('platform/#api','API &amp; integrations')}</ul></div>
    <div><h4>Solutions</h4><ul>{L('solutions/#operations','Streamline operations')}{L('solutions/#safety','Safety &amp; incidents')}{L('solutions/#margin','Margin &amp; billing')}{L('solutions/#payroll','Payroll &amp; workforce')}{L('solutions/#compliance','Compliance')}{L('solutions/#roi','ROI &amp; visibility')}{L('solutions/#firms','Security firms')}{L('solutions/#inhouse','In-house teams')}{L('solutions/#industries','Industries')}</ul></div>
    <div><h4>Resources</h4><ul>{L('resources/','All resources')}{L('resources/#guides','Guides')}{L('resources/#blog','Blog')}{L('resources/#updates','Product updates')}{L('resources/#cases','Case studies')}{L('support/#academy','Academy')}</ul></div>
    <div><h4>Company</h4><ul>{L('company/','About')}{L('company/#values','Values')}{L('company/#leadership','Leadership')}{L('company/#careers','Careers')}{L('company/#trust','Trust &amp; security')}{L('support/#email','Contact')}</ul></div>
    <div><h4>Support</h4><ul>{L('support/','Support overview')}<li><a href="#" data-jessica>Ask Jessica (24/7)</a></li>{L('support/#email','Email support')}{L('support/#faq','Knowledge base')}{L('support/#status','System status')}{L('pricing/','Pricing')}</ul></div>
  </div>
  <div class="legal"><div class="wrap">
    <span>© <span data-year>2026</span> Automaata · automaata.ai · San Francisco, California · Independent, not affiliated with any other security software provider.</span>
    <span class="links"><a href="{b}legal/#privacy">Privacy</a><a href="{b}legal/#terms">Terms</a><a href="{b}legal/#ai">AI use</a><a href="{b}legal/#accessibility">Accessibility</a><a href="{b}sitemap.xml">Sitemap</a></span>
  </div></div>
</footer>
<script src="{b}assets/site.js"></script>
<script src="{b}assets/jessica.js"></script>
</body>
</html>
"""

# ------------------------------------------------------------------ articles
def load_articles():
    arts = []
    for f in sorted((PAGES / 'resources').glob('*.html')):
        d, body = meta(f.read_text())
        d['slug'] = f.stem; d['body'] = body
        arts.append(d)
    arts.sort(key=lambda a: a.get('date', ''), reverse=True)
    return arts

def article_page(a):
    depth = 2
    path = f'/resources/{a["slug"]}/'
    out = ROOT / 'resources' / a['slug'] / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    date = datetime.date.fromisoformat(a['date']).strftime('%b %d, %Y')
    body = f"""
<article class="article wrap">
  <p class="eyebrow"><span><a href="../" style="text-decoration:none">Resources</a></span><span>{html.escape(a['type'])}</span><span>{date}</span><span>{a.get('read','5')} min read</span></p>
  <h1>{a['title']}</h1>
  <p class="lede">{a['summary']}</p>
  <div class="body">
{a['body']}
  </div>
  <p class="src" style="border:0;padding-top:28px"><a class="btn btn-primary" href="../../pricing/#request">Get a demo</a> &nbsp; <a class="arrow" href="../">All resources →</a></p>
</article>
"""
    extra = f'<meta property="article:published_time" content="{a["date"]}">'
    out.write_text(head(a['title'], a['summary'], path, depth, extra) + nav('resources', depth) + body + footer(depth))
    return path

def resources_index(arts):
    items = []
    for a in arts:
        date = datetime.date.fromisoformat(a['date']).strftime('%b %d, %Y')
        items.append(f"""<a class="res-item" href="{a['slug']}/" data-type="{a['type_key']}" data-topics="{a.get('topics','')}" data-aud="{a.get('aud','firms inhouse')}">
  <div><div class="meta"><span class="type">{html.escape(a['type'])}</span><span>{date}</span><span>{a.get('read','5')} min read</span></div><h3>{a['title']}</h3><p>{a['summary']}</p></div>
  <span class="arrow">Read more →</span>
</a>""")
    return '\n'.join(items), len(items)

# ------------------------------------------------------------------ build
def build():
    arts = load_articles()
    type_keys = {'Guide': 'guide', 'Blog article': 'blog', 'Product update': 'update', 'Case study': 'case'}
    for a in arts:
        a['type_key'] = type_keys.get(a['type'], 'blog')
    art_paths = [article_page(a) for a in arts]
    res_items, res_n = resources_index(arts)

    pages = [
        ('index.html', 'index.html', '/', 0),
        ('platform.html', 'platform/index.html', '/platform/', 1),
        ('solutions.html', 'solutions/index.html', '/solutions/', 1),
        ('support.html', 'support/index.html', '/support/', 1),
        ('resources.html', 'resources/index.html', '/resources/', 1),
        ('company.html', 'company/index.html', '/company/', 1),
        ('pricing.html', 'pricing/index.html', '/pricing/', 1),
        ('legal.html', 'legal/index.html', '/legal/', 1),
    ]
    urls = []
    for src, dest, path, depth in pages:
        d, body = meta((PAGES / src).read_text())
        body = body.replace('{{RESOURCE_ITEMS}}', res_items).replace('{{RESOURCE_COUNT}}', str(res_n))
        out = ROOT / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(head(d['title'], d['desc'], path, depth) + nav(d.get('nav', ''), depth) + body + footer(depth))
        urls.append(path)
        print('wrote', dest)
    urls += art_paths
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>')
    sm.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sm) + '\n')
    print('sitemap:', len(urls), 'urls')

if __name__ == '__main__':
    build()
