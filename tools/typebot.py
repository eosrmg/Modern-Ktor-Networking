#!/usr/bin/env python3
"""
typebot — paste, but typed.

Copy a snippet anywhere, put the caret where you want it, and run this.
Instead of appearing all at once, the code types itself in at a believable
human pace — caret moving, highlighting catching up, the lot.

    python3 tools/typebot.py                 # 3s to click into the editor, then types
    python3 tools/typebot.py --now           # no wait (for hotkey use)
    python3 tools/typebot.py --speed 9       # slower, easier to narrate over
    python3 tools/typebot.py --dry-run       # show what it would type + how long

Bind it to a hotkey and it becomes a second paste key — see `--setup`.

Needs, once per machine:
  * Accessibility permission for whatever launches it
    (System Settings -> Privacy & Security -> Accessibility)
  * Android Studio: Settings -> Editor -> General -> Smart Keys
    uncheck "Insert pair brackets" / "Insert pair quotes" / "Insert closing brace",
    and Code Completion -> uncheck "Show suggestions as you type".
    Otherwise the IDE fights the typing and you get )))) everywhere.
"""

import argparse
import random
import subprocess
import sys
import textwrap
import time

BOLD, DIM, GREEN, CYAN, YELLOW, RESET = (
    "\033[1m", "\033[2m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
)

RETURN = "key code 36"
ESCAPE = "key code 53"
REFORMAT = 'keystroke "l" using {command down, option down}'

# AppleScript `keystroke` is ASCII in practice; fold the smart characters
# that sneak in from docs and comments.
_FOLD = {
    "—": "-", "–": "-", "’": "'", "‘": "'", "“": '"', "”": '"',
    "×": "x", "→": "->", "≥": ">=", "≤": "<=", "…": "...", " ": " ",
}

SETUP = f"""{BOLD}Make it a hotkey (this is the good way){RESET}

  1. Open {CYAN}Automator{RESET} -> New Document -> {CYAN}Quick Action{RESET}
  2. Top of the pane: "Workflow receives" -> {CYAN}no input{RESET} in {CYAN}any application{RESET}
  3. Search the left list for "Run Shell Script", drag it in
  4. Paste this as the script:

     {CYAN}/usr/bin/python3 "{__file__}" --now{RESET}

  5. Save it as {CYAN}Type Clipboard{RESET}
  6. System Settings -> Keyboard -> Keyboard Shortcuts -> Services -> General
     Find "Type Clipboard", assign something like {CYAN}Ctrl-Opt-Cmd-V{RESET}
  7. System Settings -> Privacy & Security -> Accessibility
     Enable it for {CYAN}Automator{RESET} (and your terminal, for testing)

{BOLD}Then, while recording:{RESET}
  Copy the next chunk from TUTORIAL-PLAN.md, click into the editor,
  hit the hotkey, and talk over it while it types.
"""


def _ascii(text: str) -> str:
    return "".join(_FOLD.get(c, c if ord(c) < 128 else "?") for c in text)


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _send(*fragments: str) -> None:
    body = "\n".join(fragments)
    subprocess.run(
        ["osascript", "-e", f'tell application "System Events"\n{body}\nend tell'],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )


def clipboard() -> str:
    return subprocess.run(["pbpaste"], capture_output=True, text=True, check=True).stdout


def prepare(text: str, dedent: bool) -> str:
    text = _ascii(text).replace("\t", "    ").replace("\r\n", "\n").replace("\r", "\n")
    if dedent:
        text = textwrap.dedent(text)
    return text.rstrip("\n")     # never add a trailing blank line


def estimate(text: str, cps: float) -> float:
    """Roughly how long the typing will take, in seconds."""
    typed = sum(1 for line in text.split("\n") for _ in line.lstrip(" "))
    return typed / cps + text.count("\n") * 0.08


def type_line(line: str, cps: float, jitter: bool, keep_indent: bool) -> None:
    """Type one line.

    In `auto` mode we drop the leading whitespace and let the editor indent —
    which is what a person actually does, and it can't corrupt anything.
    In `raw` mode the indentation goes in verbatim, as a single burst.
    """
    stripped = line.lstrip(" ")
    indent = line[: len(line) - len(stripped)] if keep_indent else ""

    frags = []
    if indent:
        frags.append(f'keystroke "{indent}"')
    for ch in stripped:
        delay = 1.0 / cps
        if jitter:
            delay *= random.uniform(0.55, 1.8)
            if ch in " .(){},":          # tiny hesitation at punctuation
                delay *= 1.4
        frags.append(f'keystroke "{_esc(ch)}"')
        frags.append(f"delay {delay:.3f}")
    if frags:
        _send(*frags)


