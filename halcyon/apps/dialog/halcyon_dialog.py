"""Small dialogs for Halcyon's shell scripts.

    halcyon-dialog --yesno TEXT [--title T] [--yes-label L]   exit 0 for yes, 1 for no
    halcyon-dialog --error TEXT [--title T]
    halcyon-dialog --open DIR [--title T]                     prints the program picked
    halcyon-dialog --busy TEXT [--title T]                    stays up until killed
    halcyon-dialog --checklist TEXT [--title T] ID LABEL on|off ...
                                                              prints the IDs ticked, one a line
    halcyon-dialog --autoplay DISC WHAT ICON [--title T]      options on stdin as
                                                              ID<tab>ICON<tab>LABEL<tab>DESCRIPTION;
                                                              prints ID|always or ID|once
"""
import argparse
import os
import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPalette
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout, QLabel,
                               QListWidget, QListWidgetItem, QMessageBox, QProgressBar, QPushButton, QVBoxLayout)

QSS = """
QDialog { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f4fbff, stop:0.12 #cdeeff,
                                      stop:0.13 #e8f6fd, stop:1 #f6fbfe); color: #0c2e4a; }
QLabel, QCheckBox { color: #0c2e4a; }
QLabel#heading { font-size: 15pt; color: #0e78c8; }
QPushButton#option { text-align: left; padding: 8px; border: 1px solid transparent; border-radius: 4px;
                     background: transparent; color: #0c2e4a; }
QPushButton#option:hover { border-color: #84b9ea; background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                                             stop:0 #f4faff, stop:1 #d3e9fc); }
"""


def light_palette():
    """Omarchy's GTK theme setting would otherwise hand a dark palette to these light dialogs."""
    pal = QPalette()
    for role, color in ((QPalette.Window, "#eef6fb"), (QPalette.WindowText, "#0c2e4a"), (QPalette.Base, "#ffffff"),
                        (QPalette.AlternateBase, "#f0f8fd"), (QPalette.Text, "#0c2e4a"), (QPalette.Button, "#e2f2fb"),
                        (QPalette.ButtonText, "#0c2e4a"), (QPalette.Highlight, "#1e9be0"),
                        (QPalette.HighlightedText, "#ffffff")):
        pal.setColor(role, QColor(color))
    return pal


def icon_for(name):
    if name.startswith("file://"):
        return QIcon(name[len("file://"):])
    return QIcon.fromTheme(name, QIcon.fromTheme("media-optical"))


def yesno(args):
    box = QMessageBox(QMessageBox.Question, args.title, args.yesno)
    yes = box.addButton(args.yes_label or "Yes", QMessageBox.YesRole)
    box.addButton("Cancel" if args.yes_label else "No", QMessageBox.NoRole)
    box.setDefaultButton(yes)
    box.exec()
    return 0 if box.clickedButton() is yes else 1


def error(args):
    QMessageBox(QMessageBox.Critical, args.title, args.error).exec()
    return 0


def open_file(args):
    path, _ = QFileDialog.getOpenFileName(None, args.title, args.open, "Programs (*.exe *.EXE *.bat *.BAT)")
    if not path:
        return 1
    print(path)
    return 0


def busy(args):
    d = QDialog()
    d.setWindowTitle(args.title)
    lay = QVBoxLayout(d)
    lay.addWidget(QLabel(args.busy))
    bar = QProgressBar()
    bar.setRange(0, 0)
    lay.addWidget(bar)
    d.setMinimumWidth(380)
    return d.exec() and 0


def checklist(args):
    rows = args.rest
    if len(rows) % 3:
        print("--checklist needs ID LABEL on|off triples", file=sys.stderr)
        return 2
    d = QDialog()
    d.setWindowTitle(args.title)
    d.resize(640, 520)
    lay = QVBoxLayout(d)
    text = QLabel(args.checklist)
    text.setWordWrap(True)
    lay.addWidget(text)
    items = QListWidget()
    for i in range(0, len(rows), 3):
        it = QListWidgetItem(rows[i + 1])
        it.setData(Qt.UserRole, rows[i])
        it.setCheckState(Qt.Checked if rows[i + 2] == "on" else Qt.Unchecked)
        items.addItem(it)
    lay.addWidget(items, 1)
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(d.accept)
    buttons.rejected.connect(d.reject)
    lay.addWidget(buttons)
    if not d.exec():
        return 1
    for i in range(items.count()):
        if items.item(i).checkState() == Qt.Checked:
            print(items.item(i).data(Qt.UserRole))
    return 0


def autoplay(args):
    disc, what, icon = args.rest[:3]
    d = QDialog()
    d.setWindowTitle(args.title)
    d.setMinimumWidth(460)
    lay = QVBoxLayout(d)

    head = QHBoxLayout()
    pic = QLabel()
    pic.setPixmap(icon_for(icon).pixmap(48, 48))
    head.addWidget(pic)
    title = QLabel(disc)
    title.setObjectName("heading")
    title.setWordWrap(True)
    head.addWidget(title, 1)
    lay.addLayout(head)
    lay.addWidget(QLabel("What do you want to do with this disc?"))

    always = QCheckBox(f"Always do this for {what}")
    picked = []
    for line in sys.stdin.read().splitlines():
        fields = (line.split("\t") + ["", "", "", ""])[:4]
        b = QPushButton(icon_for(fields[1]), fields[2] + (f"\n{fields[3]}" if fields[3] else ""))
        b.setObjectName("option")
        b.setIconSize(QSize(32, 32))
        b.clicked.connect(lambda _=False, choice=fields[0]: (picked.append(choice), d.accept()))
        lay.addWidget(b)
    lay.addWidget(always)

    if not d.exec() or not picked:
        return 1
    print(f"{picked[0]}|{'always' if always.isChecked() else 'once'}")
    return 0


def main():
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("--title", default="Halcyon")
    p.add_argument("--yes-label")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--yesno")
    mode.add_argument("--error")
    mode.add_argument("--open")
    mode.add_argument("--busy")
    mode.add_argument("--checklist")
    mode.add_argument("--autoplay", action="store_true")
    p.add_argument("rest", nargs="*")
    args = p.parse_args()

    app = QApplication(sys.argv[:1])
    app.setApplicationName("halcyon-dialog")
    app.setDesktopFileName("halcyon-dialog")
    app.setStyle("Fusion")
    app.setPalette(light_palette())
    if hasattr(app.styleHints(), "setColorScheme"):
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    app.setStyleSheet(QSS)

    if args.yesno is not None:
        return yesno(args)
    if args.error is not None:
        return error(args)
    if args.open is not None:
        return open_file(args)
    if args.busy is not None:
        return busy(args)
    if args.checklist is not None:
        return checklist(args)
    return autoplay(args)


if __name__ == "__main__":
    os.environ.setdefault("QT_QPA_PLATFORM", "wayland;xcb")
    sys.exit(main())
