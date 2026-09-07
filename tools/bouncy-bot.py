#!/usr/bin/env python3
"""
bouncy-bot — writes BouncySwitch.kt (and MainActivity.kt) for the tutorial.

Every stage matches a beat in TUTORIAL-PLAN.md and compiles on its own,
so you can jump to any point in the video and hit Run.

    python3 tools/bouncy-bot.py list          # show the stages
    python3 tools/bouncy-bot.py write 6       # jump straight to stage 6
    python3 tools/bouncy-bot.py type 7        # TYPE stage 7 into the editor
    python3 tools/bouncy-bot.py reset         # back to the empty template

`type` sends real keystrokes to Android Studio, so it looks like a person
writing the code — caret moving, syntax highlighting catching up line by
line. It needs two things first: see `preflight` below.

Stages:
    3  static switch          4  toggleable (jumps)   5  tween
    6  spring                 7  squash & stretch     8  polished / final
"""

import argparse
import random
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "app/src/main/java/com/eosrmg/apps/materialui3"
SWITCH = PKG / "BouncySwitch.kt"
MAIN = PKG / "MainActivity.kt"

# --------------------------------------------------------------------------
# MainActivity variants
# --------------------------------------------------------------------------

MAIN_TEMPLATE = '''package com.eosrmg.apps.materialui3

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.eosrmg.apps.materialui3.ui.theme.MaterialUI3Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MaterialUI3Theme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Greeting(
                        name = "Android",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MaterialUI3Theme {
        Greeting("Android")
    }
}
'''

# Stage 3: the switch is static, so it takes no state yet.
MAIN_STATIC = '''package com.eosrmg.apps.materialui3

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.eosrmg.apps.materialui3.ui.theme.MaterialUI3Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MaterialUI3Theme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    SwitchDemo(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

@Composable
fun SwitchDemo(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        BouncySwitch(
            modifier = Modifier.graphicsLayer {
                scaleX = 2.5f
                scaleY = 2.5f
            },
        )
    }
}

@Preview(showBackground = true)
@Composable
fun SwitchDemoPreview() {
    MaterialUI3Theme {
        SwitchDemo()
    }
}
'''

# Stage 4 onwards: state is hoisted into the screen.
MAIN_STATEFUL = '''package com.eosrmg.apps.materialui3

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.eosrmg.apps.materialui3.ui.theme.MaterialUI3Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MaterialUI3Theme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    SwitchDemo(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

@Composable
fun SwitchDemo(modifier: Modifier = Modifier) {
    var checked by remember { mutableStateOf(false) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        // Scaled up so the squash & stretch reads clearly on video.
        BouncySwitch(
            checked = checked,
            onCheckedChange = { checked = it },
            modifier = Modifier.graphicsLayer {
                scaleX = 2.5f
                scaleY = 2.5f
            },
        )

        Spacer(Modifier.height(40.dp))

        Text(
            text = if (checked) "On" else "Off",
            style = MaterialTheme.typography.headlineSmall,
        )
    }
}

@Preview(showBackground = true)
@Composable
fun SwitchDemoPreview() {
    MaterialUI3Theme {
        SwitchDemo()
    }
}
'''

# --------------------------------------------------------------------------
# BouncySwitch stages
# --------------------------------------------------------------------------

STAGE_3 = '''package com.eosrmg.apps.materialui3

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp

@Composable
fun BouncySwitch(modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .size(width = 52.dp, height = 32.dp)
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .border(2.dp, MaterialTheme.colorScheme.outline, CircleShape),
    ) {
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                // offset() positions the LEFT edge, so shift back by half the thumb.
                .offset(x = 16.dp - 8.dp)
                .size(16.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.outline),
        )
    }
}
'''

STAGE_4 = '''package com.eosrmg.apps.materialui3

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.unit.dp

@Composable
fun BouncySwitch(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    val thumbCentre = if (checked) 36.dp else 16.dp

    Box(
        modifier = modifier
            .size(width = 52.dp, height = 32.dp)
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .border(2.dp, MaterialTheme.colorScheme.outline, CircleShape)
            .toggleable(
                value = checked,
                onValueChange = onCheckedChange,
                role = Role.Switch,
                indication = null,
                interactionSource = null,
            ),
    ) {
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                // offset() positions the LEFT edge, so shift back by half the thumb.
                .offset(x = thumbCentre - 8.dp)
                .size(16.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.outline),
        )
    }
}
'''

