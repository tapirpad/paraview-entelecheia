#!/usr/bin/env python3
"""Build the Entelecheia Qt stylesheet (.qss) + icons for ParaView.

Usage:  python3 gen_paraview_qss.py [blue|gold] [output_dir] [font_pt] [icon_theme]
Default: blue, ~/.local/share/paraview-entelecheia
The .qss refers to its icons by absolute path, so build it where it will live.
"""
import os, sys

VARIANT = sys.argv[1] if len(sys.argv) > 1 else "blue"
OUT = os.path.abspath(os.path.expanduser(
    sys.argv[2] if len(sys.argv) > 2 else "~/.local/share/paraview-entelecheia"))
FONT_PT = float(sys.argv[3]) if len(sys.argv) > 3 else 11   # 0 = leave font size alone
ICON_THEME = sys.argv[4] if len(sys.argv) > 4 else ""      # e.g. breeze-dark; "" = Qt default

C = dict(
    BG="#1B1F20", BASE="#161A1B", ALT="#1E2223", BTN="#2A2F31", BTN_HOV="#3A4144",
    BORDER="#363C3E", LINE="#2C3133", ROW_HOV="#2C3437", TB_HOV="#353C3F",
    TAB_HOV="#2A3033", SB="#3A4042", SB_HOV="#5E6669", TIP="#202526", MENU="#1F2324",
    FG="#959393", TEXT="#A6A4A4", FG_HI="#E2E0E0", DIM="#5A5D5D",
    DARK="#000000",   # text and marks drawn on top of the accent color
)
if VARIANT == "blue":
    C.update(ACC="#53A3C6", ACC_HI="#6DB4D3", ACC_DK="#1F3A48", ACC_SEL="#24404E",
             MENU_HOV="#264759", MENU_TXT="#8CC6DE", SEL_TXT="#D6E4EA")
else:
    C.update(ACC="#B59A5A", ACC_HI="#C8AD6B", ACC_DK="#3A3426", ACC_SEL="#4A4130",
             MENU_HOV="#4A4130", MENU_TXT="#D4B977", SEL_TXT="#E0D6BF")

ICONS = os.path.join(OUT, "icons")
os.makedirs(ICONS, exist_ok=True)

