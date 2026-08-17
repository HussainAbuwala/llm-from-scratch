# Recording Setup: Canvas + Corner Bubble

Status: Working setup notes

This covers the format you described: the Excalidraw canvas fills the frame, you
appear as a small bubble in a corner. It applies to every theory video in the
series.

## 1. Why the frames are 1600×900

Every scene in `canvas/*.excalidraw` is a 1600×900 Excalidraw **frame** — exactly
16:9. That means:

- Select a frame, press **Shift+2** ("zoom to selection") and the viewport is
  filled by that scene, correctly framed, with no manual panning.
- Scenes are laid out left to right in one row, so the whole video is a single
  rightward journey through the canvas.
- Nothing important sits under the webcam bubble: the bottom-right ~360×260 of
  each frame is kept clear (see section 5 for the exception list).

Recommended presenting loop:

1. Click the frame name in the canvas (or press **Shift+2** with the frame
   selected) to snap to a scene.
2. Talk over it, annotating live with the pen tool.
3. Move to the next scene.

## 2. Excalidraw settings before recording

- **Zen mode** (`Alt+Z`) — hides the left panel and shrinks the UI. Do this.
- **View mode** (`Alt+R`) — hides all editing UI but also disables drawing. Use
  it only for scenes where you will not annotate.
- **Theme:** light. The canvas palette is tuned for light background; dark mode
  inverts the pastel fills unpredictably.
- **Turn off** the "Objects snap" and grid — they add visual noise on screen.
- Font is already set per element; do not change the default font mid-recording.
- Disable the canvas scrollbars in the hamburger menu if the option is present.

## 3. Live annotation is the point

Do not record a static canvas with a voiceover. The reason this format works is
that the viewer watches ideas being written. For each scene, plan **one thing you
will draw live**:

| Scene type | Draw live |
|---|---|
| Sliding window | Tick each transition off as you say it |
| Count matrix | Write the tally into the cell yourself |
| Normalisation | Write the division and the result |
| Funnel | Write each × 0.x as you narrate the survivors |
| Log table | Circle the row you are talking about |
| The k curve | Mark where you'd pick k |

Keep the pen colour red (`#e03131`) for live annotation so it is visually
distinct from the pre-drawn content. Bind that to a key before you start.

Annotations are throwaway. Before recording a second take, undo them
(`Cmd+Z`) — or better, work on a **copy** of the file so the source stays clean:

```bash
cp canvas/episode_01_bigram.excalidraw canvas/episode_01_bigram.RECORDING.excalidraw
```

## 4. Installing OBS

Current release is **OBS Studio 32.2.1**, which needs macOS 13 or newer. This
machine is macOS 26.2 on Apple Silicon, so either route works:

```bash
brew install --cask obs
```

Or download the **Apple Silicon (arm64)** installer from the official site:
<https://obsproject.com/download>. Take the arm64 build, not Intel — the Intel
one runs under Rosetta and encodes noticeably slower.

Only ever install OBS from `obsproject.com` or Homebrew. It is one of the most
impersonated apps on the web; search results are full of mirrors that bundle
adware.

## 5. macOS permissions — do this before anything else

This is where most first-time OBS setups appear "broken": a black screen or a
dead webcam is almost always a missing permission, not a misconfiguration.

Open **System Settings → Privacy & Security** and enable OBS under:

| Permission | Needed for |
|---|---|
| Screen & System Audio Recording | Capturing the browser window. Without it you get a black screen. |
| Camera | The webcam bubble |
| Microphone | Your voice |
| Accessibility | Global hotkeys **while the browser is focused** — i.e. scene switching and start/stop while you present |

Quit and reopen OBS after granting each one; several only take effect on
restart. The Accessibility one is easy to skip and then wonder why your
scene-switch hotkey does nothing while Excalidraw has focus.

Skip the auto-configuration wizard on first launch — it optimises for streaming.
Use the settings below instead.

## 6. OBS settings

> **Shortcut:** `obs/install_obs_setup.py` applies everything in sections 6 and 7
> for you, as a new scene collection and profile called *LLM Series*. Quit OBS,
> run it, reopen OBS. Sections 6–7 remain the reference for what it did and how
> to change it by hand.
>
> One deliberate difference: the installed profile uses **Simple** output mode
> with `apple_h264` at *Indistinguishable Quality*, because it is one less thing
> to misconfigure. The Advanced-mode CRF settings below are the upgrade path once
> you have a few recordings behind you.

**Settings → Video**

| Field | Value |
|---|---|
| Base (Canvas) Resolution | 1920×1080 |
| Output (Scaled) Resolution | 1920×1080 |
| Downscale Filter | Lanczos |
| FPS | 30 |

30 fps is right here. You are showing static diagrams and a talking head;
60 fps doubles the file size and buys nothing.

**Settings → Output** → set Output Mode to **Advanced**, then the Recording tab:

| Field | Value |
|---|---|
| Type | Standard |
| Recording Format | **Hybrid MP4** |
| Video Encoder | Apple VT H.264 Hardware Encoder |
| Rate Control | CRF (or "Quality") around 20 — if only CBR is offered, 14000 Kbps |
| Keyframe Interval | 2s |
| Audio Track | 1 |

Hybrid MP4 is the important one: a plain MP4 is corrupt if OBS or the machine
crashes mid-recording, and MKV needs remuxing before most editors will touch it.
Hybrid MP4 survives a crash and needs no remux.

Prefer H.264 over HEVC. HEVC files are smaller but far heavier to scrub through
while editing, and you will be scrubbing a lot.

**Settings → Audio:** sample rate 48 kHz, channels stereo, and set your
microphone as Mic/Auxiliary Audio. Leave **Settings → Advanced** alone.

