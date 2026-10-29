# automaata.ai

Static marketing site for Automaata, hosted on GitHub Pages from the `main` branch (root folder, custom domain `automaata.ai`).

## Editing

Page bodies live in `tools/pages/*.html`; articles in `tools/pages/resources/*.html`. Each starts with a front-matter comment (`title`, `desc`, and for articles `type`, `date`, `topics`, `aud`, `summary`). Shared header, mega-menus and footer are in `tools/build.py`. Styles are `assets/site.css`; behaviour `assets/site.js`; the AI assistant `assets/jessica.js` (knowledge base at the top of that file).

After editing, rebuild and commit the generated pages:

```
python3 tools/build.py
```

`index.html`, `platform/`, `solutions/`, `support/`, `resources/`, `company/`, `pricing/`, `legal/` and `sitemap.xml` are generated; edit the sources, not the output.

## Jessica

Guided mode answers from the knowledge base in `assets/jessica.js`. Full-AI mode loads an open-source model (Llama 3.2 / Qwen 2.5, MLC builds) via WebLLM and runs it in the visitor's browser over WebGPU; no server or API key is involved.
