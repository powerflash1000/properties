# CLAUDE.md — عقارات

Working memory for Claude sessions. Talk to the user in Egyptian Arabic, short and practical.

## What this is
Private repo for the family's properties (apartment now; villa and chalet later). Each property = one folder under `apartments/<id>/` with a single `model.json`. The 3D viewer (`viewer/index.html`, three.js r128 from cdnjs, no build step) reads it. **Keep the repo private** (plans of owned property).

## Conventions
- Units: meters. x = east on the plan image, z = south (down). y = up. Rotation `ry` in radians; the furniture "front" is local +z (the yellow arrow shows it).
- `model.json`: `params` (ceiling, door height/width, balcony door width, window sill), `rooms` (interior rects, kinds `liv din kit wet bed dr cor foy ter land`), `walls` (center line `p`, run `a..b`, thickness `t`, openings `op` with centre `c` along the wall; types `win slide door front arch`), `furniture` (id, Arabic `name`, `type`, `x`, `z`, `ry`, `args`, optional `when` {layout, v, kitOpen} and `curtain`).
- Furniture types are built in the viewer's `BUILD` registry (sofa, bed, wardrobe, …). To move something the user names, edit its `x/z/ry` in `model.json` (find it by Arabic name/id). To add a type, add a builder to `BUILD`.
- Layout variants: items with `when.layout` show only when that layout is selected (`liv`, `din`, `kit`, `b1`, `b2`).
- Test every change with Playwright (swiftshader WebGL works; route cdnjs three to a local copy from `npm pack three@0.128.0`).
- Publish the viewer as an artifact with `python3 tools/build_single.py apt1 out.html` then the Artifact tool (the old artifact URL for the apartment is https://claude.ai/artifact/C5eZfG8Ci5wqokLVbiGcU3 — republish the same file path to keep it).
- Commit with `git -c user.name="Claude" -c user.email="noreply@anthropic.com"`.

## Editing in the viewer
- Tabs: «العفش» (move/rotate/duplicate/delete/add furniture) and «الحيطان والفتحات» (tap a wall/window/door → demolish, move a wall segment (resizes the two rooms beside it), remove/resize/move an opening, add window/door/balcony door/arch). Edits live in `localStorage` and in the share link (`#e=…`): `edits.mod/del/add` for furniture, `edits.w` for wall ops (`rm`, `mv`, `rmop`, `addop`, `modop`).
- `model.json` walls are pre-split at junctions (ids like `V7d`) so one segment can be moved alone. Moving a wall shifts the rooms' edges and the ends of perpendicular walls that meet it; junction jogs may need a manual fix in `model.json`.
- To make a user's edits permanent, apply them to `model.json` (furniture `x/z/ry`, wall `p`, `op`, room rects) and push.

- Wall panel also has «حط عفش على الحيطة دي»: picks a side (room) and a type (TV unit, bookcase, wardrobe, sofa, console, mirror, desk, bed); the item is snapped back-to-wall at the last tapped point (`snapItemToWall` using the item's bounding box) and then selected for moving. Furniture panel has «ألصقه بأقرب حيطة» and «عدّل الزاوية»; items added "in front of me" are rotated to a multiple of 90°.

- Room walls are numbered 1 (top on the plan), 2 (right), 3 (bottom), 4 (left), clockwise. With an item selected, numbers show on its room's walls; «انقلها لجدار» (or tapping a number) moves it back-to-wall facing into the room (`moveToRoomWall(n, center)`); «وسّطها» centers it on the nearest wall.

## Sync (single source of truth = this repo)
- Edits made in the viewer are stored per browser (`localStorage`), so the GitHub Pages page and the Claude artifact do NOT share them. Tab «المزامنة»: «احفظ تعديلاتي في المستودع» bakes furniture + wall/opening edits into `apartments/<id>/model.json` via the GitHub contents API (fine-grained PAT, Contents: read/write on this repo only, stored in `localStorage` as `prop:ghtoken`) and clears the local edits; «حدّث من المستودع» pulls the latest model. The artifact (inlined model, sandboxed network) cannot call GitHub, so the Pages page is the working app and the artifact is a copy that must be republished after each push.
- When the user pastes «انسخ تعديلاتي» output, apply it to `model.json` (furniture `x/z/ry`, deletions, additions, wall ops) and push.

## Controls (walk mode)
- Left stick (default: left/right turn in place, up/down walk; option "strafe"; deadzone + curve, speed + turn-speed sliders), drag to look (sensitivity/invert), «👁 أفقي» levels the view, ⟲/⟳ 90° snap turns, 🔄 auto 360° (separate left/right buttons, speed slider, any touch stops it), double-tap floor = glide there, minimap (bottom-left) shows position/heading and teleports on tap, auto-level pitch while walking. Quality high/mid/low with auto-downgrade when the average frame time is >40 ms.

## Registration against the plan photo (2026-11-24)
- Never trust eyeballed coordinates. `tools/overlay_plan.py PHOTO model.json out.png` draws walls (red), doors (green), windows (blue) on the photo (EXIF-corrected; mapping px=100+61·x, py=35+61·z). Wall lines were also snapped by measuring dark-pixel profiles. After this fit: master/dressing/bath/corridor walls moved ~0.4 m north; corridor is ~1.25 m wide in the drawing (owner guessed 1.5); the dressing is entered from the corridor-end door and is **open to the master** in its north ~1 m (no wall there); the master-suite bath door is on the dressing wall, not on the corridor; foyer ~2.2×2.0 with the front door near its east side.
- Door positions measured from the photo: Bed2 c≈3.37, dressing door c≈4.35 (on x=17.87), bath-C door c≈6.3 (same wall), Bed1 door c≈15.6, kitchen door c≈10.15, front door c≈8.95.

## Apartment 1 — known facts (from the owner)
- Total 202 m² (gross); dimensions on the plan sum to ~140 m² net. Ceiling 2.70 m. Doors ~1.0×2.30 m. Balcony doors ~1.5 m. Reception window 1×1 m, kitchen window ~1.1 m, small bathroom windows.
- Corridor length 10.30 m (3.65+1.6+3.2+1.9); width ~1.25 m measured on the plan (owner guessed 1.5, unconfirmed). Entrance foyer ~2.0×1.9 m.
- Reception balconies face the sea (Alexandria → north). All corners face streets: the apartment holds 3 corners of a 3-apartment building (ours on the right, duplex in the middle). The master looks to the back side.
- Still needed: bedroom window sizes, structural walls/columns, shafts, the real corridor width, the shared landing/stairs, material photos.
- Lighting default is a neutral "studio" light until the sun direction is confirmed.

## Roadmap
Realistic renders: export `model.json` to Blender (Cycles, bpy) for photoreal stills/360° panoramas; apply real material photos as textures; villa and chalet folders.

## Sync v2 + dressing tools (2026-11-24)
- Dock button «💾 احفظ» (always visible; yellow ● = unsaved). Save = fetch remote `model.json`; if its sha differs from our base sha, adopt remote and replay our `edits` on top (merge), then PUT, then write a numbered backup `apartments/<id>/backups/NNNN.json` + `backups/log.json` ({last, items:[{n,t,by,note}]}). Other devices poll every 45 s (120 s without token) and on tab focus (`syncPoll`) and merge the same way. Restore = «اعرض النسخ الاحتياطية» → «ارجع لها» (marks dirty, then save).
- Each device needs its own fine-grained PAT (Contents RW); never hard-code a token in the (public) repo. Author = chip in Sync tab (`prop:who`, علاء/وفاء/other), required before the first save, written to backup log `by` and commit message. The Claude artifact can't sync.
- `edits.r[roomId]` = {n,k,x0,x1,z0,z1} overrides (Rooms tab «الغرف»: rename, kind, edges ±10 cm, bath→dressing). New types `glasswardrobe` (glass doors + LED strips) and `glasspanel`; per-item dimension −/+ (`DIMS`), `fitWall(n)` fills the free span of a room wall between openings.

## Doors + label occlusion (2026-11-24)
- Door opening props (stored on the opening in model.json via `modop` patch): `open` (true/false/null = follow global «doorsOpen»), `style` (flush|panel|glass|groove|slat|double|slide), `col` (brown|oak|walnut|white|cream|grey|black), `hs` (-1 = hinge on the other side), `rev` (swing to the other room). UI: «الحيطان والفتحات» → tap a door → «الباب» section (`doorPanel`, `data-dp="key:value"`; `-` clears a key). Front door supports open/close + hinge side only.
- Floating labels (furniture names, room names, wall numbers) are hidden when a wall is between the camera and the label (`labelHidden`, raycast vs `wallGrp`, refreshed every 6 frames and when a label enters the screen). Wall highlight no longer draws through other walls.
- `__walk.yaw` now has a setter (tests).

## Look pack v1 (2026-11-24)
- Design tab: `ST.stone` (STONES: crema, carrara, calacatta, marquina, grey, emerald, travertine, rosa) drives kitchen counters + backsplash (`F().counter = stoneMat`), dining table top and the «marble» floor option; `ST.tvimg` (sunset/sea/forest/city/off, canvas-drawn picture on `tvUnit` screen, emissive); `ST.chand` (rings/crystal/globes/linear); `ST.lampc` (warm/neutral/cool point-light color).
- New types: `ac` (split unit, args.w/y, default y=2.15, back at the wall face; 5 placed in model.json by script: ac-din, ac-liv, ac-b1, ac-b2, ac-ms) and a better `fridge` (French-door, args.w). Reference image from the owner (top-down warm rendered apartment) = target look; real-time can approach it, exact match needs Blender renders (roadmap phase 3).
- TODO (look): scene is over-exposed/washed out with lamps+sun; marble veins barely visible on floors (tile repeat); add a «ستايل الصورة» preset (warm light, lower exposure), furniture closer to the reference (L sofa, marble dining table with upholstered chairs, headboards), real-photo textures.

## Product catalog (2026-11-24)
- `BRANDS` / `BRAND_STYLE` in viewer: item `args` {brand, kind, inch, mount, hp, col, w, h, y}. Types: `tv` (standalone, wall/stand), `tvUnit` (embeds a TV: args.brand/inch), `fridge` (side/french/top/bottom × steel/black/white), `ac` (wall/floor/cassette, hp 1.5–4, colors), `hood` (chimney/slim/island; separate from `hob`, which is now cooktop only; model has `kit-hood`). UI = «الماركة والنوع» block in the furniture tab (`updateBrand`, `data-bp="key:value"`). Logos are simple canvas wordmarks, bodies are generic shapes styled per brand (not licensed product models). Real branded 3D models → Blender phase.

## Look pack v2 + stick fix (2026-11-24)
- `unstick()` in `step()`: if the camera sits inside a wall's collision margin (e.g. spawn presets after the wall re-registration) it is pushed out; before this, forward/back were blocked while turning still worked.
- «✨ طبّق ستايل الصورة» (design tab, `applyLook`): palette 7 «لوكس بيج دافئ», marble floors (slab 1.6 m), crema marble, warm lamps, studio light with `ST.expo` .66, crystal chandelier. `ST.expo` slider in the light tab. New `sofaL` type. PALS: always append, never insert (saved `ST.pal` indices).

- Kitchen door (fixed 2026-11-24 from the owner's reference render): on the kitchen's EAST wall `V4b` (x=10.66) at c=3.9, w .85, swinging into the kitchen, next to the guest-bath door; the south wall `H6` toward the corridor is solid. `kit-run-e` shortened to len 1.9 (z .4 centre 2.4) to clear the door.

## Stick v3 (2026-11-26)
- Default stick mode is now `strafe` («PlayStation»: push in any direction = move relative to the view; drag the screen to look). Saved `stickMode:'turn'` is migrated once (`ST.stickV=2`). On-screen toggle `#bStick` next to the stick switches 🎮 free / ↺ turn. A yellow floor arrow (`moveArrow`) shows the walking direction while moving.
- Stick v4 (2026-11-26): default mode `auto` (`ST.stickV=3`): stick angle = world heading relative to the yaw at touch start (`stickRef`, kept in sync if the user looks/snap-turns meanwhile); the camera turns toward it (~4 rad/s) and walks forward scaled by how aligned it is; pushing down turns around 180°. Floor arrow points at the target heading. `#bStick` cycles auto → strafe → turn. Tested at 1180×820: up/right/left/down/diagonal and steering inside one touch.

## Photo items (2026-11-26)
- Any furniture item can show a real photo instead of its 3D model: furniture tab → select item → «🖼 صورة حقيقية بدل المجسّم» (upload / paste / direct image URL; white-background removal by corner flood-fill; crop to subject; max 900 px PNG). Stored as `args.img` (+ `pw` width, `py` lift, `bill` always-face-camera). `local:<id>` = on this device only (localStorage `prop:photo:<id>`); on 💾 save `uploadPhotos()` PUTs it to `apartments/<id>/photos/<id>.png` and rewrites `args.img` to `photos/<id>.png` (loaded from `../apartments/<id>/…`; not available in the single-file artifact). The 3D model is built first and swapped when the texture loads (bbox gives the default size). Direct URLs only work for hosts that allow CORS (Pinterest etc. do not — upload/paste instead). AI-generated or pasted images are the owner's call (private use).
- Dining set photos (2026-11-27): `apartments/apt1/photos/din-table.png` (oval white-marble table, fluted brass bases, pw 2.4) and `din-chair.png` (beige boucle chair, pw .58) applied to `din-table` and all `din-chair-*` (layout 0). Generated with Seedream 5 lite (1 credit each) on #00FF00 and chroma-keyed (flood from border, largest component, despill). Photo items show the 3D model in the top/orbit view (elevation ≥ .8) and the photo in walk/low views.

## Undo + photo library (2026-11-27)
- Global undo: every `saveEdits()` pushes the previous `edits` snapshot onto `editHist` (max 80); dock button «↩ تراجع (n)», Ctrl/Cmd+Z, and «↩ إلغاء آخر تعديل» in the furniture tab call `undoEdit()`. History is cleared by `adoptModel` (after save/pull). `edits.mod[id].args` is now merged into the base `args` (so a dimension tweak no longer drops `img`).
- Photo library: `apartments/<id>/photos/index.json` = [{p, n, w}] (seeded with the dining table/chair); the «🖼» panel shows thumbnails (`data-phlib`) to apply a library photo to the selected item; `uploadPhotos()` appends new uploads to the index. Photo items show photos when `mode==='walk'` or orbit elevation < 1.25, else the 3D model.