STAGE_5 = '''package com.eosrmg.apps.materialui3

import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.unit.dp

@Composable
fun BouncySwitch(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    val thumbCentre by animateDpAsState(
        targetValue = if (checked) 36.dp else 16.dp,
        animationSpec = tween(durationMillis = 300),
        label = "thumbCentre",
    )

    Box(
        modifier = modifier
            .size(width = 52.dp, height = 32.dp)
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .border(2.dp, MaterialTheme.colorScheme.outline, CircleShape)
            .toggleable(
                value = checked,
                onValueChange = onCheckedChange,
                role = Role.Switch,
                indication = null,
                interactionSource = null,
            ),
    ) {
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                .offset(x = thumbCentre - 8.dp)
                .size(16.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.outline),
        )
    }
}
'''

STAGE_6 = '''package com.eosrmg.apps.materialui3

import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.unit.dp

@Composable
fun BouncySwitch(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    val thumbCentre by animateDpAsState(
        targetValue = if (checked) 36.dp else 16.dp,
        animationSpec = spring(
            dampingRatio = 0.45f,
            stiffness = 500f,
        ),
        label = "thumbCentre",
    )

    Box(
        modifier = modifier
            .size(width = 52.dp, height = 32.dp)
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .border(2.dp, MaterialTheme.colorScheme.outline, CircleShape)
            .toggleable(
                value = checked,
                onValueChange = onCheckedChange,
                role = Role.Switch,
                indication = null,
                interactionSource = null,
            ),
    ) {
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                .offset(x = thumbCentre - 8.dp)
                .size(16.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.outline),
        )
    }
}
'''

STAGE_7 = '''package com.eosrmg.apps.materialui3

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.unit.dp
import kotlin.math.abs

@Composable
fun BouncySwitch(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    // Animatable gives us .velocity — animateDpAsState does not.
    val thumbCentre = remember { Animatable(if (checked) 36f else 16f) }

    LaunchedEffect(checked) {
        thumbCentre.animateTo(
            targetValue = if (checked) 36f else 16f,
            animationSpec = spring(
                dampingRatio = 0.45f,
                stiffness = 500f,
            ),
        )
    }

    // The whole effect: faster movement = wider and flatter.
    val stretch = (abs(thumbCentre.velocity) / 400f).coerceIn(0f, 0.35f)

    Box(
        modifier = modifier
            .size(width = 52.dp, height = 32.dp)
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .border(2.dp, MaterialTheme.colorScheme.outline, CircleShape)
            .toggleable(
                value = checked,
                onValueChange = onCheckedChange,
                role = Role.Switch,
                indication = null,
                interactionSource = null,
            ),
    ) {
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                .offset(x = thumbCentre.value.dp - 8.dp)
                .size(16.dp)
                .graphicsLayer {
                    scaleX = 1f + stretch
                    scaleY = 1f - stretch * 0.7f
                }
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.outline),
        )
    }
}
'''

