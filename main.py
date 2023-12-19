import sys
from functools import partial

from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget, QHBoxLayout,
    QLineEdit, QMenu
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.toolbarEvents()

        self.setWindowTitle("Sortowanie")

        self.setMinimumSize(QSize(300,300))

        layout = QVBoxLayout()


        title = QLabel("Wpisz ciąg liczb odzielonych przecinkiem:")
        layout.addWidget(title)
        global editText
        editText = QLineEdit()
        layout.addWidget(editText)
        global result
        result = QLabel("0")
        layout.addWidget(result)

        button1 = QPushButton("sortowanie bąbelkowe")
        button1.clicked.connect(partial(self.clicked, "bubble"))
        layout.addWidget(button1)

        bubble_shortcut = QKeySequence("Ctrl+B")
        bubble_action = QAction("sortowanie bąbelkowe", self)
        bubble_action.setShortcut(bubble_shortcut)
        bubble_action.triggered.connect(partial(self.clicked, "bubble"))
        self.addAction(bubble_action)

        button2 = QPushButton("sortowanie szybkie")
        button2.clicked.connect(partial(self.clicked, "quick"))
        layout.addWidget(button2)

        quick_shortcut = QKeySequence("Ctrl+Q")
        quick_action = QAction("sortowanie szybkie", self)
        quick_action.setShortcut(quick_shortcut)
        quick_action.triggered.connect(partial(self.clicked, "quick"))
        self.addAction(quick_action)

        button3 = QPushButton("sortowanie ze scalaniem")
        button3.clicked.connect(partial(self.clicked, "merge"))
        layout.addWidget(button3)

        merge_shortcut = QKeySequence("Ctrl+M")
        merge_action = QAction("sortowanie ze scalaniem", self)
        merge_action.setShortcut(merge_shortcut)
        merge_action.triggered.connect(partial(self.clicked, "merge"))
        self.addAction(merge_action)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def toolbarEvents(self):
        toolbar = self.addToolBar('sortowanie')

        sort_bubble = QAction("sortowanie bąbelkowe", self)
        sort_bubble.triggered.connect(partial(self.clicked, "bubble"))
        toolbar.addAction(sort_bubble)

        sort_quick = QAction("sortowanie szybkie", self)
        sort_quick.triggered.connect(partial(self.clicked, "quick"))
        toolbar.addAction(sort_quick)

        sort_merge = QAction("sortowanie ze scalaniem", self)
        sort_merge.triggered.connect(partial(self.clicked, "merge"))
        toolbar.addAction(sort_merge)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        sort_bubble = QAction("sortowanie bąbelkowe", self)
        sort_bubble.triggered.connect(partial(self.clicked, "bubble"))
        menu.addAction(sort_bubble)

        sort_quick = QAction("sortowanie szybkie", self)
        sort_quick.triggered.connect(partial(self.clicked, "quick"))
        menu.addAction(sort_quick)

        sort_merge = QAction("sortowanie ze scalaniem", self)
        sort_merge.triggered.connect(partial(self.clicked, "merge"))
        menu.addAction(sort_merge)

        menu.exec(self.mapToGlobal(event.pos()))

    def clicked(self, description):
        text = editText.text()

        if text:
            for c in text:
                if c.isnumeric() or c == ',':
                    continue
                else:
                    result.setText("Wrong input!")
                    return

            nums_str = text.split(',')

            while ("" in nums_str):
                nums_str.remove("")

            nums = []
            for n in nums_str:
                nums.append(int(n))

            res = 0
            match description:
                case 'bubble':
                    print('sortowanie bąbelkowe')
                    res = self.sortowanie_babelkowe(nums)
                case 'quick':
                    print('sortowanie szybkie')
                    res = self.sortowanie_szybkie(nums)
                case 'merge':
                    print('sortowanie ze scalaniem')
                    res = self.sortowanie_przez_scalanie(nums)
                case _:
                    result.setText("Something went wrong")
                    return

            result.setText(str(res))

#porównuje sąsiednie elementy tablicy i zamienia je miejscami, jeśli są one w złej kolejności. Proces ten powtarza się aż do momentu, gdy cała tablica jest posortowana
    def sortowanie_babelkowe(self, tablica):
        n = len(tablica)

        for i in range(n):
            for j in range(0, n - i - 1):
                if tablica[j] > tablica[j + 1]:
                    tablica[j], tablica[j + 1] = tablica[j + 1], tablica[j]

        return tablica

# opiera się na wybieraniu elementu rozdzielającego (tzw. pivot) i dzieleniu tablicy na dwie części: mniejsze od pivota i większe od pivota. Następnie rekurencyjnie sortujemy obie części
    def sortowanie_szybkie(self, tablica):
        if len(tablica) <= 1:
            return tablica
        else:
            pivot = tablica[0]
            mniejsze = [x for x in tablica[1:] if x <= pivot]
            wieksze = [x for x in tablica[1:] if x > pivot]
            return self.sortowanie_szybkie(mniejsze) + [pivot] + self.sortowanie_szybkie(wieksze)

# sortowanie przez scalanie polega na rekurencyjnym podziale tablicy na mniejsze części, a następnie scalaniu posortowanych części w jedną całość
    def sortowanie_przez_scalanie(self, tablica):
        if len(tablica) <= 1:
            return tablica

        srodek = len(tablica) // 2
        lewa_czesc = tablica[:srodek]
        prawa_czesc = tablica[srodek:]

        lewa_czesc = self.sortowanie_przez_scalanie(lewa_czesc)
        prawa_czesc = self.sortowanie_przez_scalanie(prawa_czesc)

        posortowana_tablica = []
        i = j = 0

        while i < len(lewa_czesc) and j < len(prawa_czesc):
            if lewa_czesc[i] < prawa_czesc[j]:
                posortowana_tablica.append(lewa_czesc[i])
                i += 1
            else:
                posortowana_tablica.append(prawa_czesc[j])
                j += 1

        posortowana_tablica.extend(lewa_czesc[i:])
        posortowana_tablica.extend(prawa_czesc[j:])

        return posortowana_tablica


app = QApplication()
window = MainWindow()
window.show()
app.exec()