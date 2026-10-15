# bwylde-social-assets

Public image host and post renderer for b.wylde social content. Everything here is public. Never put anything private in this repo.

## Layout
- `pipeline/render_post.py` renders a JSON spec into Instagram-ready JPGs (1080x1350, story 1080x1920)
- `pipeline/fonts/` Bricolage Grotesque, Space Grotesk, Instrument Serif Italic
- `posts/YYYY-MM-DD-slug/slide-N.jpg` rendered posts, one folder per post (public URLs via raw.githubusercontent.com)
- `carousels/` earlier hand-built carousels

## Render
    pip install playwright pillow --break-system-packages   # only if missing
    python3 pipeline/render_post.py spec.json posts/2026-10-14-short-slug

Spec: `{"slides":[{"template":"quote-plum","fields":{"eyebrow":"Permission","headline":"Nothing about you is *broken*."}}]}`

Rich text: `*word*` becomes the Citron serif italic word. A final `.` or `?` becomes the Citron period. `\n` is a line break. The renderer refuses em/en dashes.

## Templates and fields
- `cover`: eyebrow, headline, line, cta, counter
- `body`: eyebrow, headline, number, title, text, counter
- `quote-ink`, `quote-plum`, `quote-emerald`, `quote-bone`: eyebrow, headline, tag
- `sign-ink`, `sign-plum`, `sign-emerald`, `sign-bone`: eyebrow, number, headline, text, tag (numbered "signs" slide: big serif number, bold statement, one supporting sentence)
- `quote-card`: eyebrow, headline, tag
- `announce`: eyebrow, headline, text, strip, button
- `story`: eyebrow, headline, chips (list), text
- `stat`: eyebrow, number, text, source, tag
- `define`: eyebrow, term, pos, text, example, tag
- `myth`: myth, reality, tag
- `list`: eyebrow, headline, items (3), tag

## Public image URL
`https://raw.githubusercontent.com/brittanysandovalrn-dot/bwylde-social-assets/main/posts/<folder>/slide-N.jpg`

## Carousel formats
- **Explainer** (wordier, deeper): `cover` opener with an arrow (eyebrow, headline, line, cta "Swipe →", counter), 5 numbered `sign-*` slides that walk one idea step by step (2 to 3 sentences each), `quote-card` closer, `announce` GoFeral slide.
- **Signs list**: `cover` opener with an arrow ("Things that feel like X but are actually signs Y:"), 5 numbered `sign-*` slides, `quote-card` closer, `announce` GoFeral slide.
- **Quote scroll** (short): 6 `quote-*` slides, `quote-card` closer, `announce` GoFeral slide.
- Longer formats always open with the `cover` arrow slide. The `announce` slide is tailored to each post: its headline and text say what GoFeral would do for that post's specific theme (about 25 words, keep it above the strip). Captions use emoji that fit the content, never one default.
