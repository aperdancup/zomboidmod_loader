import sys
import os
import re
import shutil

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QScrollArea,
    QCheckBox, QFrame, QProgressBar, QMessageBox,
    QStatusBar, QSizePolicy, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette


# ── Palette ────────────────────────────────────────────────────────────────────
BG       = "#0d0f14"
SURFACE  = "#13161e"
SURFACE2 = "#1a1e2a"
ACCENT   = "#c8372d"
ACCENT2  = "#e8513e"
TEXT     = "#e8e4dc"
TEXT_DIM = "#6b6f7a"
BORDER   = "#252a38"
GREEN    = "#3dba6a"
YELLOW   = "#d4a339"

STYLE = f"""
QMainWindow, QWidget {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'Consolas', 'Courier New', monospace;
}}

/* ── Top bar ── */
#topbar {{
    background-color: {SURFACE};
    border-bottom: 2px solid {ACCENT};
}}
#title_label {{
    font-size: 20px;
    font-weight: bold;
    color: {TEXT};
    letter-spacing: 3px;
}}
#subtitle_label {{
    font-size: 10px;
    color: {ACCENT};
    letter-spacing: 6px;
}}

/* ── Tabs ── */
QTabWidget::pane {{
    border: none;
    background-color: {BG};
}}
QTabBar {{
    background-color: {SURFACE};
}}
QTabBar::tab {{
    background-color: {SURFACE};
    color: {TEXT_DIM};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 28px;
    font-size: 11px;
    letter-spacing: 3px;
    font-family: 'Consolas', monospace;
    font-weight: bold;
}}
QTabBar::tab:selected {{
    color: {TEXT};
    border-bottom: 2px solid {ACCENT};
    background-color: {BG};
}}
QTabBar::tab:hover:!selected {{
    color: {ACCENT2};
    border-bottom: 2px solid {ACCENT2};
}}

/* ── Inputs ── */
QLineEdit {{
    background-color: {SURFACE2};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 7px 10px;
    font-size: 12px;
    font-family: 'Consolas', monospace;
}}
QLineEdit:focus {{
    border: 1px solid {ACCENT};
}}

/* ── Generic button ── */
QPushButton {{
    background-color: {SURFACE2};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 7px 16px;
    font-family: 'Consolas', monospace;
    font-size: 12px;
}}
QPushButton:hover {{
    background-color: {BORDER};
    border-color: {ACCENT};
    color: {ACCENT2};
}}
QPushButton:pressed {{
    background-color: {ACCENT};
    color: white;
}}
QPushButton:disabled {{
    color: {TEXT_DIM};
    border-color: {SURFACE2};
}}

/* ── Named buttons ── */
#btn_extract {{
    background-color: {ACCENT};
    color: white;
    font-weight: bold;
    font-size: 13px;
    letter-spacing: 2px;
    padding: 10px 28px;
    border: none;
    border-radius: 4px;
}}
#btn_extract:hover   {{ background-color: {ACCENT2}; }}
#btn_extract:disabled {{ background-color: #3a2020; color: #6b3030; }}

#btn_selall {{
    background-color: transparent;
    border: 1px solid {GREEN};
    color: {GREEN};
    font-size: 11px;
    padding: 5px 12px;
}}
#btn_selall:hover {{ background-color: {GREEN}; color: {BG}; }}

#btn_desel {{
    background-color: transparent;
    border: 1px solid {TEXT_DIM};
    color: {TEXT_DIM};
    font-size: 11px;
    padding: 5px 12px;
}}
#btn_desel:hover {{ background-color: {BORDER}; color: {TEXT}; }}

#btn_browse {{
    background-color: transparent;
    border: 1px solid {BORDER};
    color: {TEXT_DIM};
    padding: 7px 14px;
    font-size: 11px;
}}
#btn_browse:hover {{ border-color: {ACCENT}; color: {ACCENT}; }}

#btn_scan {{
    background-color: transparent;
    border: 1px solid {GREEN};
    color: {GREEN};
    font-size: 11px;
    padding: 5px 14px;
}}
#btn_scan:hover {{ background-color: {GREEN}; color: {BG}; }}

/* ── Search box ── */
#search_box {{
    background-color: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 12px;
    color: {TEXT};
}}
#search_box:focus {{ border-color: {ACCENT}; }}

/* ── Labels ── */
#section_label {{
    color: {ACCENT};
    font-size: 10px;
    letter-spacing: 4px;
    font-weight: bold;
}}
#count_label  {{ color: {TEXT_DIM}; font-size: 11px; }}
#info_label   {{ color: {TEXT_DIM}; font-size: 11px; font-style: italic; }}
#saved_label  {{ color: {GREEN};    font-size: 11px; }}

/* ── Scroll area ── */
QScrollArea {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    background-color: {SURFACE};
}}
QScrollBar:vertical {{
    background: {SURFACE}; width: 8px; border: none;
}}
QScrollBar::handle:vertical {{
    background: {BORDER}; border-radius: 4px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: {ACCENT}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ── Mod rows ── */
QCheckBox {{
    color: {TEXT}; font-size: 13px; spacing: 10px;
}}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border-radius: 3px;
    border: 1px solid {BORDER};
    background-color: {SURFACE2};
}}
QCheckBox::indicator:checked {{
    background-color: {ACCENT}; border-color: {ACCENT};
}}
QCheckBox::indicator:hover {{ border-color: {ACCENT}; }}

/* ── Toggle switch style checkbox for enabler tab ── */
#enable_check::indicator {{
    width: 16px; height: 16px;
    border-radius: 3px;
    border: 1px solid {BORDER};
    background-color: {SURFACE2};
}}
#enable_check::indicator:checked {{
    background-color: {GREEN}; border-color: {GREEN};
}}
#enable_check::indicator:hover {{ border-color: {GREEN}; }}

/* ── Progress bar ── */
QProgressBar {{
    background-color: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 4px;
    height: 10px;
    color: transparent;
}}
QProgressBar::chunk {{ background-color: {ACCENT}; border-radius: 3px; }}

/* ── Status bar ── */
QStatusBar {{
    background-color: {SURFACE};
    color: {TEXT_DIM};
    border-top: 1px solid {BORDER};
    font-size: 11px;
    font-family: 'Consolas', monospace;
}}

/* ── Divider ── */
#divider {{
    background-color: {BORDER};
    max-height: 1px; min-height: 1px;
}}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  default.txt parser / writer
# ══════════════════════════════════════════════════════════════════════════════
def parse_default_txt(path):
    """Return set of enabled mod names (without leading backslash)."""
    enabled = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        in_mods = False
        for line in content.splitlines():
            stripped = line.strip()
            if stripped == "mods":
                in_mods = True
                continue
            if stripped == "{":
                continue
            if stripped == "}":
                in_mods = False
                continue
            if in_mods:
                m = re.match(r'mod\s*=\s*\\?(.+?),?\s*$', stripped)
                if m:
                    enabled.add(m.group(1).strip())
    except Exception:
        pass
    return enabled


def write_default_txt(path, enabled_mods):
    """Write default.txt preserving VERSION and maps block."""
    # Read existing to preserve maps section
    maps_lines = []
    version_line = "VERSION = 1,"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Extract version
        vm = re.search(r'(VERSION\s*=\s*\S+)', content)
        if vm:
            version_line = vm.group(1)
        # Extract maps block contents
        maps_match = re.search(r'maps\s*\{([^}]*)\}', content, re.DOTALL)
        if maps_match:
            for line in maps_match.group(1).splitlines():
                s = line.strip()
                if s:
                    maps_lines.append(s)
    except Exception:
        pass

    lines = [version_line, "mods", "{"]
    for mod in sorted(enabled_mods):
        lines.append(f"\tmod = \\{mod},")
    lines.append("}")
    lines.append("maps")
    lines.append("{")
    for ml in maps_lines:
        lines.append(f"\t{ml}")
    lines.append("}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ══════════════════════════════════════════════════════════════════════════════
#  Worker Thread  (extraction)
# ══════════════════════════════════════════════════════════════════════════════
class ExtractWorker(QThread):
    progress = pyqtSignal(int, int)
    mod_done = pyqtSignal(str, bool)
    finished = pyqtSignal(int, int)

    def __init__(self, mods, dest):
        super().__init__()
        self.mods = mods
        self.dest = dest

    def run(self):
        ok = fail = 0
        for i, (name, src) in enumerate(self.mods):
            self.progress.emit(i + 1, len(self.mods))
            try:
                dst = os.path.join(self.dest, os.path.basename(src))
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                ok += 1
                self.mod_done.emit(name, True)
            except Exception:
                fail += 1
                self.mod_done.emit(name, False)
        self.finished.emit(ok, fail)


# ══════════════════════════════════════════════════════════════════════════════
#  Mod Row  (Extractor tab)
# ══════════════════════════════════════════════════════════════════════════════
class ModRow(QFrame):
    def __init__(self, mod_name, mod_path, steam_id, parent=None):
        super().__init__(parent)
        self.mod_name = mod_name
        self.mod_path = mod_path
        self.steam_id = steam_id

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        self.checkbox = QCheckBox()
        self.checkbox.setFixedWidth(20)

        name_lbl = QLabel(mod_name)
        name_lbl.setFont(QFont("Consolas", 12))
        name_lbl.setStyleSheet(f"color: {TEXT};")

        id_lbl = QLabel(f"[{steam_id}]")
        id_lbl.setFont(QFont("Consolas", 10))
        id_lbl.setStyleSheet(f"color: {TEXT_DIM};")
        id_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(self.checkbox)
        layout.addWidget(name_lbl, 1)
        layout.addWidget(id_lbl)

    def is_checked(self): return self.checkbox.isChecked()
    def set_checked(self, v): self.checkbox.setChecked(v)
    def matches(self, q): return q.lower() in self.mod_name.lower()


# ══════════════════════════════════════════════════════════════════════════════
#  Enable Row  (Enabler tab)
# ══════════════════════════════════════════════════════════════════════════════
class EnableRow(QFrame):
    toggled = pyqtSignal(str, bool)   # mod_name, enabled

    def __init__(self, mod_name, enabled, parent=None):
        super().__init__(parent)
        self.mod_name = mod_name

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("enable_check")
        self.checkbox.setFixedWidth(20)
        self.checkbox.setChecked(enabled)
        self.checkbox.stateChanged.connect(
            lambda s: self.toggled.emit(self.mod_name, s == Qt.Checked)
        )

        name_lbl = QLabel(mod_name)
        name_lbl.setFont(QFont("Consolas", 12))
        name_lbl.setStyleSheet(f"color: {TEXT};")

        status = QLabel("ENABLED" if enabled else "DISABLED")
        status.setObjectName("_status_lbl")
        status.setFont(QFont("Consolas", 9))
        status.setFixedWidth(64)
        status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        status.setStyleSheet(f"color: {GREEN};" if enabled else f"color: {TEXT_DIM};")
        self._status = status

        self.checkbox.stateChanged.connect(self._update_status)

        layout.addWidget(self.checkbox)
        layout.addWidget(name_lbl, 1)
        layout.addWidget(self._status)

    def _update_status(self, state):
        on = state == Qt.Checked
        self._status.setText("ENABLED" if on else "DISABLED")
        self._status.setStyleSheet(f"color: {GREEN};" if on else f"color: {TEXT_DIM};")

    def is_enabled(self): return self.checkbox.isChecked()
    def set_enabled(self, v):
        self.checkbox.blockSignals(True)
        self.checkbox.setChecked(v)
        self.checkbox.blockSignals(False)
        self._update_status(Qt.Checked if v else Qt.Unchecked)

    def matches(self, q): return q.lower() in self.mod_name.lower()


# ══════════════════════════════════════════════════════════════════════════════
#  Extractor Tab
# ══════════════════════════════════════════════════════════════════════════════
class ExtractorTab(QWidget):
    # Emitted when dst_edit changes so Enabler tab can follow
    dest_changed = pyqtSignal(str)

    def __init__(self, status_bar, parent=None):
        super().__init__(parent)
        self.status_bar = status_bar
        self.mod_rows   = []
        self.worker     = None
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(14)

        root.addWidget(self._make_paths())
        root.addWidget(self._make_divider())
        root.addWidget(self._make_list(), 1)
        root.addWidget(self._make_action_bar())

    # ── sub-sections ────────────────────────────────────────────────────────
    def _make_paths(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        lbl_src = QLabel("WORKSHOP MODS FOLDER"); lbl_src.setObjectName("section_label")
        src_row = QHBoxLayout()
        self.src_edit = QLineEdit()
        self.src_edit.setPlaceholderText(".../steamcmd/steamapps/workshop/content/108600")
        btn_src = QPushButton("BROWSE"); btn_src.setObjectName("btn_browse")
        btn_src.setFixedWidth(80); btn_src.clicked.connect(self._browse_src)
        src_row.addWidget(self.src_edit); src_row.addWidget(btn_src)

        scan_btn = QPushButton("⟳  SCAN MODS"); scan_btn.setObjectName("btn_scan")
        scan_btn.clicked.connect(self._scan)

        lbl_dst = QLabel("DESTINATION FOLDER"); lbl_dst.setObjectName("section_label")
        dst_row = QHBoxLayout()
        self.dst_edit = QLineEdit()
        self.dst_edit.setPlaceholderText("Select target folder for extracted mods...")
        self.dst_edit.textChanged.connect(self.dest_changed)
        btn_dst = QPushButton("BROWSE"); btn_dst.setObjectName("btn_browse")
        btn_dst.setFixedWidth(80); btn_dst.clicked.connect(self._browse_dst)
        dst_row.addWidget(self.dst_edit); dst_row.addWidget(btn_dst)

        lay.addWidget(lbl_src)
        lay.addLayout(src_row)
        lay.addWidget(scan_btn)
        lay.addWidget(lbl_dst)
        lay.addLayout(dst_row)
        return w

    def _make_list(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        hdr = QHBoxLayout()
        lbl = QLabel("AVAILABLE MODS"); lbl.setObjectName("section_label")
        self.count_lbl = QLabel("0 mods  ·  0 selected"); self.count_lbl.setObjectName("count_label")
        self.search = QLineEdit(); self.search.setObjectName("search_box")
        self.search.setPlaceholderText("🔍  Search mods..."); self.search.setFixedWidth(220)
        self.search.textChanged.connect(self._filter)
        btn_all  = QPushButton("SELECT ALL");   btn_all.setObjectName("btn_selall")
        btn_none = QPushButton("DESELECT ALL"); btn_none.setObjectName("btn_desel")
        btn_all.clicked.connect(lambda: self._set_all(True))
        btn_none.clicked.connect(lambda: self._set_all(False))
        hdr.addWidget(lbl); hdr.addWidget(self.count_lbl); hdr.addStretch()
        hdr.addWidget(self.search); hdr.addWidget(btn_all); hdr.addWidget(btn_none)
        lay.addLayout(hdr)

        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.inner = QWidget()
        self.inner_lay = QVBoxLayout(self.inner)
        self.inner_lay.setContentsMargins(0, 0, 0, 0)
        self.inner_lay.setSpacing(0)
        self.inner_lay.addStretch()
        self.scroll.setWidget(self.inner)
        lay.addWidget(self.scroll, 1)
        return w

    def _make_action_bar(self):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 4, 0, 0); lay.setSpacing(12)
        self.progress = QProgressBar(); self.progress.setFixedHeight(10)
        self.progress.setValue(0); self.progress.setVisible(False)
        self.btn_extract = QPushButton("⬇  EXTRACT SELECTED")
        self.btn_extract.setObjectName("btn_extract"); self.btn_extract.setFixedWidth(200)
        self.btn_extract.clicked.connect(self._extract)
        lay.addWidget(self.progress, 1); lay.addWidget(self.btn_extract)
        return w

    def _make_divider(self):
        d = QFrame(); d.setObjectName("divider"); d.setFrameShape(QFrame.HLine)
        return d

    # ── logic ────────────────────────────────────────────────────────────────
    def _browse_src(self):
        p = QFileDialog.getExistingDirectory(self, "Select Workshop Content Folder")
        if p: self.src_edit.setText(p)

    def _browse_dst(self):
        p = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if p: self.dst_edit.setText(p)

    def get_dest(self): return self.dst_edit.text().strip()

    def _scan(self):
        src = self.src_edit.text().strip()
        if not src or not os.path.isdir(src):
            QMessageBox.warning(self, "Invalid Path", "Please select a valid workshop content folder.")
            return
        for r in self.mod_rows: r.setParent(None)
        self.mod_rows.clear()
        n = self.inner_lay.count()
        if n > 0:
            item = self.inner_lay.takeAt(n - 1)
            if item: del item

        found = 0
        for sid in sorted(os.listdir(src)):
            sp = os.path.join(src, sid)
            if not os.path.isdir(sp): continue
            mp = os.path.join(sp, "mods")
            if not os.path.isdir(mp): continue
            for mn in sorted(os.listdir(mp)):
                mpath = os.path.join(mp, mn)
                if not os.path.isdir(mpath): continue
                row = ModRow(mn, mpath, sid)
                row.checkbox.stateChanged.connect(self._update_count)
                self.mod_rows.append(row)
                self.inner_lay.addWidget(row)
                found += 1

        self.inner_lay.addStretch()
        self._update_count()
        self.status_bar.showMessage(f"Scan complete  ·  {found} mod(s) found")
        self.search.clear()

    def _filter(self, q):
        for r in self.mod_rows: r.setVisible(r.matches(q))
        self._update_count()

    def _set_all(self, state):
        for r in self.mod_rows:
            if r.isVisible(): r.set_checked(state)
        self._update_count()

    def _update_count(self):
        total = len(self.mod_rows)
        sel   = sum(1 for r in self.mod_rows if r.is_checked())
        self.count_lbl.setText(f"{total} mods  ·  {sel} selected")

    def _extract(self):
        dst = self.dst_edit.text().strip()
        if not dst or not os.path.isdir(dst):
            QMessageBox.warning(self, "Invalid Destination", "Please select a valid destination folder.")
            return
        selected = [(r.mod_name, r.mod_path) for r in self.mod_rows if r.is_checked()]
        if not selected:
            QMessageBox.information(self, "Nothing Selected", "Check at least one mod to extract.")
            return
        self.btn_extract.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setMaximum(len(selected))
        self.progress.setValue(0)
        self.status_bar.showMessage(f"Extracting {len(selected)} mod(s)…")
        self.worker = ExtractWorker(selected, dst)
        self.worker.progress.connect(lambda c, t: self.progress.setValue(c))
        self.worker.mod_done.connect(self._on_done)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_done(self, name, ok):
        self.status_bar.showMessage(f"{'✔' if ok else '✘'}  {name}")

    def _on_finished(self, ok, fail):
        self.btn_extract.setEnabled(True)
        self.progress.setVisible(False)
        msg = f"Done!  {ok} extracted" + (f",  {fail} failed" if fail else "")
        self.status_bar.showMessage(msg)
        QMessageBox.information(
            self, "Extraction Complete",
            f"✔  {ok} mod(s) extracted successfully." +
            (f"\n✘  {fail} mod(s) failed." if fail else "")
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Enabler Tab
# ══════════════════════════════════════════════════════════════════════════════
class EnablerTab(QWidget):
    def __init__(self, status_bar, parent=None):
        super().__init__(parent)
        self.status_bar  = status_bar
        self.enable_rows = []
        self.default_path = None   # path to default.txt
        self._mods_dir    = None
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(14)

        # ── Path row ────────────────────────────────────────────────────────
        lbl = QLabel("MODS FOLDER  (same as extractor destination)")
        lbl.setObjectName("section_label")
        path_row = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Set destination in Extractor tab, or browse here…")
        self.path_edit.setReadOnly(False)
        btn_browse = QPushButton("BROWSE"); btn_browse.setObjectName("btn_browse")
        btn_browse.setFixedWidth(80); btn_browse.clicked.connect(self._browse)
        btn_load = QPushButton("⟳  LOAD"); btn_load.setObjectName("btn_scan")
        btn_load.clicked.connect(self._load)
        path_row.addWidget(self.path_edit); path_row.addWidget(btn_browse); path_row.addWidget(btn_load)

        root.addWidget(lbl)
        root.addLayout(path_row)
        root.addWidget(self._make_divider())

        # ── List header ─────────────────────────────────────────────────────
        hdr = QHBoxLayout()
        list_lbl = QLabel("INSTALLED MODS"); list_lbl.setObjectName("section_label")
        self.count_lbl = QLabel(""); self.count_lbl.setObjectName("count_label")
        self.search = QLineEdit(); self.search.setObjectName("search_box")
        self.search.setPlaceholderText("🔍  Search mods..."); self.search.setFixedWidth(220)
        self.search.textChanged.connect(self._filter)
        btn_all  = QPushButton("ENABLE ALL");   btn_all.setObjectName("btn_selall")
        btn_none = QPushButton("DISABLE ALL");  btn_none.setObjectName("btn_desel")
        btn_all.clicked.connect(lambda: self._set_all(True))
        btn_none.clicked.connect(lambda: self._set_all(False))
        hdr.addWidget(list_lbl); hdr.addWidget(self.count_lbl); hdr.addStretch()
        hdr.addWidget(self.search); hdr.addWidget(btn_all); hdr.addWidget(btn_none)
        root.addLayout(hdr)

        # ── Scroll list ─────────────────────────────────────────────────────
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.inner = QWidget()
        self.inner_lay = QVBoxLayout(self.inner)
        self.inner_lay.setContentsMargins(0, 0, 0, 0)
        self.inner_lay.setSpacing(0)
        self.inner_lay.addStretch()
        self.scroll.setWidget(self.inner)
        root.addWidget(self.scroll, 1)

        # ── Bottom status row ────────────────────────────────────────────────
        bot = QHBoxLayout()
        self.info_lbl = QLabel("Load a mods folder to manage enabled mods.")
        self.info_lbl.setObjectName("info_label")
        self.saved_lbl = QLabel("")
        self.saved_lbl.setObjectName("saved_label")
        bot.addWidget(self.info_lbl); bot.addStretch(); bot.addWidget(self.saved_lbl)
        root.addLayout(bot)

    def _make_divider(self):
        d = QFrame(); d.setObjectName("divider"); d.setFrameShape(QFrame.HLine)
        return d

    # ── public slot called from main window when extractor dst changes ──────
    def set_mods_dir(self, path):
        if path and path != self.path_edit.text():
            self.path_edit.setText(path)

    # ── logic ────────────────────────────────────────────────────────────────
    def _browse(self):
        p = QFileDialog.getExistingDirectory(self, "Select Mods Folder")
        if p: self.path_edit.setText(p)

    def _load(self):
        mods_dir = self.path_edit.text().strip()
        if not mods_dir or not os.path.isdir(mods_dir):
            QMessageBox.warning(self, "Invalid Path", "Please select a valid mods folder.")
            return

        self._mods_dir = mods_dir
        default_path   = os.path.join(mods_dir, "default.txt")
        self.default_path = default_path

        # Read enabled set from default.txt (may not exist yet)
        enabled = parse_default_txt(default_path) if os.path.exists(default_path) else set()

        # Discover installed mods (subdirs of mods_dir)
        installed = sorted(
            d for d in os.listdir(mods_dir)
            if os.path.isdir(os.path.join(mods_dir, d))
        )

        # Clear existing rows
        for r in self.enable_rows: r.setParent(None)
        self.enable_rows.clear()
        n = self.inner_lay.count()
        if n > 0:
            item = self.inner_lay.takeAt(n - 1)
            if item: del item

        for mn in installed:
            row = EnableRow(mn, mn in enabled)
            row.toggled.connect(self._on_toggle)
            self.enable_rows.append(row)
            self.inner_lay.addWidget(row)

        self.inner_lay.addStretch()
        self._update_count()
        self.search.clear()
        self.saved_lbl.setText("")

        if not os.path.exists(default_path):
            self.info_lbl.setText("⚠  default.txt not found — will be created on first change.")
        else:
            self.info_lbl.setText(f"Loaded  ·  {os.path.basename(default_path)}")

        self.status_bar.showMessage(f"Enabler: {len(installed)} mod(s) loaded from {mods_dir}")

    def _on_toggle(self, mod_name, enabled):
        """Called whenever a single toggle flips — auto-save immediately."""
        self._save()

    def _set_all(self, state):
        # Block individual saves, bulk-set, then save once
        for r in self.enable_rows:
            if r.isVisible():
                r.checkbox.blockSignals(True)
                r.set_enabled(state)
                r.checkbox.blockSignals(False)
        self._save()
        self._update_count()

    def _filter(self, q):
        for r in self.enable_rows: r.setVisible(r.matches(q))
        self._update_count()

    def _update_count(self):
        total   = len(self.enable_rows)
        enabled = sum(1 for r in self.enable_rows if r.is_enabled())
        self.count_lbl.setText(f"{total} mods  ·  {enabled} enabled")

    def _save(self):
        if not self.default_path:
            return
        enabled = {r.mod_name for r in self.enable_rows if r.is_enabled()}
        try:
            write_default_txt(self.default_path, enabled)
            self.saved_lbl.setText("✔  Saved")
            self.status_bar.showMessage(f"default.txt updated  ·  {len(enabled)} mod(s) enabled")
            self._update_count()
        except Exception as e:
            self.saved_lbl.setText("✘  Save failed")
            QMessageBox.critical(self, "Save Error", str(e))


# ══════════════════════════════════════════════════════════════════════════════
#  Main Window
# ══════════════════════════════════════════════════════════════════════════════
class ModManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PZ MOD MANAGER")
        self.setMinimumSize(800, 660)
        self.resize(920, 720)
        self._build_ui()
        self.setStyleSheet(STYLE)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._make_topbar())

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready  ·  Select a tab to begin")

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.extractor_tab = ExtractorTab(self.status_bar)
        self.enabler_tab   = EnablerTab(self.status_bar)

        self.tabs.addTab(self.extractor_tab, "  EXTRACTOR  ")
        self.tabs.addTab(self.enabler_tab,   "  MOD ENABLER  ")

        # Sync destination folder from extractor → enabler
        self.extractor_tab.dest_changed.connect(self.enabler_tab.set_mods_dir)

        root.addWidget(self.tabs, 1)

    def _make_topbar(self):
        bar = QWidget(); bar.setObjectName("topbar"); bar.setFixedHeight(64)
        lay = QHBoxLayout(bar); lay.setContentsMargins(20, 0, 20, 0)
        icon = QLabel("☣"); icon.setFont(QFont("Segoe UI Emoji", 22))
        icon.setStyleSheet(f"color: {ACCENT};")
        col = QVBoxLayout(); col.setSpacing(0)
        t = QLabel("PROJECT ZOMBOID"); t.setObjectName("title_label")
        s = QLabel("MOD MANAGER");     s.setObjectName("subtitle_label")
        col.addWidget(t); col.addWidget(s)
        lay.addWidget(icon); lay.addSpacing(10); lay.addLayout(col); lay.addStretch()
        return bar


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    dark = QPalette()
    dark.setColor(QPalette.Window,          QColor(BG))
    dark.setColor(QPalette.WindowText,      QColor(TEXT))
    dark.setColor(QPalette.Base,            QColor(SURFACE))
    dark.setColor(QPalette.AlternateBase,   QColor(SURFACE2))
    dark.setColor(QPalette.ToolTipBase,     QColor(TEXT))
    dark.setColor(QPalette.ToolTipText,     QColor(BG))
    dark.setColor(QPalette.Text,            QColor(TEXT))
    dark.setColor(QPalette.Button,          QColor(SURFACE2))
    dark.setColor(QPalette.ButtonText,      QColor(TEXT))
    dark.setColor(QPalette.BrightText,      QColor(ACCENT2))
    dark.setColor(QPalette.Highlight,       QColor(ACCENT))
    dark.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(dark)

    win = ModManager()
    win.show()
    sys.exit(app.exec_())
