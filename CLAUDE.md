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

## Controls (walk mode)
- Left stick (default: left/right turn in place, up/down walk; option "strafe"; deadzone + curve, speed + turn-speed sliders), drag to look (sensitivity/invert), «👁 أفقي» levels the view, ⟲/⟳ 90° snap turns, 🔄 auto 360° (separate left/right buttons, speed slider, any touch stops it), double-tap floor = glide there, minimap (bottom-left) shows position/heading and teleports on tap, auto-level pitch while walking. Quality high/mid/low with auto-downgrade when the average frame time is >40 ms.

## Apartment 1 — known facts (from the owner)
- Total 202 m² (gross); dimensions on the plan sum to ~140 m² net. Ceiling 2.70 m. Doors ~1.0×2.30 m. Balcony doors ~1.5 m. Reception window 1×1 m, kitchen window ~1.1 m, small bathroom windows.
- Corridor length 10.30 m (3.65+1.6+3.2+1.9), width ~1.5 m (assumed). Entrance foyer ~2.0×1.9 m.
- Reception balconies face the sea (Alexandria → north). All corners face streets: the apartment holds 3 corners of a 3-apartment building (ours on the right, duplex in the middle). The master looks to the back side.
- Still needed: bedroom window sizes, structural walls/columns, shafts, the real corridor width, the shared landing/stairs, material photos.
- Lighting default is a neutral "studio" light until the sun direction is confirmed.

## Roadmap
Realistic renders: export `model.json` to Blender (Cycles, bpy) for photoreal stills/360° panoramas; apply real material photos as textures; villa and chalet folders.
