# Entelecheia theme for ParaView

A dark theme for the **official ParaView binary** (the one downloaded from paraview.org),
matching the Entelecheia Kvantum theme and terminal palette.

The binary ships its own copy of Qt, so it ignores system theming tools such as
Kvantum and qt6ct. This package themes it from the outside instead, using three
things ParaView's Qt does read:

- a Qt stylesheet (`.qss`) passed on the command line
- a private `kdeglobals` color file that switches Qt into dark mode
- a replacement color style for the Python syntax highlighter

Nothing is compiled, and nothing outside ParaView is affected.


## Package contents

| File | Purpose |
|---|---|
| `install.sh` | One-step installer: builds the theme, creates the launcher, applies the Python colors. |
| `gen_paraview_qss.py` | Generator for the stylesheet, its icons and the `kdeglobals` file. All theme colors are defined at the top. |
| `pygments_entelecheia.py` | Syntax-highlighting colors for ParaView's Python editors. |
| `README.md` | This file. |


## Requirements

- The ParaView binary from paraview.org, unpacked anywhere.
- `python3` on the system, to run the generator. It uses only the standard library.
- Optional: a dark icon theme such as `breeze-dark` or `Papirus-Dark`, for file-dialog icons.
  On Debian or Ubuntu: `sudo apt install breeze-icon-theme`.


## Quick start

```sh
bash install.sh /path/to/ParaView-<version>/bin/paraview
paraview-themed
```

`paraview-themed` is installed in `~/.local/bin`, so that folder must be on your `PATH`.
The installer also adds **ParaView (Entelecheia)** to your application menu.

Rerun `install.sh` whenever you change a setting below or move ParaView to a new folder.


## Installer arguments

```sh
bash install.sh <paraview_binary> [variant] [font_pt] [icon_theme]
```

| Argument | Default | Meaning |
|---|---|---|
| `paraview_binary` | required | Path to `bin/paraview` inside the downloaded ParaView folder. |
| `variant` | `blue` | Accent color: `blue` (terminal color4, `#53A3C6`) or `gold` (color3, `#B59A5A`). |
| `font_pt` | `11` | UI font size in points. `0` leaves the size to ParaView (Edit → Settings → General). |
| `icon_theme` | `auto` | Icon theme for file dialogs. `auto` uses `breeze-dark` if it is installed. To see what you have: `ls /usr/share/icons ~/.local/share/icons` |

Examples:

```sh
bash install.sh ~/opt/ParaView-6.0.1/bin/paraview                       # blue, 11pt, auto icons
bash install.sh ~/opt/ParaView-6.0.1/bin/paraview gold 11               # gold accent, 12pt
bash install.sh ~/opt/ParaView-6.0.1/bin/paraview blue 12 Tela-dark     # different icon theme
```


## Files created by the installer

| Location | What it is |
|---|---|
| `~/.local/share/paraview-entelecheia/entelecheia-<variant>.qss` | The Qt stylesheet. |
| `~/.local/share/paraview-entelecheia/icons/*.svg` | Check marks, arrows and dock buttons used by the stylesheet. |
| `~/.local/share/paraview-entelecheia/kde/kdeglobals` | Dark palette, dark-mode flag, icon theme and double-click setting for Qt. |
| `~/.local/bin/paraview-themed` | Launcher script that starts ParaView with all of the above. |
| `~/.local/share/applications/paraview-themed.desktop` | Application menu entry that runs the launcher. |
| `<ParaView>/lib/python3.*/site-packages/pygments/styles/default.py` | **Replaced** with `pygments_entelecheia.py`. Only done if ParaView bundles pygments. |
| `<ParaView>/lib/python3.*/site-packages/pygments/styles/default.py.orig` | Backup of the original, made on the first run only. |