STAGE_8 = '''package com.eosrmg.apps.materialui3

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.unit.dp
import kotlin.math.abs

// Material 3 switch measurements, straight from the spec.
private val TrackWidth = 52.dp
private val TrackHeight = 32.dp
private val ThumbSizeOff = 16.dp
private val ThumbSizeOn = 24.dp

// The thumb's CENTRE travels between these two x positions (in dp).
private const val ThumbCentreOff = 16f
private const val ThumbCentreOn = 36f

// How much velocity counts as "full stretch", and how far we let it stretch.
private const val VelocityForFullStretch = 400f
private const val MaxStretch = 0.35f

/**
 * A Material 3 switch that squashes and stretches as it moves.
 *
 * The trick: we drive the thumb with an [Animatable] instead of animateDpAsState,
 * because an Animatable exposes its current [Animatable.velocity]. Fast movement
 * stretches the thumb horizontally; as the spring settles, velocity drops to zero
 * and the thumb rounds back out on its own.
 */
@Composable
fun BouncySwitch(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
    dampingRatio: Float = 0.45f,
    stiffness: Float = 500f,
) {
    // 1 — Position. Animatable holds a raw Float (dp) so we can read velocity off it.
    val thumbCentre = remember {
        Animatable(if (checked) ThumbCentreOn else ThumbCentreOff)
    }

    LaunchedEffect(checked) {
        thumbCentre.animateTo(
            targetValue = if (checked) ThumbCentreOn else ThumbCentreOff,
            animationSpec = spring(dampingRatio = dampingRatio, stiffness = stiffness),
        )
    }

    // 2 — Squash & stretch. This is the whole effect: the faster it moves, the
    //     wider and flatter it gets. No extra animation needed.
    val stretch = (abs(thumbCentre.velocity) / VelocityForFullStretch)
        .coerceIn(0f, MaxStretch)

    // 3 — Everything else can use the simple animate*AsState helpers.
    val thumbSize by animateDpAsState(
        targetValue = if (checked) ThumbSizeOn else ThumbSizeOff,
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "thumbSize",
    )
    val trackColor by animateColorAsState(
        targetValue = if (checked) {
            MaterialTheme.colorScheme.primary
        } else {
            MaterialTheme.colorScheme.surfaceContainerHighest
        },
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "trackColor",
    )
    val borderColor by animateColorAsState(
        targetValue = if (checked) {
            MaterialTheme.colorScheme.primary
        } else {
            MaterialTheme.colorScheme.outline
        },
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "borderColor",
    )
    val thumbColor by animateColorAsState(
        targetValue = if (checked) {
            MaterialTheme.colorScheme.onPrimary
        } else {
            MaterialTheme.colorScheme.outline
        },
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "thumbColor",
    )
    val iconAlpha by animateFloatAsState(
        targetValue = if (checked) 1f else 0f,
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "iconAlpha",
    )

    Box(
        modifier = modifier
            .size(width = TrackWidth, height = TrackHeight)
            .clip(CircleShape)
            .background(trackColor)
            .border(width = 2.dp, color = borderColor, shape = CircleShape)
            .toggleable(
                value = checked,
                onValueChange = onCheckedChange,
                role = Role.Switch,
                indication = null,
                interactionSource = null,
            ),
    ) {
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                // offset() positions the LEFT edge, so shift back by half the thumb.
                .offset(x = thumbCentre.value.dp - thumbSize / 2)
                .size(thumbSize)
                .graphicsLayer {
                    scaleX = 1f + stretch
                    scaleY = 1f - stretch * 0.7f
                }
                .clip(CircleShape)
                .background(thumbColor),
            contentAlignment = Alignment.Center,
        ) {
            CheckMark(
                color = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier
                    .size(thumbSize - 8.dp)
                    .graphicsLayer { alpha = iconAlpha },
            )
        }
    }
}

/** A checkmark drawn by hand, so we don't need the material-icons dependency. */
@Composable
private fun CheckMark(color: Color, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        val path = Path().apply {
            moveTo(size.width * 0.20f, size.height * 0.52f)
            lineTo(size.width * 0.42f, size.height * 0.74f)
            lineTo(size.width * 0.80f, size.height * 0.28f)
        }
        drawPath(
            path = path,
            color = color,
            style = Stroke(
                width = size.width * 0.16f,
                cap = StrokeCap.Round,
                join = StrokeJoin.Round,
            ),
        )
    }
}
'''

STAGES = {
    3: ("Static switch",       "track + thumb, no state, doesn't move",       STAGE_3, MAIN_STATIC),
    4: ("Toggleable",          "it works, and it JUMPS — the ugly moment",    STAGE_4, MAIN_STATEFUL),
    5: ("Tween",               "smooth but lifeless",                         STAGE_5, MAIN_STATEFUL),
    6: ("Spring",              "it bounces — the core lesson",                STAGE_6, MAIN_STATEFUL),
    7: ("Squash & stretch",    "Animatable + velocity — the money shot",      STAGE_7, MAIN_STATEFUL),
    8: ("Polished / final",    "colors, thumb growth, checkmark, constants",   STAGE_8, MAIN_STATEFUL),
}

