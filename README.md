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
- `thread-plum`, `thread-emerald`, `thread-bone`, `thread-citron`, `thread-ink`: headline (use `\n\n` for paragraph breaks inside a slide), optional kicker (bold accent line under the text, good for the payoff slide), tag (use "n/9" counters). Medium text, vertically centered.
- `full-plum`, `full-emerald`, `full-bone`, `full-citron`, `full-ink`: headline, tag. One big sentence per slide, vertically centered. Keep it to about 22 words or less; the renderer shrinks long text to fit.
- `whisper-plum`, `whisper-emerald`, `whisper-bone`, `whisper-citron`, `whisper-ink`: headline, tag (use "n/12" counters). Small italic serif, vertically centered in open space, one thought per slide, about 8 to 22 words.
- Any slide can add `"grain": true` next to `template` and `fields` for a soft paper-grain texture. Default it on for `thread-*` and `whisper-*`; optional elsewhere.

## Public image URL
`https://raw.githubusercontent.com/brittanysandovalrn-dot/bwylde-social-assets/main/posts/<folder>/slide-N.jpg`

## Carousel formats
- **Explainer** (wordier, deeper): `cover` opener with an arrow (eyebrow, headline, line, cta "Swipe →", counter), 5 numbered `sign-*` slides that walk one idea step by step (2 to 3 sentences each), `quote-card` closer, `announce` GoFeral slide.
- **Signs list**: `cover` opener with an arrow ("Things that feel like X but are actually signs Y:"), 5 numbered `sign-*` slides, `quote-card` closer, `announce` GoFeral slide.
- **Quote scroll** (short): 6 `quote-*` slides, `quote-card` closer, `announce` GoFeral slide.
- **Pattern cards / block cards (`period-*`, `cut-*`) are RETIRED** (the oversized circle read as wonky). The renderer rejects them. Use Quote scroll, Mirror cards or Shape cards for standalone card sets.
- Longer formats always open with the `cover` arrow slide. The `announce` slide is tailored to each post: its headline and text say what GoFeral would do for that post's specific theme (about 25 words, keep it above the strip). Captions use emoji that fit the content, never one default.

- **Mirror cards** (9 slides, no cover): 7 `mir-bone`/`mir-citron`/`mir-plum`/`mir-emerald`/`mir-ink` big-type slides (fields headline with one *word*, tag; one validating "this is me" line each), then a `list` off-ramp slide (eyebrow "Try this in 60 seconds", 3 steps, tag "No app needed"), then a tailored `announce`. Every caption asks for a share (story or send) and a save.

- **Cover variants (profile-grid variety):** the profile grid shows slide 1 of every post, so openers must not all look alike. For Explainer and Signs list posts, swap the `cover` template for one of: `cover` (ink), `cover-plum`, `cover-emerald`, `cover-bone`, `cover-citron` (same card composition, different color) or `slab-plum`, `slab-emerald`, `slab-bone`, `slab-citron` (a hard color field over an ink base with a Citron Break line). Same fields as `cover` (eyebrow, headline, line, cta, counter; the slab ignores counter). Never put the same cover color or composition on two posts in a row.

- **Story thread** (9 slides, no cover): 8 `thread-*` slides telling one first-person-feeling scene or "you" scenario with a hook on slide 1, a build, and a reframe/payoff on slide 8 (a contrasting color, with a `kicker`), then a tailored `announce`. Layout field value: "Story thread".
- **Full-bleed** (5 slides, no cover): 4 `full-*` slides, one big sentence each, then a tailored `announce`. The shortest format. Layout field value: "Full-bleed".
- **Whisper scroll** (12 slides, no cover): 10 `whisper-*` quiet one-thought slides, a share prompt slide (contrasting color), then a tailored `announce`. Built for saves and sends. Layout field value: "Whisper scroll".
- Never use an ink/black color for slide 1 of a Story thread, Full-bleed or Whisper scroll post (grid rule). Copy may swear when it fits Britt's voice.

- **Grid rule:** slide 1 is what the profile grid shows. Never use ink/black as slide 1, and rotate colors across neighboring posts, including within the same layout.
