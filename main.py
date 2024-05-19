import random
import sys
import threading
import time

from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

# constants
ROW_COUNT = 200
COL_COUNT = 3

# create fake data: 100 rows, 3 columns
fake_data: list[list[int]] = []
for _ in range(ROW_COUNT):
    fake_data.append([random.randint(0, 100) for _ in range(COL_COUNT)])


class Window(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget(self)
        self.table.setRowCount(ROW_COUNT)
        self.table.setColumnCount(COL_COUNT)

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        btn1 = QPushButton("Load data (main thread)")
        btn1.clicked.connect(self.load_data)

        btn2 = QPushButton("Load data (create thread)")
        btn2.clicked.connect(self.load_data_thread)

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(self.table)

    def load_data(self):
        self.update_table()

    def load_data_thread(self):
        thr = threading.Thread(target=self.update_table, args=())
        thr.start()
        thr.join()

    def update_table(self):
        start = time.time()

        for row_idx, row_data in enumerate(fake_data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table.setItem(row_idx, col_idx, item)

        end = time.time()

        print(f"Execute time: {end - start}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