# --------------------------------------------------------------------------

BOLD, DIM, GREEN, CYAN, RESET = "\033[1m", "\033[2m", "\033[32m", "\033[36m", "\033[0m"


def cmd_list() -> None:
    print(f"\n{BOLD}bouncy-bot stages{RESET}  {DIM}(beats in TUTORIAL-PLAN.md){RESET}\n")
    for n, (title, blurb, code, _) in STAGES.items():
        lines = len(code.splitlines())
        print(f"  {CYAN}{n}{RESET}  {BOLD}{title:<20}{RESET} {DIM}{blurb}{RESET}")
        print(f"     {DIM}{lines} lines{RESET}")
    print(f"\n  {CYAN}reset{RESET}  {DIM}back to the empty Android Studio template{RESET}\n")


def write_stage(n: int) -> None:
    title, _, code, main = STAGES[n]
    SWITCH.write_text(code)
    MAIN.write_text(main)
    print(f"{GREEN}✓{RESET} stage {n} — {BOLD}{title}{RESET}")
    print(f"  {DIM}{SWITCH.relative_to(ROOT)}  ({len(code.splitlines())} lines){RESET}")
    print(f"  {DIM}{MAIN.relative_to(ROOT)}{RESET}")


# --------------------------------------------------------------------------
# Keystroke typing — the real thing
# --------------------------------------------------------------------------

APP_DEFAULT = "Android Studio"

# AppleScript `keystroke` is ASCII-only in practice, so fold the few smart
# characters that live in the comments.
_FOLD = {"—": "-", "–": "-", "’": "'", "‘": "'", "“": '"', "”": '"', "×": "x"}

RETURN = "key code 36"
ESCAPE = "key code 53"