## 7. Scenes and the webcam bubble

Build three scenes:

| Scene | Contents | Used for |
|---|---|---|
| `01 Canvas + bubble` | Browser window + bubble | Most of every theory video |
| `02 Face full` | Webcam full frame | Talking beats — intro scenes 01, 03, 05, 08 |
| `03 Editor + bubble` | Editor/terminal window + bubble | Build videos |

### The screen source

Add source → **macOS Screen Capture** → Method: **Window** → pick your browser
window. Window capture rather than display capture, because it automatically
excludes OBS itself, the menu bar, and notification banners.

Enable **Show Cursor**. You are pointing at things; the cursor is part of the
teaching.

### The webcam source

Add source → **Video Capture Device** → `FaceTime HD Camera`.

Worth knowing: your iPhone works as a Continuity Camera and shows up in this
same list. It is a large step up in image quality over the built-in FaceTime
camera, and it costs nothing to try.

Then right-click the webcam source → **Filters**, and add these two **in this
order**:

1. **Crop/Pad** — crop the left and right equally to make the source square.
   From a 1920×1080 feed, crop 420 px from each side, leaving 1080×1080.
2. **Image Mask/Blend** — Type: **Alpha Mask (Alpha Channel)**, Path:
   `obs/bubble_mask.png`

Order matters. Masking before cropping gives you an oval.

### The rim and shadow

OBS has no border filter, so the rim is a separate image on top. Add source →
**Image** → `obs/bubble_ring_blue.png` (or `bubble_ring_orange.png`), and place
it above the webcam in the source list.

Both `bubble_mask.png` and `bubble_ring_*.png` are generated by
`obs/make_bubble_assets.py` and are aligned to each other, so give them the
**identical transform**.

### Exact placement

Select each source and press **Cmd+E** (Edit Transform) to type numbers rather
than dragging:

| | Position | Size |
|---|---|---|
| Bottom-right (default) | 1550, 710 | 330 × 330 |
| Top-right (for the scenes in section 9) | 1550, 40 | 330 × 330 |

That is a 330 px bubble with a 40 px margin. The ring PNG's shadow extends
slightly past the circle, which is intentional — it stops the bubble looking
pasted onto the white canvas.

Select the webcam and the ring together → right-click → **Group**, and name it
`Bubble`. Then copy it into your other scenes with **Copy** → **Paste
Reference** (not Paste Duplicate), so changing the bubble once changes it
everywhere.

## 8. Hotkeys

Settings → Hotkeys. Set at minimum:

- Start Recording / Stop Recording
- **Pause Recording** — the most useful one. Pause between scenes instead of
  stopping, and you get one continuous file with the dead air already removed.
- Switch to `01 Canvas + bubble`
- Switch to `02 Face full`

Pick combinations no app uses, e.g. `F13`–`F16`, or `Ctrl+Opt+1/2`. These only
fire while another app is focused if Accessibility is granted (section 5).

### A correction worth knowing

OBS records multiple **audio** tracks natively, but a separate **video** track
for the webcam requires the third-party *Source Record* plugin. For your first
videos, don't install it — switch scenes live with a hotkey instead. It is one
less thing to go wrong, and the edit is simpler.

## 9. Bottom-right clearance

The generator keeps most scenes clear in the bottom-right, but check these
before recording — they have content close to that corner:

- Episode 1, scene 08 (`The count matrix`) — the violet panel extends to
  x≈1510, y≈850.
- Episode 1, scene 21 (`Add-k smoothing`) — the violet "nothing is free" panel
  sits at the bottom right.
- Episode 1, scene 23 (`Two different problems`) — the parenthetical note is
  bottom-right.

For those three, move the bubble to the **top-right** for the duration, or plan
to speak them from full-frame face.

## 10. Audio

- In the OBS mixer, aim for peaks between **−12 and −6 dB**. Yellow is fine, red
  is clipping and unfixable in the edit.
- Add a **Noise Suppression** filter (RNNoise) and a **Limiter** at −3 dB to the
  mic source. Skip a noise gate on a first setup; it clips the starts of words
  more often than it helps.
- Record a room-tone reference before starting; it makes noise removal
  predictable.
- Speak the numbers out loud. "Zero point two five" reads far better than
  silence over a table.
- One take per scene, not one take per video. 27 short takes are recoverable; a
  30-minute take is not.

## 11. Before you hit record

A five-minute check that saves a re-record:

- [ ] Do Not Disturb on. Slack and mail quit, not just minimised.
- [ ] Browser: bookmarks bar hidden, other tabs closed, Excalidraw in zen mode.
- [ ] Canvas file open, and it's the `.RECORDING.` copy (section 3).
- [ ] Disk space: budget roughly **1.5 GB per 10 minutes** at these settings.
- [ ] Record 30 seconds — talk, annotate, switch scenes once.
- [ ] **Watch that 30 seconds back on your phone.** This is the step people skip.
      Check: canvas text legible at phone size, audio peaks in range, bubble not
      covering anything, cursor visible, no notification banner.

If the canvas text is too small on the phone, the fix is to zoom the frame
slightly rather than to change font sizes — the scenes are built at a size that
works when a frame fills the viewport.

## 12. Editing rhythm

The canvas gives you natural cut points: one scene, one cut. Use them.

- Hard-cut between scenes; no transitions, no zoom whooshes.
- If a scene takes more than ~90 seconds, split it in the edit with a brief
  face cutaway. The theory videos are dense; the face is the punctuation.
- Keep the failure moments. Scene 11 (greedy loops), scene 13 (bad samples),
  scene 25 (nonsense output) are the most watchable parts of episode 1 — do not
  tidy them into a summary.
