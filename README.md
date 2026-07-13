# Portfolio

A personal portfolio built as a plain HTML application styled with Tailwind CSS.

## Getting started

Just open `index.html` in your browser, no build step required. Tailwind is
loaded via the Play CDN, so utility classes work instantly.

```bash
open index.html
```

## Structure

```
portfolio/
├── index.html      # main page
├── css/styles.css  # custom styles + fonts (on top of Tailwind)
├── js/main.js      # page scripts
├── assets/         # images, icons, etc.
└── README.md
```

## Going to production (optional)

The Play CDN is perfect for prototyping but not recommended for production.
When you're ready, switch to a proper Tailwind build:

```bash
npm install -D tailwindcss
npx tailwindcss init
# build:
npx tailwindcss -i ./css/input.css -o ./css/output.css --watch
```

Then replace the `<script src="https://cdn.tailwindcss.com"></script>` tag with
a link to the compiled `output.css`.
