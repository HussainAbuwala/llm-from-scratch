# YouTube Metadata — Channel Intro (The Unplanned Stack)

Canvas: `canvas/channel_intro.excalidraw` · Plan: `../CHANNEL_INTRO_PLAN.md`

> **Not yet recorded.** Everything here is ready except chapter timings, which
> can only be measured from a real cut. See §7.

---

## 1. Read this before uploading: a trailer is not a normal video

Two things make this upload different, and both change what you do with it.

**It autoplays muted.** On your channel homepage, for anyone not subscribed,
YouTube plays this automatically with the sound off. The first five seconds have
to work as a silent image. Shot 00 — the wordmark and the map — does exactly
that, which is the main argument for opening on it rather than on your face.

**YouTube's trailer slot wants 30–90 seconds; your video is 4–5 minutes.** That
is a real mismatch and worth deciding deliberately:

- **Recommended:** publish the full 4–5 minute version as a normal video, then cut
  a **60–90 second** version for the trailer slot itself — shots 00, 01, 07, 08,
  11. Same recording, no reshoot. The long one earns watch time in the feed; the
  short one converts on the channel page.
- **Simpler:** use the full version in both places and accept that most autoplay
  viewers leave partway. Not fatal — a trailer is measured on subscribes, not
  retention.

Do not shorten the *recording* to fit the trailer slot. The 4–5 minute version is
the better video; the trailer cut is a derivative.

---

## 2. Title

**Recommended:**

```
Start Here — The Unplanned Stack
```

"Start Here" is the convention for a channel trailer and does its main job:
telling a new visitor on your channel page which video to press first. It pairs
with the crooked-stack thumbnail, which carries the personality while the title
carries the function.

**Alternatives**

| Title | When to use |
|---|---|
| `What This Channel Is (and Why It Has a Weird Name)` | If you want it to work as a regular video in the feed too — curiosity gap, and the stack thumbnail answers it |
| `I'm Figuring It Out in Public. Here's the Plan.` | Leads with the honesty angle rather than the name |
| `Welcome to The Unplanned Stack` | Safest, most generic, lowest ceiling |

Avoid putting "channel trailer" or "intro" in the title. It tells a viewer this
video is admin rather than content.

---

## 3. Description

Copy from here to the end of the block:

```
I'm Hussain — a software developer who is much better at understanding things than at planning them.

In software, a "stack" is a carefully chosen set of technologies you pick before you build. Life is not like that. Mine is a career, a creative habit, and a new country in Canada, none of which arrived in a planned order. Hence the name.

This channel is where I take something complicated, work out how it actually operates, and then show you — including the parts I got wrong on the way.

── WHAT'S HERE ───────────────────

Systems from First Principles — real software systems rebuilt from the simplest version that works, then broken until you can see why the complicated version exists:
  · how can a webpage hijack an AI agent?
  · how can a lost tracker find your suitcase?
  · how do many people edit one design at once, without losing work?
  · why do production LLMs split reading your prompt from writing the answer?

Every one of them asks the same three questions:
  1. What problem are we solving?
  2. Why does the simplest solution fail?
  3. What does each added piece of complexity buy us?

Building an LLM From Scratch — a long series building a language model from nothing: counting, then gradients, then attention, then a small GPT trained on a laptop. No API keys, no black boxes.

── HOW I MAKE THESE ──────────────

Everything is checked against first-party engineering sources, and claims are labelled Documented, Inferred, or Proposed, so you always know which parts are established and which are my simplification. Company engineering posts are dated snapshots, not proof of a current architecture, and I say so.

I am also learning plenty of this as I go. When I get something wrong, the correction goes in the next video.

── THE APPROACH ──────────────────

The topics will move around — technology, career, creativity, building a life somewhere new. The approach won't: stay curious, understand things deeply, and share the real process, including what doesn't work.

If you're figuring things out as you go too, you're in the right place.

#softwareengineering #learninpublic #systemsdesign
```

Notes:

- Only the first ~150 characters show before "…more", so the self-deprecating
  first line is doing the work. Keep it.
- Add the two playlist links under "WHAT'S HERE" once the playlists exist.
- No repo link here. This is a channel-level video; the repos belong on the
  individual episodes they support.
- This description should stay accurate for a year. Nothing dated, no
  "currently", no video counts.

---

## 4. Tags

```
the unplanned stack, systems from first principles, software engineering explained, how systems work, computer science explained, learn in public, software developer, distributed systems, system design, llm explained, first principles thinking, engineering deep dive, tech explainer, building in public, developer channel
```

---

## 5. Upload settings

| Field | Value |
|---|---|
| Visibility | Public |
| Category | Science & Technology |
| Language | English |
| Made for kids | **No** |
| Altered content disclosure | **No** |
| Comments | On |
| Playlist | None — a trailer sits outside the series playlists |
| License | Standard YouTube License |
| Allow embedding | Yes |

**Then set it as the trailer**, which is a separate step and easy to forget:

> YouTube Studio → Customization → Layout → **Video spotlight** →
> *Channel trailer for people who haven't subscribed*

While you are there, set **Featured video for returning subscribers** to your most
recent real episode, not this one. Subscribers should never land on the trailer.

---

## 6. Thumbnail

Three at `youtube/thumbnails/`, all blueprint-themed to match the video.

| File | Concept | |
|---|---|---|
| `channel_stack.png` | A tidy tech stack beside the one you actually have | **recommended** |
| `channel_intro_alt.png` | `UnplannedStackError: no blueprint found` | Sharper, but only for developers |
| `channel_intro.png` | The plan vs the route actually taken | Weakest — needs a diagram parsed |

`channel_stack.png` wins because the joke is a silhouette: two towers, one tidy
and one about to fall over. That still reads at 320px in a feed, where the
decision is made, after every label has turned to mush.

Source files are `canvas/thumbnail_stack.excalidraw` and friends — export the
final PNG from Excalidraw itself (select frame → Export image → PNG, "only
selected") rather than using the committed render.

---

## 7. Chapters

**Don't add any.** At 4–5 minutes across twelve shots, each chapter would be
roughly 25 seconds, several would fall under YouTube's 10-second minimum, and the
whole list would be silently ignored. Chapters help a 30-minute theory video, not
a trailer.

If the recording comes in much longer than planned and you want them anyway:

```bash
.venv/bin/python youtube/chapters.py "~/Movies/llm-series/<file>.mp4"
```

Then read the shot headings off the generated sheet, as with episode 0.

---

## 8. Pinned comment

```
The name is a joke about software: a "stack" is the set of technologies you choose on purpose before you build. Mine — a career, making things, moving to Canada — arrived in no particular order and mostly without my permission.

Two places to start:
· Systems from First Principles — real systems rebuilt from the simplest thing that works
· Building an LLM From Scratch — a language model from nothing, one episode at a time

If I've got something wrong, tell me. Corrections go in the next video.
```

---

## 9. End screen

- **Subscribe element**, plus **one video**: your strongest existing Short or the
  Figma multiplayer long-form. Not "latest upload" — a trailer should send people
  to your best work, not your newest.
- Keep the end screen off the final line of the video. The invitation is the
  close; let it land before the cards appear.

---

## 10. Pre-publish checklist

- [ ] First 5 seconds work with the sound off
- [ ] Set as channel trailer in Customization → Layout
- [ ] Featured video for returning subscribers set to something else
- [ ] Thumbnail checked at 20% zoom
- [ ] Description's first 150 characters read well truncated
- [ ] Playlist links added once playlists exist
- [ ] Watched once on a phone, muted, to check it survives autoplay
