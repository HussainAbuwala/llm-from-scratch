# Video 0 Plan: Series Introduction

Status: Ready to record

Canvas: `canvas/series_intro.excalidraw` (10 scenes)
Scope source: [SERIES_PLAN.md](SERIES_PLAN.md)

## 1. What this video is for

One job: a viewer who has never heard of you decides whether to commit to a long
series. That decision is made on three questions, in this order:

1. Is this person going to teach me something real, or read a Wikipedia article?
2. Will this series actually finish, or die at episode 3?
3. Is it pitched at me, or above/below me?

Every scene below exists to answer one of those. Nothing else belongs here.

## 2. What this video is NOT

- Not a lesson. Do not teach the bigram model here. The moment you start
  explaining, this becomes episode 1 with a worse title.
- Not a life story. The personal framing is the honesty hook, not the content.
- Not a hype reel. No "this will change everything". The credibility of the
  series is that it is small and finishable.

Target runtime: **7–9 minutes.** If it runs past 11, cut scene 07 or 09.

## 3. Title and packaging

**Recommended:** `I'm Building an LLM From Scratch (and Learning It As I Go)`

Alternatives:

- `Building an LLM From Scratch — the Plan`
- `14 Episodes to a Working LLM. Episode 0.`
- `I Can Use an LLM. I Can't Explain One. So I'm Building One.`

The last one is the strongest hook but the weakest search term. Recommendation:
use the first as the title and the last as the opening line.

Thumbnail: you on one side, the four-step arc (COUNT → LEARN → ATTEND →
GENERATE) on the other, three words maximum. The arc is the promise; show the
whole staircase so the scope reads instantly.

## 4. Segment plan

| Time | Canvas scene | On screen | The beat |
|---|---|---|---|
| 0:00–0:35 | 01 · Title | Face, then canvas title | The hook: "I use these every day. I could not explain one to you." |
| 0:35–1:40 | 02 · The one idea | The next-token loop | There is exactly one idea. Show the bars. Do not explain them yet. |
| 1:40–2:30 | 03 · Using vs understanding | Two panels | Name the gap. Admit you're learning. State the format. |
| 2:30–3:30 | 04 · The arc | Four rising steps | Four moves, each because the last one hit a wall. The scope in one picture. |
| 3:30–4:45 | 05 · The episodes | Three columns, 14 chips | Concrete list. Say plainly where it ends and what is not included. |
| 4:45–5:40 | 06 · Theory + code | Two panels | Every concept ships twice. State the on-camera honesty rule. |
| 5:40–6:30 | 07 · The maths | Timeline strip | Kill the maths objection. No prerequisite course. |
| 6:30–7:20 | 08 · Honest terms | Three panels | What you need; what you don't; what is not promised. |
| 7:20–7:50 | 09 · What you get | Four artefact cards | Everything is free and in the description. How to follow along. |
| 7:50–8:30 | 10 · Next | Terminal output + claims | Tease episode 1. End on the generated names, not on a request to subscribe. |

## 5. Beat notes

### Scene 01 — the hook

Open on your face, not the canvas. One sentence, no preamble:

> I use these things every day, and if you asked me to explain how one actually
> works, I couldn't. So I'm going to build one, from nothing, and you can watch
> me learn it.

Then cut to canvas. Say the series name once.

Do not open with "hey guys, welcome back to the channel."

### Scene 02 — the one idea

This is the most important 60 seconds in the video. The viewer must leave with
exactly one mechanical fact: **a language model outputs a probability for every
possible next token, and generation is doing that repeatedly.**

Point at the bars. Say the numbers out loud. Trace the loop arrow with the
cursor. Then say the line that buys the whole series:

> GPT-4 does this. The model I build in the next episode does this. The distance
> between them is engineering, not a different idea.

Resist explaining softmax, tokens, or attention. You have not earned those yet.

### Scene 03 — the honesty beat

Say clearly that you are learning this, that you will check primary sources, and
that when you get something wrong you will say so on camera and fix it. This is
the differentiator against every polished-expert tutorial. It only works if you
actually do it later.

### Scene 04 — the arc

Walk up the staircase with the cursor: count, learn, attend, generate. One
sentence per step, and for each, name the wall that forces the next step:

- COUNT → the table explodes
- LEARN → fixed context wastes capacity
- ATTEND → now we need to train it properly
- GENERATE → done

### Scene 05 — the episode list

Read the part headings, not all fourteen titles. Then say the two sentences that
determine whether people trust the series:

> It ends with a small Transformer that we wrote, trained on a laptop, that
> generates text. It does not go into fine-tuning or serving. I'd rather finish
> fourteen episodes than abandon twenty-five.

### Scene 06 — theory + code

Explain the two-video format: theory video is this canvas and a worked example;
build video is an empty file and a terminal. Then the rule:

> The number I work out by hand and the number the code prints have to match, on
> screen. If they don't, that's the video.

### Scene 07 — the maths

Common reason people quit. Walk the timeline. Emphasise: no prerequisite
chapter, each idea arrives in the episode that needs it, in the smallest useful
form. Say explicitly: "if a symbol is on screen, I've already told you what it
means."

### Scene 08 — honest terms

Read the NOT PROMISED panel almost verbatim. Under-promising here is what makes
scene 05 believable.

### Scene 10 — the tease

Show the generated names. Then list what the model lacks — no neural network, no
attention, one character of memory — and land on:

> It still learns real structure from text, and it fails in ways that explain
> why everything after it exists.

End there. A short "episode 1 is next" is enough.

## 6. Recording notes specific to this video

- More A-roll than a normal episode: aim for ~40% face. Scenes 01, 03, 05, 08
  are talking beats; the canvas is support.
- Scenes 02 and 04 are canvas-led; keep yourself in the corner bubble.
- Do not read the canvas text aloud verbatim. The canvas is the skeleton; your
  voice is the muscle. If a scene has a paragraph on it, paraphrase it.

## 7. Description skeleton

```
I can use an LLM. I can't explain one. So I'm building one from scratch —
counting, then learning, then attention, then a small GPT — and learning the
maths as I go.

Series plan, theory docs, code, and the Excalidraw canvas from this video:
<repo link>

00:00  I can't explain one
00:35  The only idea in the series
01:40  Using vs understanding
02:30  The four moves
03:30  All 14 episodes
04:45  Theory video + build video
05:40  The maths, just in time
06:30  What you need (and what I'm not promising)
07:20  What you get
07:50  Next: the smallest language model
```

## 8. Success criteria

- A viewer can restate the next-token idea after one watch.
- A viewer can say where the series ends.
- A viewer with no ML background does not feel excluded, and one with ML
  background does not feel patronised.
- Nothing is promised that `SERIES_PLAN.md` does not commit to.