Everything in `~/.local/share/paraview-entelecheia/` is generated output. Commit the
package files, not that folder. Your ParaView settings and window layout in
`~/.config/ParaView/` are not touched; see [ParaView's own settings](#paraviews-own-settings).


## How it works

### 1. The launcher

`paraview-themed` is a short script:

```sh
export QT_QPA_PLATFORMTHEME=kde
export KDE_SESSION_VERSION=6
export XDG_CONFIG_DIRS="$HOME/.local/share/paraview-entelecheia/kde:${XDG_CONFIG_DIRS:-/etc/xdg}"
exec /path/to/paraview -style=fusion -stylesheet=$HOME/.local/share/paraview-entelecheia/entelecheia-blue.qss "$@"
```

The variables are set only for this one ParaView process, so other apps are unaffected.

### 2. The stylesheet (`-style=fusion -stylesheet=…`)

Qt accepts a stylesheet on the command line of any Qt app, including the ParaView
binary. A stylesheet is CSS-like rules for Qt widgets. It sets the colors, borders,
rounded corners, padding and hover effects for buttons, inputs, lists, tabs, menus,
scrollbars and so on. `-style=fusion` picks Qt's Fusion style as the base that
the stylesheet draws on top of.

Stylesheets can only use images as files on disk, not embedded images. So the generator
writes small SVG icons (check marks, arrows, dock buttons) into `icons/` and refers to
them by absolute path. That is why the stylesheet is generated at install time rather
than shipped as a fixed file.

### 3. Dark mode via `kdeglobals`

A stylesheet can't change everything. Some colors come from Qt's *palette* and from
whether Qt thinks the system is in dark mode:

- **Fusion's tab-bar line:** Fusion draws a 1-pixel line under the dock tab bars in the
  palette's "Light" color. With Qt's default palette that is white.
- **ParaView's own dark-mode switch:** ParaView asks Qt whether the system is dark and,
  if so, uses bright colors for Python shell output, errors and warnings.
  Otherwise it uses dark green and dark red, which are unreadable on a dark background.

On a desktop that doesn't announce a dark or light preference, such as xmonad, Qt
assumes light. The fix uses a mode built into Qt itself, so no KDE install or background
service is needed:

- `QT_QPA_PLATFORMTHEME=kde` with `KDE_SESSION_VERSION=6` makes Qt read its colors from a
  `kdeglobals` file.
- `XDG_CONFIG_DIRS` points Qt at the private `kdeglobals` in
  `~/.local/share/paraview-entelecheia/kde/`, so your real `~/.config` stays untouched.
- That file defines the full palette (window, view, button, selection, tooltip and link
  colors). Its color-scheme name contains "Dark", which is how Qt decides the system is dark.

The file also sets two things that this mode would otherwise change:

- **Icon theme:** Qt's KDE mode defaults to `breeze`, which is meant for light desktops and
  shows dark icons. The installer sets a dark-background theme such as `breeze-dark` instead.
- **Click behavior:** `SingleClick=false` keeps double-click to open files, instead of KDE's
  old single-click behavior.

### 4. ParaView-specific rules in the stylesheet

| Rule | Why |
|---|---|
| `QFrame#CentralWidgetFrame { border: none; }` | Removes the blue frame ParaView draws around the active render view. |
| `pqPropertyWidget { border: none; }` | Removes the blue frame around property groups whose 3D widget is active, such as a Clip plane. |
| `QComboBox#EntityType { max-width: 28em; }` | The file dialog's "Files of type" list grows to fit every supported extension, which made the dialog wider than the screen. |
| `QTabBar { qproperty-drawBase: 0; }` | Asks Qt not to draw the tab-bar base line. The dark palette is the real fix; this is a backup. |
| `QProgressBar` with no border or chunk rules | Leaves the drawing to Fusion, which uses dark text over the filled part and light text over the empty part, as in the memory meter. |

### 5. Python syntax colors

ParaView colors Python code with the `pygments` library and always asks for its built-in
style named "default", with no setting to choose another. The installer therefore
overwrites `pygments/styles/default.py` inside ParaView's bundled Python with
`pygments_entelecheia.py`, which defines the same style name with the terminal palette:

- **Magenta:** keywords.
- **Blue:** functions, classes and modules.
- **Green:** strings.
- **Yellow:** numbers and `True`/`None`.
- **Cyan:** built-ins.
- **Gray italic:** comments.

This affects the Python Script Editor and script fields such as the Programmable Filter's.
The Python shell console itself does no syntax coloring; its output colors come from the
dark mode described in section 3.

If ParaView doesn't bundle pygments, the installer prints a `pip install --target …`
command to add it. Then rerun the installer.


## Customizing

- **Colors:** edit the `C = dict(...)` block near the top of `gen_paraview_qss.py`.
  The accent colors for each variant are just below it. Rerun `install.sh`.
- **Syntax colors:** edit `pygments_entelecheia.py` and rerun `install.sh`.
- **File dialog width:** change `max-width: 28em` in the "file dialog size" section of
  `gen_paraview_qss.py`.
- **Render view background:** this is drawn by VTK, not Qt, so the theme can't reach it.
  Set it in Edit → Settings → Color Palette. `#1B1F20` matches the window background.


## ParaView's own settings

ParaView stores its settings in `~/.config/ParaView/`:

- **`ParaView<version>.ini`:** toolbar and panel layout, window size, file-dialog size, favorites and recent files.
- **`ParaView-UserSettings.json`:** everything from Edit → Settings.

ParaView writes these when it quits. To keep them in version control, symlink the whole
folder rather than single files, because ParaView replaces the `.ini` file when saving and
would break a file symlink. The `.ini` name includes the version, so rename it after
upgrading ParaView to keep your layout.


## Troubleshooting

| Symptom | Fix |
|---|---|
| ParaView isn't dark, or the white line under the tabs is back | Make sure you started it with `paraview-themed`. A `~/.config/kdeglobals` file containing `[Colors:` sections, often left by KDE apps, overrides the private one. The installer warns about this; rename that file. |
| File dialog icons are dark or hard to see | Install a dark icon theme and rerun the installer, or pass one explicitly as the 4th argument. |
| File dialog opens too large once | ParaView restored the size saved from an earlier run. Resize it once, or delete the `FileDialog` lines in `~/.config/ParaView/ParaView<version>.ini`. |
| No syntax colors in the Python Script Editor | ParaView's Python lacks pygments; follow the `pip install --target …` hint the installer printed. |
| `paraview-themed: command not found` | Add `~/.local/bin` to your `PATH`, or run `~/.local/bin/paraview-themed`. |


## Uninstalling

```sh
rm -rf ~/.local/share/paraview-entelecheia
rm -f  ~/.local/bin/paraview-themed ~/.local/share/applications/paraview-themed.desktop
# restore the original pygments style (path is printed by the installer):
mv <ParaView>/lib/python3.*/site-packages/pygments/styles/default.py.orig \
   <ParaView>/lib/python3.*/site-packages/pygments/styles/default.py
```

Starting `paraview` directly, without the launcher, always gives the stock look.