PREFLIGHT = f"""{BOLD}Before you run `type`, once per machine:{RESET}

  {CYAN}1. Let your terminal control the computer{RESET}
     System Settings -> Privacy & Security -> Accessibility
     Add + enable your terminal app (Terminal, iTerm, or Android Studio).

  {CYAN}2. Turn off the IDE's auto-typing helpers{RESET}
     They fight the bot and corrupt the code.
     Settings -> Editor -> General -> Smart Keys
        [ ] Insert pair brackets
        [ ] Insert pair quotes
        [ ] Insert closing brace
     Settings -> Editor -> General -> Code Completion
        [ ] Show suggestions as you type

  {CYAN}3. Open BouncySwitch.kt and click into it{RESET}
     The bot types wherever the caret is. Empty file, caret at line 1.

{DIM}Turn the Smart Keys options back on when you're done recording.{RESET}
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


def _type_line(line: str, cps: float, jitter: bool) -> None:
    """Type one line, minus its leading whitespace — the IDE does the
    indenting, same as it would for a person typing."""
    stripped = line.lstrip(" ")

    frags = []
    for ch in stripped:
        delay = 1.0 / cps
        if jitter:
            delay *= random.uniform(0.55, 1.8)
            if ch in " .(){},":       # tiny hesitation at punctuation
                delay *= 1.4
        frags.append(f'keystroke "{_esc(ch)}"')
        frags.append(f"delay {delay:.3f}")
    if frags:
        _send(*frags)


def type_stage(n: int, cps: float, app: str, jitter: bool, countdown: int) -> None:
    """Send real keystrokes to the IDE so it looks like a person writing."""
    title, _, code, main = STAGES[n]
    MAIN.write_text(main)      # the screen file is set up instantly
    SWITCH.write_text("")      # empty file for you to open

    print(PREFLIGHT)
    print(f"{BOLD}stage {n} — {title}{RESET}  {DIM}({cps:.0f} chars/sec, ctrl-C to bail){RESET}\n")
    input(f"  Open {CYAN}BouncySwitch.kt{RESET}, then press Enter here... ")

    for i in range(countdown, 0, -1):
        print(f"  {DIM}focusing {app} in {i}...{RESET}", end="\r", flush=True)
        time.sleep(1)
    print(" " * 40, end="\r")

    try:
        subprocess.run(["osascript", "-e", f'tell application "{app}" to activate'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        time.sleep(0.6)

        lines = _ascii(code).split("\n")
        for i, line in enumerate(lines):
            _type_line(line, cps, jitter)
            if i < len(lines) - 1:
                # Escape first — an open completion popup eats the Return and
                # the whole file ends up on one line.
                _send(ESCAPE, "delay 0.04", RETURN, "delay 0.14")
                if not line.strip():
                    time.sleep(0.25)      # breathe at blank lines
    except KeyboardInterrupt:
        print(f"\n{DIM}stopped. `write {n}` drops in the finished file.{RESET}")
        return
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode().strip() if e.stderr else ""
        print(f"\nerror: osascript failed — {err}", file=sys.stderr)
        print(f"{DIM}Usually means step 1 of preflight isn't done.{RESET}", file=sys.stderr)
        return

    print(f"{GREEN}✓{RESET} typed stage {n} — {BOLD}{title}{RESET}")


def stream_stage(n: int, cps: float) -> None:
    """Fallback: grow the file on disk and let the IDE reload it.

    No Accessibility permission needed, but it looks like text appearing
    rather than someone typing. Use it if `type` won't cooperate.
    """
    title, _, code, main = STAGES[n]
    MAIN.write_text(main)

    delay = 1.0 / cps
    buf = []
    print(f"{DIM}streaming stage {n} — {title} (ctrl-C to stop){RESET}")
    try:
        for ch in code:
            buf.append(ch)
            SWITCH.write_text("".join(buf))
            time.sleep(delay)
            if ch == "\n":
                time.sleep(delay * 4)
    except KeyboardInterrupt:
        SWITCH.write_text(code)
        print(f"\n{DIM}interrupted — wrote the rest instantly{RESET}")
        return
    print(f"{GREEN}✓{RESET} done — stage {n}, {BOLD}{title}{RESET}")


def cmd_reset() -> None:
    if SWITCH.exists():
        SWITCH.unlink()
    MAIN.write_text(MAIN_TEMPLATE)
    print(f"{GREEN}✓{RESET} reset to the empty template")
    print(f"  {DIM}deleted BouncySwitch.kt, restored MainActivity.kt{RESET}")


def main() -> int:
    p = argparse.ArgumentParser(prog="bouncy-bot", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list", help="show the stages")
    sub.add_parser("preflight", help="what to set up before `type` works")

    w = sub.add_parser("write", help="write a stage instantly")
    w.add_argument("stage", type=int, choices=sorted(STAGES))

    t = sub.add_parser("type", help="type a stage into the editor for real")
    t.add_argument("stage", type=int, choices=sorted(STAGES))
    t.add_argument("--speed", type=float, default=14.0, metavar="CPS",
                   help="characters per second (default 14, about 170 wpm)")
    t.add_argument("--app", default=APP_DEFAULT, help=f"app to focus (default: {APP_DEFAULT})")
    t.add_argument("--steady", action="store_true", help="machine-even rhythm, no human jitter")
    t.add_argument("--countdown", type=int, default=3, metavar="SEC")

    s = sub.add_parser("stream", help="fallback: grow the file on disk instead")
    s.add_argument("stage", type=int, choices=sorted(STAGES))
    s.add_argument("--speed", type=float, default=45.0, metavar="CPS")

    sub.add_parser("reset", help="back to the empty template")

    a = p.parse_args()

    if not PKG.is_dir():
        print(f"error: package dir not found — {PKG}", file=sys.stderr)
        return 1

    if a.cmd == "list" or a.cmd is None:
        cmd_list()
    elif a.cmd == "preflight":
        print(PREFLIGHT)
    elif a.cmd == "write":
        write_stage(a.stage)
    elif a.cmd == "type":
        type_stage(a.stage, a.speed, a.app, not a.steady, a.countdown)
    elif a.cmd == "stream":
        stream_stage(a.stage, a.speed)
    elif a.cmd == "reset":
        cmd_reset()
    return 0


if __name__ == "__main__":
    sys.exit(main())
