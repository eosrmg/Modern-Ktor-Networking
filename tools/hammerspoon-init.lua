-- typebot for Hammerspoon — paste, but typed.
--
--   Ctrl+V   type the clipboard at a human pace
--   Ctrl+Alt+V   cancel a run in progress
--
-- Install:  cp tools/hammerspoon-init.lua ~/.hammerspoon/init.lua
-- Then grant Hammerspoon Accessibility and hit Reload Config.

local CPS = 14          -- characters per second
local JITTER = true     -- irregular, human-ish timing
local NL_DELAY = 0.14   -- pause after Return
local KEEP_INDENT = false -- false: drop leading spaces and let the editor
                          -- indent (safe). true: type indentation verbatim,
                          -- which double-indents in any editor that auto-indents.

-- Smart characters that don't survive a keystroke; fold them to ASCII.
local FOLD = {
  ["\u{2014}"] = "-",  ["\u{2013}"] = "-",
  ["\u{2018}"] = "'",  ["\u{2019}"] = "'",
  ["\u{201C}"] = '"',  ["\u{201D}"] = '"',
  ["\u{00D7}"] = "x",  ["\u{2026}"] = "...",
}

local queue, timer = {}, nil

local function pump()
  local item = table.remove(queue, 1)
  if not item then
    timer = nil
    return
  end
  if item.text then
    hs.eventtap.keyStrokes(item.text)
  else
    hs.eventtap.keyStroke(item.mods or {}, item.key, 0)
  end
  timer = hs.timer.doAfter(item.delay, pump)
end

local function start()
  if not timer then pump() end
end

local function cancel()
  queue = {}
  if timer then
    timer:stop()
    timer = nil
  end
  hs.alert.show("typebot cancelled")
end

local function clean(text)
  for from, to in pairs(FOLD) do
    text = text:gsub(from, to)
  end
  return (text:gsub("\r\n", "\n"):gsub("\r", "\n"):gsub("\t", "    "):gsub("\n+$", ""))
end

local function splitLines(text)
  local lines = {}
  for line in (text .. "\n"):gmatch("([^\n]*)\n") do
    lines[#lines + 1] = line
  end
  return lines
end

local function delayFor(ch)
  local d = 1.0 / CPS
  if JITTER then
    d = d * (0.55 + math.random() * 1.25)
    if ch:match("[%s%.%(%)%{%},]") then d = d * 1.4 end
  end
  return d
end

local function typeClipboard()
  local raw = hs.pasteboard.getContents()
  if not raw or raw:gsub("%s", "") == "" then
    hs.alert.show("clipboard is empty")
    return
  end

  local lines = splitLines(clean(raw))
  queue = {}

  for i, line in ipairs(lines) do
    local stripped = line:gsub("^ +", "")
    local indent = KEEP_INDENT and line:sub(1, #line - #stripped) or ""

    -- Indentation goes in as one burst; nobody taps out sixteen spaces.
    if #indent > 0 then
      queue[#queue + 1] = { text = indent, delay = 0.01 }
    end
    for ch in stripped:gmatch(".") do
      queue[#queue + 1] = { text = ch, delay = delayFor(ch) }
    end

    if i < #lines then
      -- Escape first: if a completion popup is open, Enter accepts the
      -- completion instead of making a newline and the whole snippet lands
      -- on one line. Escape is harmless when there's no popup.
      queue[#queue + 1] = { key = "escape", delay = 0.04 }
      queue[#queue + 1] = { key = "return", delay = NL_DELAY }
      if stripped == "" then
        queue[#queue].delay = 0.2 -- breathe at blank lines
      end
    end
  end

  hs.alert.show(string.format("typing %d lines", #lines), 0.7)
  start()
end

hs.hotkey.bind({ "ctrl" }, "v", typeClipboard)
hs.hotkey.bind({ "ctrl", "alt" }, "v", cancel)

hs.alert.show("typebot loaded - ctrl+V types the clipboard")
