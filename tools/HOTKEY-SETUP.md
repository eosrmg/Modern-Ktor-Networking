# Make Ctrl+V type instead of paste

Two ways. **Option A needs nothing installed** and only changes Android Studio —
that's the one to use for recording.

Keep `⌘V` as the real paste. Bind `⌃V` to typebot. Then you have both:
`⌘V` when you just want the code in, `⌃V` when the camera is rolling.

---

## Option A — Android Studio only (no install) ← recommended

### 1. Add the external tool

**Settings → Tools → External Tools → `+`**

| Field | Value |
|---|---|
| Name | `Type Clipboard` |
| Group | `typebot` |
| Program | `/usr/bin/python3` |
| Arguments | `$ProjectFileDir$/tools/typebot.py --now` |
| Working directory | `$ProjectFileDir$` |

Then click **Advanced Options** and **uncheck everything**:

- [ ] Synchronize files after execution
- [ ] Open console for tool output
- [ ] Show console when a message is printed to stdout / stderr

That last group matters. If the console opens, the Run panel steals focus
mid-take and the keystrokes land in the wrong place.

### 2. Free up Ctrl+V first

`⌃V` already belongs to **VCS Operations Popup** in Android Studio. Two actions
can't share a shortcut — the built-in wins, and you get the VCS menu instead of
your typing.

**Settings → Keymap** → search `VCS Operations Popup` → right-click →
**Remove `⌃V`**.

### 3. Bind it to Ctrl+V

**Settings → Keymap** → search `Type Clipboard` → right-click →
**Add Keyboard Shortcut** → press `⌃V` → OK → **Apply**.

If a conflict warning still appears, choose **Remove**, never *Leave*.
*Leave* keeps both bindings and the built-in action keeps winning.

> Want to keep the VCS popup? Use **`⌃⌥V`** for Type Clipboard instead —
> it's unassigned on the macOS keymap.

### 4. Grant Accessibility

**System Settings → Privacy & Security → Accessibility** → enable
**Android Studio**. It's Studio launching the script, so Studio is what needs
permission — not your terminal.

Restart Android Studio after granting it.

### 5. Turn off the IDE's auto-typing helpers

**Settings → Editor → General → Smart Keys**

- [ ] Insert pair brackets
- [ ] Insert pair quotes
- [ ] Insert closing brace

**Settings → Editor → General → Code Completion**

- [ ] Show suggestions as you type

**This is not optional.** With these on, the IDE inserts its own `)` and `"`
while the bot types its own, and you end up with `))))`. Turn them back on
when you're done recording.

### 6. Use it

Copy a chunk from `TUTORIAL-PLAN.md` → click where you want it → hit `⌃V` →
narrate while it types.

**Changing the speed:** edit the Arguments field.
`--speed 9` is slower and easier to talk over, `--speed 20` is brisk.

---

## Option B — system-wide (needs Hammerspoon)

Works in every app, not just Studio, and types noticeably more smoothly —
Hammerspoon sends keystrokes natively instead of shelling out to `osascript`
for every character.

```bash
brew install --cask hammerspoon
```

Then:

```bash
mkdir -p ~/.hammerspoon
cp tools/hammerspoon-init.lua ~/.hammerspoon/init.lua
```

Open Hammerspoon, grant it **Accessibility**, click **Reload Config**.

`⌃V` now types the clipboard anywhere. `⌃⌥V` cancels a run in progress.

Speed lives at the top of the file:

```lua
local CPS = 14      -- characters per second
local JITTER = true -- human-ish irregular timing
```

You still need step 4 above — the Smart Keys settings are an Android Studio
thing regardless of what sends the keystrokes.

---

## If it doesn't work

| Symptom | Cause |
|---|---|
| Nothing happens at all | Accessibility not granted to the app that launched it (Studio for A, Hammerspoon for B). Restart the app after granting. |
| `))))` or doubled quotes | Smart Keys still on — step 4 |
| Code drifts further right each line | Auto-indent isn't being cancelled; make sure you're not passing `--no-indent-fix` |
| A completion popup swallows text | Code Completion "Show suggestions as you type" still on |
| Run panel pops open mid-take | Advanced Options in step 1 still checked |
| It pastes normally instead of typing | The keymap binding didn't take — check Settings → Keymap for a conflict on `⌃V` |
| A **VCS Operations** menu appears | `⌃V` is still bound to VCS Operations Popup — step 2 |

Sanity check without the hotkey, straight from the terminal:

```bash
python3 tools/typebot.py --dry-run
```

That prints what it would type and how long it'll take, without sending a
single keystroke.
