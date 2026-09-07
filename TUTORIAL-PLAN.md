# Bouncy Material 3 Switch — 20 Minute Tutorial

**Recording script + full reference code.**
The project is back to the empty template. Everything you need to rebuild it is in this file.

Verified against: AGP 9.3.1 · Kotlin 2.2.10 · Compose BOM 2026.02.01 · minSdk 24 · `BUILD SUCCESSFUL`

---

## 0. Before you hit record

**Checklist**
- [ ] Emulator running, **Pixel 6 / API 34+**, dark mode OFF (light reads better on video)
- [ ] Android Studio font size **18pt+**, editor zoomed so code fills the frame
- [ ] Close the Project pane and Logcat — screen space is your budget
- [ ] Split view: code on the left, **Preview on the right** (you'll use it constantly)
- [ ] Turn OFF "optimize imports on the fly" so viewers can see you add imports
- [ ] Have this file open on a second screen

**Title options** (pick one, put the keyword first)
1. `Jetpack Compose Animation — Build a Bouncy Switch in 20 Minutes`
2. `Material 3 Switch, But With Squash & Stretch (Jetpack Compose)`
3. `Your Compose Animations Are Boring. Here's the Fix.` ← highest CTR, lowest search

**Thumbnail** — the big switch mid-flight, thumb visibly stretched, plus the word **BOUNCY** and a small `spring()` code snippet in the corner.

**Description opener**
> Material 3's built-in Switch has a hardcoded animation you can't change. In this video we build our own from scratch — 50 lines of Kotlin — and make it squash and stretch using the spring's own velocity. No libraries, no dependencies.

---

## 1. The nine beats

| # | Time | Beat | Ends with |
|---|------|------|-----------|
| 1 | 0:00–0:40 | Hook | Finished switch bouncing full-screen |
| 2 | 0:40–1:30 | Why not `Switch()`? | Empty project |
| 3 | 1:30–4:00 | Static switch | It looks right, doesn't move |
| 4 | 4:00–5:30 | Make it toggle | It **jumps** — ugly |
| 5 | 5:30–8:00 | `tween` | Smooth but lifeless |
| 6 | 8:00–12:00 | **`spring()`** | It bounces ← core lesson |
| 7 | 12:00–16:00 | **Squash & stretch** | The money shot |
| 8 | 16:00–18:30 | Polish | Looks shippable |
| 9 | 18:30–20:00 | Recap | Outro |

---

## Beat 1 — Hook (0:00–0:50)

**Do not open with the channel name.** Lead with the animation, brand second —
viewers decide in ~5 seconds, and "welcome back to" is the most-skipped opening
on YouTube. You still say it, just 20 seconds later, once they're hooked.

You need the **stock Switch on screen** for the comparison. It's been removed
from `MainActivity`, so for this shot only, drop it back in next to yours,
film 15 seconds, then delete it again:

```kotlin
var stock by remember { mutableStateOf(false) }
Switch(checked = stock, onCheckedChange = { stock = it })
```

### 0:00–0:08 — cold open, silent

No voice. Just the big switch. Flip it three times, then a fourth in slow
motion. Let the squash land.

### 0:08–0:22 — the hook

> "That's a Material 3 switch.
> *(cut to the stock one, flip it)*
> And that's Material 3's actual switch. Same size, same colors, same
> checkmark. The difference is about five lines of code — and I'll show you
> exactly which five."

### 0:22–0:35 — now the brand

> "Welcome back to Droid Script. Today we're building this from scratch in
> Jetpack Compose. No libraries, no dependencies, one file, about fifty lines."

### 0:35–0:50 — the promise, then go

> "By the end you'll know why `spring` beats `tween` for anything a user can
> touch, and how to get squash and stretch out of an animation basically for
> free. Let's get into it."

Cut straight to the empty project. No intro animation, no "before we start,
make sure to subscribe" — that goes at the end.

**Say "five lines", not "a few lines".** A specific number is a promise, and
it's roughly honest: `Animatable` + `LaunchedEffect` + the `stretch` line +
two `graphicsLayer` lines.

---

## Beat 2 — Why not just use `Switch()`? (0:40–1:30)

Type the built-in into `MainActivity`:

```kotlin
var checked by remember { mutableStateOf(false) }
Switch(checked = checked, onCheckedChange = { checked = it })
```

Run it. Flip it.

> "Material 3 already ships a Switch. It works, it's accessible, it's fine. But that animation is hardcoded inside the library — there's no parameter for it. If you want it to feel different, you have to own the component. So let's build one."

**Delete it.** Blank slate.

---

## Beat 3 — The static switch (1:30–4:00)

New file: **`BouncySwitch.kt`**

> "Material 3 spec: the track is 52 by 32 dp. The thumb is 16 when it's off, 24 when it's on. And the thumb's centre travels from x=16 to x=36."

```kotlin
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
                .offset(x = 16.dp - 8.dp)   // centre 16, thumb 16 wide → left edge at 8
                .size(16.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.outline),
        )
    }
}
```

**Say this out loud — it trips people up all video:**
> "`offset` positions the *left edge*, not the centre. So to put the centre at 16, I subtract half the thumb width. Remember that, it comes back later."

Add a `@Preview`. It renders. It does nothing.

---

## Beat 4 — Make it toggle (4:00–5:30)

Hoist the state — signature changes:

```kotlin
@Composable
fun BouncySwitch(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    val thumbCentre = if (checked) 36.dp else 16.dp
```

Add to the track modifier chain:

```kotlin
            .toggleable(
                value = checked,
                onValueChange = onCheckedChange,
                role = Role.Switch,
                indication = null,
                interactionSource = null,
            ),
```

And the thumb uses it:

```kotlin
                .offset(x = thumbCentre - 8.dp)
```

`MainActivity`:

```kotlin
var checked by remember { mutableStateOf(false) }
BouncySwitch(checked = checked, onCheckedChange = { checked = it })
```

Run. **Let the ugly jump land.** Flip it 3 times in silence.

> "It works. It's horrible. There's no animation at all — it teleports. Let's fix that."

*(`role = Role.Switch` is the accessibility bit — mention it in one sentence, don't dwell.)*

---

## Beat 5 — First animation: `tween` (5:30–8:00)

One line becomes four:

```kotlin
    val thumbCentre by animateDpAsState(
        targetValue = if (checked) 36.dp else 16.dp,
        animationSpec = tween(durationMillis = 300),
        label = "thumbCentre",
    )
```

Run. It slides.

> "Better. But be honest — that's boring. It moves at a constant, predictable speed and stops dead. Nothing in the real world moves like that. A real object has weight, it overshoots, it settles."

That's your setup for the actual lesson.

---

## Beat 6 — `spring()` (8:00–12:00) ← **CORE LESSON**

Change **one argument**:

```kotlin
        animationSpec = spring(
            dampingRatio = 0.5f,
            stiffness = 400f,
        ),
```

Run. It bounces. Big reaction moment.

Now teach the two numbers **by changing them live on camera**:

| Change to | What they see | What you say |
|---|---|---|
| `dampingRatio = 1f` | No overshoot | "1 is critically damped — it stops exactly on target" |
| `dampingRatio = 0.5f` | Nice bounce | "0.5 is Compose's `DampingRatioMediumBouncy`" |
| `dampingRatio = 0.2f` | Silly wobble | "0.2 is `DampingRatioHighBouncy` — usually too much" |
| `stiffness = 200f` | Slow, floaty | "Low stiffness = a weak spring" |
| `stiffness = 1500f` | Snappy | "1500 is the default, `StiffnessMedium`" |

Land on `dampingRatio = 0.45f, stiffness = 500f`.

**Then the killer demo — spam-click the switch fast.**

> "Watch this. With `tween`, interrupting an animation restarts it from zero — it stutters. A spring doesn't. It keeps whatever velocity it already had and redirects. That's why springs feel right for anything a user can interrupt. And notice — I never specified a duration. Springs don't have one. That's the point."

---

## Beat 7 — Squash & stretch (12:00–16:00) ← **MONEY SHOT**

> "Right now the thumb is a rigid circle. Real objects deform when they move fast. Animators call it squash and stretch — it's one of Disney's twelve principles. And here's the thing: our spring *already knows* how fast it's going. We just can't reach the number."

**The pivot line:**
> "`animateDpAsState` gives you a value. `Animatable` gives you a value **and a velocity**. And velocity is what makes things feel alive."

Replace the `animateDpAsState` block:

```kotlin
    val thumbCentre = remember { Animatable(if (checked) 36f else 16f) }

    LaunchedEffect(checked) {
        thumbCentre.animateTo(
            targetValue = if (checked) 36f else 16f,
            animationSpec = spring(dampingRatio = 0.45f, stiffness = 500f),
        )
    }
```

> "Two things changed. It's a raw `Float` now, not a `Dp` — Animatable works in plain numbers. And I need a `LaunchedEffect` to kick it off when `checked` changes, because Animatable doesn't watch state for me."

Fix the offset (`.dp` on the value):

```kotlin
                .offset(x = thumbCentre.value.dp - 8.dp)
```

Run — confirm nothing broke. **Then the three lines:**

```kotlin
    val stretch = (abs(thumbCentre.velocity) / 400f).coerceIn(0f, 0.35f)
```

```kotlin
                .graphicsLayer {
                    scaleX = 1f + stretch
                    scaleY = 1f - stretch * 0.7f
                }
```

*(goes between `.size()` and `.clip()`)*

Run. **This is the moment. Slow-mo replay.**

> "That's it. The faster it moves, the wider and flatter it gets. And as the spring settles, velocity drops to zero, so it rounds back out on its own. I never animated the stretch — it's a side effect of the motion."

**Three details worth 30 seconds each:**
- `/ 400f` — "how much velocity counts as full stretch. Tune it to taste."
- `.coerceIn(0f, 0.35f)` — "without this, a fast flick makes it a pancake."
- `* 0.7f` on scaleY — "squash *less* than you stretch. Equal amounts look wrong. Animation rule, not a Compose rule."

---

## Beat 8 — Polish (16:00–18:30)

Move fast here, it's all the same pattern.

**Thumb grows when on:**
```kotlin
    val thumbSize by animateDpAsState(
        targetValue = if (checked) 24.dp else 16.dp,
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "thumbSize",
    )
```
→ offset now subtracts half of *that*: `.offset(x = thumbCentre.value.dp - thumbSize / 2)` and `.size(thumbSize)`

**Colors — same shape three times:**
```kotlin
    val trackColor by animateColorAsState(
        targetValue = if (checked) MaterialTheme.colorScheme.primary
                      else MaterialTheme.colorScheme.surfaceContainerHighest,
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "trackColor",
    )
```
Repeat for `borderColor` (primary / outline) and `thumbColor` (onPrimary / outline).

**The checkmark** — paste this, don't type it live:
```kotlin
    val iconAlpha by animateFloatAsState(
        targetValue = if (checked) 1f else 0f,
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "iconAlpha",
    )
```

> "Quick heads-up — `Icons.Default.Check` won't resolve on a fresh Compose project any more. The material-icons artifact isn't pulled in automatically. Rather than add a dependency just for one tick, I'm drawing it with Canvas. Fifteen lines, and it never breaks."

Paste `CheckMark` (full source below).

**Last step — pull the magic numbers into named constants at the top of the file.**
> "Never leave 36 and 16 floating in your layout code."

---

## Beat 9 — Recap (18:30–20:00)

> "Three things to take away.
> **One** — `spring` beats `tween` for anything a user can interrupt. No duration, keeps its velocity.
> **Two** — `Animatable` gives you velocity. `animateDpAsState` doesn't. That's the only reason to reach for it.
> **Three** — `graphicsLayer` scaling is basically free. It doesn't re-layout anything, so you can drive it from a value that changes every frame.
>
> Full code's in the description. Next video I'll take this same spring and build a bouncy bottom nav bar — subscribe if you want that one."

---

## 2. Reference — the finished code

### `BouncySwitch.kt`

```kotlin
package com.eosrmg.apps.materialui3

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
```

### `MainActivity.kt`

```kotlin
package com.eosrmg.apps.materialui3

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
```

---

## 3. Gotchas & likely comments

**`Icons.Default.Check` doesn't resolve.** Confirmed on BOM 2026.02.01 — `material-icons-core` is no longer a transitive dependency of material3. Either add `androidx.compose.material:material-icons-core` yourself, or draw it (what we do). Mention this at Beat 8 or the comments will be full of it.

**"This recomposes every frame."** True. Reading `thumbCentre.value` during composition invalidates the composable each frame while animating. It's unavoidable in this approach — velocity isn't observable on its own — and it's completely fine for one switch. The pro answer, if someone asks: move the offset into a lambda (`Modifier.offset { IntOffset(...) }`) so it only re-layouts instead of recomposing. Good follow-up video.

**"Why `interactionSource = null`?"** It disables the ripple. On a bouncy switch the ripple fights the motion. Set it to `remember { MutableInteractionSource() }` if you want it back.

**"Why not `Modifier.clickable`?"** `toggleable` with `Role.Switch` is what makes TalkBack announce it as a switch and read its on/off state. One sentence, then move on.

**The `offset` / centre confusion.** `offset` sets the left edge. Every time the thumb size changes you must subtract half of the *current* size. Say it at Beat 3, repeat it at Beat 8.

---

## 4. Interactive mockup

`toggle-mockups.html` in the project root — all five design variants with live spring physics and
`dampingRatio` / `stiffness` sliders. Useful for the Beat 6 explanation if you want a cutaway
showing the two parameters visually instead of re-running the emulator each time.