def newline(pause: float, escape_first: bool) -> None:
    """Escape, then Return, then a beat for the editor to react.

    The Escape is why this works. If a code-completion popup is open — and in
    Kotlin one is open most of the time — Enter *accepts the completion*
    instead of inserting a newline, and the whole snippet lands on one line.
    Escape dismisses the popup first. It does nothing when there isn't one.

    Nothing clever beyond that on purpose. An earlier version also pressed
    Cmd+Shift+Left to cancel the editor's auto-indent, but on an unindented
    line the caret is already at column 0, so that selection reached back
    across the newline and the next line typed over it.
    """
    frags = []
    if escape_first:
        frags += [ESCAPE, "delay 0.04"]
    frags += [RETURN, f"delay {pause:.3f}"]
    _send(*frags)


def type_text(text: str, cps: float, jitter: bool, keep_indent: bool,
              pause: float, escape_first: bool, reformat: bool) -> None:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        type_line(line, cps, jitter, keep_indent)
        if i < len(lines) - 1:
            newline(pause, escape_first)
            if not line.strip():
                time.sleep(0.2)          # breathe at blank lines

    if reformat:
        time.sleep(0.3)
        _send(REFORMAT)                  # Cmd+Opt+L — IntelliJ "Reformat Code"


def main() -> int:
    p = argparse.ArgumentParser(
        prog="typebot", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--speed", type=float, default=14.0, metavar="CPS",
                   help="characters per second (default 14, a brisk typist)")
    p.add_argument("--wait", type=float, default=3.0, metavar="SEC",
                   help="pause before typing, to click into the editor (default 3)")
    p.add_argument("--now", action="store_true", help="start immediately (for hotkey use)")
    p.add_argument("--steady", action="store_true", help="even machine rhythm, no human jitter")
    p.add_argument("--dedent", action="store_true", help="strip the common leading indent")
    p.add_argument("--indent", choices=("auto", "raw"), default="auto",
                   help="auto: drop leading spaces, let the editor indent (default, safest). "
                        "raw: type the indentation verbatim — only for editors "
                        "that don't auto-indent, or you'll get double indents.")
    p.add_argument("--reformat", action="store_true",
                   help="press Cmd+Opt+L at the end (IntelliJ Reformat Code)")
    p.add_argument("--nl-delay", type=float, default=0.14, metavar="SEC",
                   help="pause after each Return (default 0.14)")
    p.add_argument("--no-esc", action="store_true",
                   help="don't press Escape before each Return. Only for editors "
                        "with no completion popup — in an IDE, Enter gets eaten by "
                        "the popup and the whole snippet lands on one line.")
    p.add_argument("--dry-run", action="store_true", help="show the text and timing, type nothing")
    p.add_argument("--setup", action="store_true", help="how to bind this to a hotkey")
    a = p.parse_args()

    if a.setup:
        print(SETUP)
        return 0

    text = prepare(clipboard(), a.dedent)
    if not text.strip():
        print(f"{YELLOW}clipboard is empty — copy some code first{RESET}", file=sys.stderr)
        return 1

    lines = text.count("\n") + 1
    secs = estimate(text, a.speed)

    if a.dry_run:
        print(f"{DIM}--- would type ---{RESET}")
        print(text)
        print(f"{DIM}--- {lines} lines, {len(text)} chars, ~{secs:.0f}s at {a.speed:.0f} cps ---{RESET}")
        return 0

    print(f"{BOLD}{lines} lines{RESET} {DIM}· ~{secs:.0f}s at {a.speed:.0f} chars/sec · ctrl-C to stop{RESET}")

    if not a.now:
        for i in range(int(a.wait), 0, -1):
            print(f"  {DIM}click into the editor... {i}{RESET}", end="\r", flush=True)
            time.sleep(1)
        print(" " * 40, end="\r")

    try:
        type_text(text, a.speed, not a.steady, a.indent == "raw",
                  a.nl_delay, not a.no_esc, a.reformat)
    except KeyboardInterrupt:
        print(f"\n{DIM}stopped{RESET}")
        return 130
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode().strip() if e.stderr else ""
        print(f"\nerror: osascript failed — {err}", file=sys.stderr)
        print(f"{DIM}Usually means Accessibility permission is missing. "
              f"See --setup step 7.{RESET}", file=sys.stderr)
        return 1

    print(f"{GREEN}done{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