def svg(name, body, size=16):
    with open(os.path.join(ICONS, name + ".svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
                f'viewBox="0 0 16 16">{body}</svg>\n')

def stroke(d, col, w=1.6):
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')

CHEV = {"down": "M4,6 L8,10 L12,6", "up": "M4,10 L8,6 L12,10",
        "left": "M10,4 L6,8 L10,12", "right": "M6,4 L10,8 L6,12"}
for d, p in CHEV.items():
    svg(f"arrow-{d}", stroke(p, C["FG"]))
    svg(f"arrow-{d}-hover", stroke(p, C["ACC_HI"]))
    svg(f"arrow-{d}-disabled", stroke(p, C["DIM"]))
svg("check", stroke("M3.5,8.3 L6.5,11.3 L12.5,4.8", C["DARK"], 2))
svg("check-disabled", stroke("M3.5,8.3 L6.5,11.3 L12.5,4.8", C["DIM"], 2))
svg("check-menu", stroke("M3.5,8.3 L6.5,11.3 L12.5,4.8", C["ACC"], 1.8))
svg("dash", f'<rect x="3.5" y="7" width="9" height="2" rx="1" fill="{C["DARK"]}"/>')
svg("radio-dot", f'<circle cx="8" cy="8" r="3" fill="{C["DARK"]}"/>')
svg("close", stroke("M4.5,4.5 L11.5,11.5 M11.5,4.5 L4.5,11.5", C["FG"], 1.5))
svg("float", f'<rect x="3.5" y="3.5" width="9" height="9" rx="1.5" fill="none" '
             f'stroke="{C["FG"]}" stroke-width="1.4"/>')
svg("empty", "")

I = lambda n: f'url("{ICONS}/{n}.svg")'

FONT_RULE = f"font-size: {FONT_PT:g}pt;" if FONT_PT > 0 else ""
qss = f"""
/* Entelecheia ({VARIANT}) - Qt stylesheet for ParaView. Run with: -style=fusion */

/* ---------- base ---------- */
QWidget {{
    {FONT_RULE}
    background-color: {C['BG']};
    color: {C['TEXT']};
    selection-background-color: {C['ACC']};
    selection-color: {C['DARK']};
    outline: none;
}}
QWidget:disabled {{ color: {C['DIM']}; }}
QMainWindow::separator {{ background: {C['BG']}; width: 4px; height: 4px; }}
QMainWindow::separator:hover {{ background: {C['ACC_DK']}; }}
QSplitter::handle {{ background: {C['BG']}; }}
QSplitter::handle:hover {{ background: {C['ACC_DK']}; }}
QSplitter::handle:horizontal {{ width: 4px; }}
QSplitter::handle:vertical {{ height: 4px; }}
QLabel {{ background: transparent; }}
QFrame[frameShape="4"], QFrame[frameShape="5"] {{   /* HLine / VLine */
    background: {C['LINE']}; border: none; max-height: 1px;
}}
QFrame[frameShape="5"] {{ max-height: 16777215px; max-width: 1px; }}

/* ---------- tooltips ---------- */
QToolTip {{
    {FONT_RULE}   /* tooltips get their own smaller font from Qt unless set here */
    background-color: {C['TIP']};
    color: {C['TEXT']};
    border: 1px solid {C['BORDER']};
    border-radius: 3px;
    padding: 3px 5px;
}}

/* ---------- push buttons ---------- */
QPushButton {{
    background-color: {C['BTN']};
    color: {C['TEXT']};
    border: 1px solid {C['BORDER']};
    border-radius: 3px;
    padding: 3px 10px;
    min-height: 16px;
}}
QPushButton:hover {{ background-color: {C['BTN_HOV']}; border-color: {C['ACC']}; color: {C['FG_HI']}; }}
QPushButton:pressed {{ background-color: {C['ACC']}; border-color: {C['ACC']}; color: {C['DARK']}; }}
QPushButton:checked {{ background-color: {C['ACC_DK']}; border-color: {C['ACC']}; color: {C['ACC_HI']}; }}
QPushButton:default {{ border-color: {C['ACC']}; }}
QPushButton:disabled {{ background-color: #222628; border-color: {C['LINE']}; color: {C['DIM']}; }}
QPushButton::menu-indicator {{
    image: {I('arrow-down')}; subcontrol-origin: padding; subcontrol-position: right center;
    width: 10px; height: 10px; right: 4px;
}}

/* ---------- tool buttons (flat until hovered) ---------- */
QToolButton {{
    background-color: transparent;
    color: {C['TEXT']};
    border: 1px solid transparent;
    border-radius: 3px;
    padding: 2px;
}}
QToolButton:hover {{ background-color: {C['TB_HOV']}; border-color: #454C4F; }}
QToolButton:pressed {{ background-color: {C['ACC_DK']}; border-color: {C['ACC']}; }}
QToolButton:checked {{ background-color: {C['ACC_DK']}; border-color: {C['ACC_DK']}; color: {C['ACC_HI']}; }}
QToolButton:checked:hover {{ border-color: {C['ACC']}; }}
QToolButton[popupMode="1"] {{ padding-right: 14px; }}
QToolButton::menu-button {{ border: none; width: 12px; }}
QToolButton::menu-arrow, QToolButton::menu-indicator {{ image: {I('arrow-down')}; width: 9px; height: 9px; }}
QToolButton::menu-arrow:hover, QToolButton::menu-indicator:hover {{ image: {I('arrow-down-hover')}; }}

/* ---------- text inputs ---------- */
QLineEdit, QAbstractSpinBox, QTextEdit, QPlainTextEdit {{
    background-color: {C['BASE']};
    color: {C['TEXT']};
    border: 1px solid {C['BORDER']};
    border-radius: 3px;
    padding: 2px 4px;
}}
QLineEdit:hover, QAbstractSpinBox:hover {{ border-color: #4A5052; }}
QLineEdit:focus, QAbstractSpinBox:focus, QTextEdit:focus, QPlainTextEdit:focus {{ border-color: {C['ACC']}; }}
QLineEdit:disabled, QAbstractSpinBox:disabled {{ background-color: {C['BG']}; border-color: {C['LINE']}; color: {C['DIM']}; }}
QLineEdit[readOnly="true"] {{ background-color: {C['BG']}; }}

QAbstractSpinBox {{ padding-right: 16px; }}
QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {{
    background: transparent; border: none; width: 14px;
    subcontrol-origin: border;
}}
QAbstractSpinBox::up-button {{ subcontrol-position: top right; }}
QAbstractSpinBox::down-button {{ subcontrol-position: bottom right; }}
QAbstractSpinBox::up-button:hover, QAbstractSpinBox::down-button:hover {{ background: {C['BTN_HOV']}; border-radius: 2px; }}
QAbstractSpinBox::up-arrow {{ image: {I('arrow-up')}; width: 9px; height: 9px; }}
QAbstractSpinBox::down-arrow {{ image: {I('arrow-down')}; width: 9px; height: 9px; }}
QAbstractSpinBox::up-arrow:hover {{ image: {I('arrow-up-hover')}; }}
QAbstractSpinBox::down-arrow:hover {{ image: {I('arrow-down-hover')}; }}
QAbstractSpinBox::up-arrow:disabled, QAbstractSpinBox::up-arrow:off {{ image: {I('arrow-up-disabled')}; }}
QAbstractSpinBox::down-arrow:disabled, QAbstractSpinBox::down-arrow:off {{ image: {I('arrow-down-disabled')}; }}

/* ---------- combo boxes ---------- */
QComboBox {{
    background-color: {C['BTN']};
    color: {C['TEXT']};
    border: 1px solid {C['BORDER']};
    border-radius: 3px;
    padding: 2px 6px;
    min-height: 16px;
}}
QComboBox:hover {{ background-color: {C['BTN_HOV']}; border-color: {C['ACC']}; }}
QComboBox:on {{ border-color: {C['ACC']}; }}
QComboBox:editable {{ background-color: {C['BASE']}; }}
QComboBox:disabled {{ background-color: #222628; border-color: {C['LINE']}; color: {C['DIM']}; }}
QComboBox::drop-down {{ border: none; width: 18px; subcontrol-origin: padding; subcontrol-position: center right; }}
QComboBox::down-arrow {{ image: {I('arrow-down')}; width: 10px; height: 10px; }}
QComboBox::down-arrow:hover, QComboBox::down-arrow:on {{ image: {I('arrow-down-hover')}; }}
QComboBox::down-arrow:disabled {{ image: {I('arrow-down-disabled')}; }}
QComboBox QAbstractItemView {{
    background-color: {C['MENU']};
    border: 1px solid {C['BORDER']};
    selection-background-color: {C['MENU_HOV']};
    selection-color: {C['MENU_TXT']};
    padding: 2px;
}}

/* ---------- check boxes & radio buttons ---------- */
QCheckBox, QRadioButton {{ background: transparent; spacing: 6px; }}
QCheckBox:hover, QRadioButton:hover {{ color: {C['FG_HI']}; }}
QCheckBox::indicator, QAbstractItemView::indicator, QGroupBox::indicator {{
    width: 13px; height: 13px;
    background-color: {C['BASE']};
    border: 1px solid #5A5D5D;
    border-radius: 3px;
}}
QCheckBox::indicator:hover, QAbstractItemView::indicator:hover, QGroupBox::indicator:hover {{ border-color: {C['ACC']}; }}
QCheckBox::indicator:checked, QAbstractItemView::indicator:checked, QGroupBox::indicator:checked {{
    background-color: {C['ACC']}; border-color: {C['ACC']}; image: {I('check')};
}}
QCheckBox::indicator:checked:hover, QAbstractItemView::indicator:checked:hover {{ background-color: {C['ACC_HI']}; border-color: {C['ACC_HI']}; }}
QCheckBox::indicator:indeterminate, QAbstractItemView::indicator:indeterminate {{
    background-color: {C['ACC']}; border-color: {C['ACC']}; image: {I('dash')};
}}
QCheckBox::indicator:disabled, QAbstractItemView::indicator:disabled {{ background-color: {C['BG']}; border-color: #333839; }}
QCheckBox::indicator:checked:disabled, QAbstractItemView::indicator:checked:disabled {{
    background-color: #333839; border-color: #333839; image: {I('check-disabled')};
}}
QRadioButton::indicator {{
    width: 13px; height: 13px;
    background-color: {C['BASE']};
    border: 1px solid #5A5D5D;
    border-radius: 7px;
}}
QRadioButton::indicator:hover {{ border-color: {C['ACC']}; }}
QRadioButton::indicator:checked {{ background-color: {C['ACC']}; border-color: {C['ACC']}; image: {I('radio-dot')}; }}
QRadioButton::indicator:checked:hover {{ background-color: {C['ACC_HI']}; border-color: {C['ACC_HI']}; }}
QRadioButton::indicator:disabled {{ background-color: {C['BG']}; border-color: #333839; }}

/* ---------- group boxes ---------- */
QGroupBox {{
    background-color: {C['ALT']};
    border: 1px solid {C['LINE']};
    border-radius: 4px;
    margin-top: 14px;
    padding-top: 4px;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 8px; padding: 0 4px; color: {C['FG']}; background: transparent;
}}

/* ---------- item views (pipeline browser, file dialog, spreadsheet) ---------- */
QAbstractItemView {{
    background-color: {C['BASE']};
    alternate-background-color: {C['ALT']};
    color: {C['TEXT']};
    border: 1px solid {C['LINE']};
    border-radius: 2px;
    selection-background-color: {C['ACC']};
    selection-color: {C['DARK']};
}}
QAbstractItemView::item {{ padding: 1px 2px; border: none; }}
QAbstractItemView::item:hover {{ background-color: {C['ROW_HOV']}; color: {C['FG_HI']}; }}
QAbstractItemView::item:selected {{ background-color: {C['ACC']}; color: {C['DARK']}; }}
QAbstractItemView::item:selected:!active {{ background-color: {C['ACC_SEL']}; color: {C['SEL_TXT']}; }}
QTableView {{ gridline-color: {C['LINE']}; }}
QTableView QTableCornerButton::section {{ background-color: {C['ALT']}; border: none; }}

QTreeView::branch {{ background: transparent; }}
QTreeView::branch:hover {{ background-color: {C['ROW_HOV']}; }}
QTreeView::branch:selected {{ background-color: {C['ACC']}; }}
QTreeView::branch:selected:!active {{ background-color: {C['ACC_SEL']}; }}
QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {{ image: {I('arrow-right')}; }}
QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{ image: {I('arrow-down')}; }}
QTreeView::branch:has-children:closed:hover {{ image: {I('arrow-right-hover')}; }}
QTreeView::branch:has-children:open:hover {{ image: {I('arrow-down-hover')}; }}

/* ---------- headers ---------- */
QHeaderView {{ background-color: {C['ALT']}; border: none; }}
QHeaderView::section {{
    background-color: {C['ALT']};
    color: {C['FG']};
    border: none;
    border-right: 1px solid {C['LINE']};
    border-bottom: 1px solid {C['BORDER']};
    padding: 2px 6px;
    font-weight: bold;
}}
QHeaderView::section:hover {{ background-color: {C['TAB_HOV']}; color: {C['FG_HI']}; border-bottom-color: {C['ACC']}; }}
QHeaderView::section:checked {{ color: {C['ACC_HI']}; }}
QHeaderView::up-arrow {{ image: {I('arrow-up')}; width: 9px; height: 9px; subcontrol-position: center right; }}
QHeaderView::down-arrow {{ image: {I('arrow-down')}; width: 9px; height: 9px; subcontrol-position: center right; }}

/* ---------- scrollbars ---------- */
QScrollBar {{ background: {C['BASE']}; border: none; border-radius: 4px; }}
QScrollBar:vertical {{ width: 10px; margin: 0; }}
QScrollBar:horizontal {{ height: 10px; margin: 0; }}
QScrollBar::handle {{ background: {C['SB']}; border-radius: 4px; margin: 1px; }}
QScrollBar::handle:vertical {{ min-height: 30px; }}
QScrollBar::handle:horizontal {{ min-width: 30px; }}
QScrollBar::handle:hover {{ background: {C['SB_HOV']}; }}
QScrollBar::handle:pressed {{ background: {C['ACC']}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; border: none; background: none; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}
QAbstractScrollArea::corner {{ background: {C['BG']}; }}

/* ---------- sliders ---------- */
QSlider {{ background: transparent; }}
QSlider::groove:horizontal {{ height: 4px; background: {C['LINE']}; border-radius: 2px; }}
QSlider::groove:vertical {{ width: 4px; background: {C['LINE']}; border-radius: 2px; }}
QSlider::sub-page:horizontal {{ background: {C['ACC']}; border-radius: 2px; }}
QSlider::add-page:vertical {{ background: {C['ACC']}; border-radius: 2px; }}
QSlider::handle {{ background: {C['TEXT']}; border: none; width: 12px; height: 12px; border-radius: 6px; }}
QSlider::handle:horizontal {{ margin: -4px 0; }}
QSlider::handle:vertical {{ margin: 0 -4px; }}
QSlider::handle:hover {{ background: {C['ACC_HI']}; }}
QSlider::handle:pressed {{ background: {C['ACC']}; }}
QSlider::handle:disabled {{ background: {C['DIM']}; }}
QSlider::sub-page:horizontal:disabled {{ background: {C['DIM']}; }}

/* ---------- progress bars ----------
   No border/chunk rules on purpose: that lets Fusion draw the text in two colors,
   dark over the filled part and light over the empty part (e.g. the memory meter). */
QProgressBar {{
    background-color: {C['BASE']};
    color: {C['FG_HI']};
    selection-background-color: {C['ACC']};
    selection-color: {C['DARK']};
}}

/* ---------- tabs ---------- */
QTabWidget::pane {{ border: 1px solid {C['BORDER']}; border-radius: 3px; top: -1px; background: {C['BG']}; }}
QTabBar {{ background: transparent; qproperty-drawBase: 0; }}
QMainWindow > QTabBar {{ qproperty-drawBase: 0; }}
QTabBar::tab {{
    background-color: {C['BG']};
    color: #6F7070;
    border: 1px solid transparent;
    border-bottom: 1px solid {C['BORDER']};
    padding: 4px 10px;
    margin-right: 1px;
}}
QTabBar::tab:hover {{ background-color: {C['TAB_HOV']}; color: {C['TEXT']}; border-bottom-color: {C['ACC']}; }}
QTabBar::tab:selected {{
    background-color: {C['BTN']};
    color: {C['FG_HI']};
    border: 1px solid {C['BORDER']};
    border-top: 2px solid {C['ACC']};
    border-bottom-color: {C['BTN']};
    border-top-left-radius: 3px; border-top-right-radius: 3px;
}}
QTabBar::close-button {{ image: {I('close')}; subcontrol-position: right; }}
QTabBar::close-button:hover {{ background: {C['BTN_HOV']}; border-radius: 2px; }}
QTabBar::scroller {{ width: 18px; }}
QTabBar QToolButton {{ background: {C['BG']}; }}
QTabBar QToolButton::left-arrow {{ image: {I('arrow-left')}; }}
QTabBar QToolButton::right-arrow {{ image: {I('arrow-right')}; }}

/* ---------- menus ---------- */
QMenuBar {{ background-color: {C['BG']}; color: {C['FG']}; border-bottom: 1px solid {C['LINE']}; }}
QMenuBar::item {{ background: transparent; padding: 3px 8px; border-radius: 3px; }}
QMenuBar::item:selected, QMenuBar::item:pressed {{ background-color: {C['MENU_HOV']}; color: {C['MENU_TXT']}; }}
QMenu {{
    background-color: {C['MENU']};
    color: {C['TEXT']};
    border: 1px solid {C['BORDER']};
    border-radius: 4px;
    padding: 4px;
}}
QMenu::item {{ background: transparent; padding: 4px 20px 4px 8px; border-radius: 3px; }}
QMenu::item:selected {{ background-color: {C['MENU_HOV']}; color: {C['MENU_TXT']}; }}
QMenu::item:disabled {{ color: {C['DIM']}; }}
QMenu::icon {{ padding-left: 6px; }}
QMenu::separator {{ height: 1px; background: {C['BORDER']}; margin: 4px 6px; }}
QMenu::indicator {{ width: 14px; height: 14px; padding-left: 4px; }}
QMenu::indicator:checked {{ image: {I('check-menu')}; }}
QMenu::right-arrow {{ image: {I('arrow-right')}; width: 10px; height: 10px; padding-right: 4px; }}
QMenu::right-arrow:selected {{ image: {I('arrow-right-hover')}; }}

/* ---------- toolbars, docks, status bar ---------- */
QToolBar {{ background-color: {C['BG']}; border: none; spacing: 2px; padding: 2px; }}
QToolBar::separator {{ background: {C['BORDER']}; width: 1px; height: 1px; margin: 4px 3px; }}
QToolBar::handle {{ background: transparent; width: 6px; height: 6px; }}

QDockWidget {{
    color: {C['FG']};
    titlebar-close-icon: {I('close')};
    titlebar-normal-icon: {I('float')};
}}
QDockWidget::title {{
    background-color: {C['ALT']};
    padding: 4px 6px;
    border-bottom: 1px solid {C['LINE']};
    text-align: left;
}}
QDockWidget::close-button, QDockWidget::float-button {{
    background: transparent; border: none; border-radius: 2px; padding: 1px;
}}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {{ background: {C['BTN_HOV']}; }}

QStatusBar {{ background-color: {C['BG']}; color: {C['FG']}; border-top: 1px solid {C['LINE']}; }}
QStatusBar::item {{ border: none; }}
QSizeGrip {{ width: 12px; height: 12px; }}

/* ---------- ParaView: active-view border and widget highlight frames ---------- */
QFrame#CentralWidgetFrame {{ border: none; }}
pqPropertyWidget {{ border: none; }}

/* ---------- ParaView: file dialog size ----------
   The "Files of type" list grows to fit its longest entry (every supported extension),
   which made the dialog wider than the screen. Cap it; the full text still shows in
   its dropdown, cut off at the end. */
QComboBox#EntityType {{ max-width: 28em; }}

/* ---------- scroll areas / properties panel ---------- */
QScrollArea {{ border: none; background: transparent; }}
QScrollArea > QWidget > QWidget {{ background: transparent; }}
"""

# ---------- kdeglobals: makes Qt itself run in dark mode ----------
# The launcher points Qt's built-in "kde" theme at this file (QT_QPA_PLATFORMTHEME=kde).
# Qt then reports a dark color scheme (ParaView uses this for Python shell/output colors)
# and builds its base palette from these colors (this removes Fusion's white lines).
def rgb(h):
    h = h.lstrip("#"); return ",".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))
