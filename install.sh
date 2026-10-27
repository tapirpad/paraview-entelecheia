#!/usr/bin/env bash
# Install the Entelecheia stylesheet for ParaView and create a "paraview-themed" launcher.
# Usage: ./install.sh /path/to/ParaView-.../bin/paraview [blue|gold] [font_pt] [icon_theme]
#   font_pt:    UI font size in points (default 11; 0 = keep ParaView's own size)
#   icon_theme: icon theme for file dialogs etc. (default: auto = breeze-dark if installed)
#               list installed themes with:  ls /usr/share/icons ~/.local/share/icons
set -e
PV_BIN="$(realpath "${1:?Usage: ./install.sh /path/to/paraview/bin/paraview [blue|gold] [font_pt]}")"
VARIANT="${2:-blue}"
FONT_PT="${3:-11}"
ICON_THEME="${4:-auto}"
DEST="$HOME/.local/share/paraview-entelecheia"
HERE="$(cd "$(dirname "$0")" && pwd)"
PV_ROOT="$(dirname "$(dirname "$PV_BIN")")"

[ -x "$PV_BIN" ] || { echo "Not an executable: $PV_BIN"; exit 1; }

# Pick an icon theme meant for dark backgrounds
if [ "$ICON_THEME" = "auto" ]; then
    ICON_THEME=""
    for d in "$HOME/.local/share/icons" "$HOME/.icons" /usr/local/share/icons /usr/share/icons; do
        if [ -f "$d/breeze-dark/index.theme" ]; then ICON_THEME="breeze-dark"; break; fi
    done
    [ -n "$ICON_THEME" ] && echo "Icon theme: breeze-dark" \
        || echo "Icon theme: none found automatically (pass one as the 4th argument)"
fi

# 1) stylesheet + icons
python3 "$HERE/gen_paraview_qss.py" "$VARIANT" "$DEST" "$FONT_PT" "$ICON_THEME"

# 2) launcher + menu entry
mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
LAUNCHER="$HOME/.local/bin/paraview-themed"
cat > "$LAUNCHER" << LAUNCH
#!/usr/bin/env bash
# Run Qt in dark mode using the private kdeglobals next to the stylesheet.
# This only affects this ParaView process, not your other apps.
export QT_QPA_PLATFORMTHEME=kde
export KDE_SESSION_VERSION=6
export XDG_CONFIG_DIRS="$DEST/kde:\${XDG_CONFIG_DIRS:-/etc/xdg}"
exec "$PV_BIN" -style=fusion -stylesheet="$DEST/entelecheia-$VARIANT.qss" "\$@"
LAUNCH
chmod +x "$LAUNCHER"
cat > "$HOME/.local/share/applications/paraview-themed.desktop" << DESK
[Desktop Entry]
Type=Application
Name=ParaView (Entelecheia)
Exec=$LAUNCHER %F
Icon=$PV_ROOT/share/icons/hicolor/96x96/apps/paraview.png
Categories=Science;Graphics;
Terminal=false
DESK

# A real ~/.config/kdeglobals (left by KDE apps) takes priority over ours for colors
if grep -qs '^\[Colors:' "${XDG_CONFIG_HOME:-$HOME/.config}/kdeglobals"; then
    echo "Warning: ${XDG_CONFIG_HOME:-$HOME/.config}/kdeglobals defines colors and will override the"
    echo "  dark palette for ParaView. Rename or remove it if ParaView doesn't turn dark."
fi

# 3) Python shell syntax colors (pygments style inside ParaView's bundled Python)
STYLE_FILE="$(find "$PV_ROOT" -path '*/pygments/styles/default.py' 2>/dev/null | head -n1)"
if [ -n "$STYLE_FILE" ]; then
    [ -f "$STYLE_FILE.orig" ] || cp "$STYLE_FILE" "$STYLE_FILE.orig"
    cp "$HERE/pygments_entelecheia.py" "$STYLE_FILE"
    rm -f "$(dirname "$STYLE_FILE")"/__pycache__/default.*.pyc
    echo "Python shell colors installed into: $STYLE_FILE"
    echo "  (to undo: mv '$STYLE_FILE.orig' '$STYLE_FILE')"
else
    SITE="$(find "$PV_ROOT" -type d -name site-packages 2>/dev/null | head -n1)"
    echo "Note: ParaView's Python has no 'pygments', so its shell has no syntax colors."
    [ -n "$SITE" ] && echo "  Add it with:  pip install --target '$SITE' pygments   then rerun this script."
fi

echo
echo "Done. Start ParaView with:  paraview-themed"