os.makedirs(os.path.join(OUT, "kde"), exist_ok=True)
with open(os.path.join(OUT, "kde", "kdeglobals"), "w") as f:
    f.write(f"""[General]
ColorScheme=EntelecheiaDark

[KDE]
SingleClick=false
{"" if not ICON_THEME else chr(10) + "[Icons]" + chr(10) + "Theme=" + ICON_THEME + chr(10)}
[Colors:Window]
BackgroundNormal={rgb(C['BG'])}
ForegroundNormal={rgb(C['FG'])}

[Colors:View]
BackgroundNormal={rgb(C['BASE'])}
BackgroundAlternate={rgb(C['ALT'])}
ForegroundNormal={rgb(C['TEXT'])}
ForegroundLink={rgb(C['ACC'])}
ForegroundVisited=180,108,188

[Colors:Button]
BackgroundNormal={rgb(C['BTN'])}
ForegroundNormal={rgb(C['TEXT'])}

[Colors:Selection]
BackgroundNormal={rgb(C['ACC'])}
ForegroundNormal={rgb(C['DARK'])}

[Colors:Tooltip]
BackgroundNormal={rgb(C['TIP'])}
ForegroundNormal={rgb(C['TEXT'])}
""")

with open(os.path.join(OUT, f"entelecheia-{VARIANT}.qss"), "w") as f:
    f.write(qss.lstrip())
print(os.path.join(OUT, f"entelecheia-{VARIANT}.qss"))
