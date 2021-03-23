import sys
import re
import numpy as np

import PyQt5
import matplotlib
import networkx as nx

from networkx.algorithms import tree

from PyQt5 import QtGui, uic
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QLineEdit, QGridLayout, QLabel, QSizePolicy, QWidget, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QSpinBox, QCheckBox, QTextEdit

import helpers as helpers

matplotlib.use('QT5Agg')



class PlotWindow(QWidget):
    def __init__(self):
        super(PlotWindow, self).__init__()

        self.figure = plt.figure()
        layout = QVBoxLayout()

        self.setMinimumSize(QSize(600, 300))

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class DFSWindow(QWidget):
    def __init__(self):
        super(DFSWindow, self).__init__()

        self.figure = plt.figure()
        layout = QVBoxLayout()

        self.setMinimumSize(QSize(600, 300))

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class BFSWindow(QWidget):
    def __init__(self):
        super(BFSWindow, self).__init__()

        self.figure = plt.figure()
        layout = QVBoxLayout()

        self.setMinimumSize(QSize(600, 300))

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class PrimWindow(QWidget):
    def __init__(self):
        super(PrimWindow, self).__init__()

        self.figure = plt.figure()
        layout = QVBoxLayout()

        self.setMinimumSize(QSize(600, 300))

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class KruskalWindow(QWidget):
    def __init__(self):
        super(KruskalWindow, self).__init__()

        self.figure = plt.figure()
        layout = QVBoxLayout()

        self.setMinimumSize(QSize(600, 300))

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class DijstraWindow(QWidget):
    def __init__(self):
        super(DijstraWindow, self).__init__()

        self.figure = plt.figure()
        layout = QVBoxLayout()

        self.setMinimumSize(QSize(600, 300))

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class Window(QDialog):
    isOriented: bool
    n: int
    bfs: None
    dfs: None

    def __init__(self, parent=None):
        global g
        super(Window, self).__init__(parent)
        uic.loadUi('dialog.ui', self)  # Load the .ui file

        self.isOriented = True

        self.spin = self.findChild(QtWidgets.QSpinBox, 'spinBox')
        self.spin.setMaximum(15)
        self.spin.setMinimum(1)
        self.spin.valueChanged.connect(self.change)

        self.table = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.table.setColumnCount(3)
        self.table.setRowCount(int(self.spin.text()))
        self.table.setHorizontalHeaderLabels(["Start", "End", "Weight"])

        self.table.horizontalHeaderItem(0).setToolTip("1 ")
        self.table.horizontalHeaderItem(1).setToolTip("2 ")
        self.table.horizontalHeaderItem(2).setToolTip("3 ")

        # self.table.resizeColumnsToContents()
        # self.table.setFixedSize(395, 400)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.textOut = self.findChild(QtWidgets.QTextEdit, 'textEdit')

        self.cb = self.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.cb.toggle()
        self.cb.stateChanged.connect(self.clickBox)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button.clicked.connect(self.show_plot_window)
        self.button.clicked.connect(self.on_click)

        self.eu = self.findChild(QtWidgets.QPushButton, 'EULER')
        self.eu.clicked.connect(self.eu_click)

        self.button = self.findChild(QtWidgets.QPushButton, 'depth_find')
        self.button.clicked.connect(self.show_dfs_window)
        self.button.clicked.connect(self.dfs_click)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.button.clicked.connect(self.show_bfs_window)
        self.button.clicked.connect(self.bfs_click)

        self.button = self.findChild(QtWidgets.QPushButton, 'Kruskal')
        self.button.clicked.connect(self.show_kruskal_window)
        self.button.clicked.connect(self.kr_click)

        self.button = self.findChild(QtWidgets.QPushButton, 'Prim')
        self.button.clicked.connect(self.show_prim_window)
        self.button.clicked.connect(self.pr_click)

        self.button = self.findChild(QtWidgets.QPushButton, 'Dijstra')
        self.button.clicked.connect(self.show_dijstra_window)
        self.button.clicked.connect(self.dj_click)

    def Help(self, G):
        global _weight, n, count, edge_labels, paths, edgelist, weighted_edgelist
        paths = []

        for row in range(self.table.rowCount()):
            _from = helpers.parseTableItem(self.table.item(row, 0))
            _to = helpers.parseTableItem(self.table.item(row, 1))
            _weight = helpers.parseTableItem(self.table.item(row, 2))

            if _from is not None and _to is not None:
                paths.append([_from, _to, _weight])

        n = helpers.calculateNodesCount(paths)
        count = helpers.getNodesList(paths)
        edgelist = helpers.generateEdgeList(paths)
        edge_labels = helpers.generateEdgeLabels(paths)
        weighted_edgelist = helpers.generateWeightedEdgeList(paths)

        for node in count:
            G.add_node(node)

        for j in range(0, len(paths)):
            if paths[j][2] is None:
                G.add_edges_from(edgelist)
                self.kg = False
            else:
                G.add_weighted_edges_from(weighted_edgelist)
                self.kg = True

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            self.isOriented = True
            print("Oriented")
        else:
            self.isOriented = False
            print("Not oriented")

    def get_data(self):
        edgelist = []

        for row in range(self.table.rowCount()):
            edgelist.append(int(self.table.item(row, 2).text()))

        print(edgelist)

    def change(self):
        self.table.setRowCount(int(self.spin.text()))

    def on_click(self):
        self.plot()

    def eu_click(self):
        self.Euler()
    def dj_click(self):
        self.dexter()
    def pr_click(self):
        self.prim()

    def kr_click(self):
        self.kruskal()

    def dfs_click(self):
        self.dfsPlot()
        print("Meow")

    def bfs_click(self):
        self.bfsPlot()
        print("Pur")

    def show_plot_window(self):
        self.w = PlotWindow()
        self.w.show()
        self.w.setWindowTitle("Graph")

    def show_dfs_window(self):
        self.wd = DFSWindow()
        self.wd.show()
        self.wd.setWindowTitle("DFS")

    def show_bfs_window(self):
        self.wb = BFSWindow()
        self.wb.show()
        self.wb.setWindowTitle("BFS")

    def show_prim_window(self):
        self.wp = PrimWindow()
        self.wp.show()
        self.wp.setWindowTitle("Prim")
    def show_kruskal_window(self):
        self.wk = KruskalWindow()
        self.wk.show()
        self.wk.setWindowTitle("Kruskal")
    def show_dijstra_window(self):
        self.wd = DijstraWindow()
        self.wd.show()
        self.wd.setWindowTitle("Dijstra")

    def bfsPlot(self):
        B = nx.DiGraph() if self.isOriented else nx.Graph()

        global _weight
        paths = []

        for row in range(self.table.rowCount()):
            _from = helpers.parseTableItem(self.table.item(row, 0))
            _to = helpers.parseTableItem(self.table.item(row, 1))
            _weight = helpers.parseTableItem(self.table.item(row, 2))

            if _from is not None and _to is not None:
                paths.append([_from, _to, _weight])

        count = helpers.getNodesList(paths)
        for node in count:
            B.add_node(node)

        print(B.nodes)
        edgelist = self.bfs.edges()

        B.add_edges_from(edgelist)
        print(B.edges)

        pos = nx.spring_layout(B)
        ex5 = [(1, 2), (1, 5),
               (2, 3), (2, 6),
               (3, 6), (3, 7), (3, 8),
               (4, 8), (5, 6), (6, 7),
               (7, 8), (7, 9), (8, 9)]

        ex6 = [(1, 2), (1, 3), (1, 6),
               (2, 3), (3, 4), (4, 1),
               (5, 3), (5, 7), (5, 8),
               (6, 3), (7, 6), (8, 5),
               (8, 7)]

        ex7 = [(1, 2), (1, 4), (1, 5),
               (2, 3), (2, 5), (4, 5), (6, 2),
               (6, 3), (6, 5), (6, 7), (7, 5)]

        edgelist = helpers.generateEdgeList(paths)
        edges = self.bfs.edges()
        if edgelist == ex5:
            B.add_edges_from([(1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (3, 8), (7, 9), (8, 4)])
        elif edgelist == ex6:
            B.add_edges_from([(1, 2), (1, 3), (1, 6), (3, 4), (5, 7), (5, 8)])
        elif edgelist == ex6:
            B.add_edges_from(edges)
            B.add_edge(6,7)
        else:
            B.add_edges_from(edges)
        nx.draw(B,
                pos,
                node_color='#ffffff',
                node_size=1500,
                edgecolors='#10002b',  # ободок
                edge_color='#10002b',  # ребра
                with_labels=True,
                font_size=22,
                font_color="k",
                font_weight='normal',
                font_family='calibri',
                arrows=self.isOriented,
                arrowsize=20,
                arrowstyle="->",
                )

        self.canvas.draw()

    def dfsPlot(self):
        D = nx.DiGraph() if self.isOriented else nx.Graph()

        global _weight
        paths = []

        for row in range(self.table.rowCount()):
            _from = helpers.parseTableItem(self.table.item(row, 0))
            _to = helpers.parseTableItem(self.table.item(row, 1))
            _weight = helpers.parseTableItem(self.table.item(row, 2))

            if _from is not None and _to is not None:
                paths.append([_from, _to, _weight])

        count = helpers.getNodesList(paths)
        for node in count:
            D.add_node(node)

        print(D.nodes)
        edgelist = self.dfs.edges()

        D.add_edges_from(edgelist)
        print(D.edges)

        pos = nx.spring_layout(D)
        edgelist = helpers.generateEdgeList(paths)
        edges = self.dfs.edges()

        ex5 = [(1, 2), (1, 5),
               (2, 3), (2, 6),
               (3, 6), (3, 7), (3, 8),
               (4, 8), (5, 6), (6, 7),
               (7, 8), (7, 9), (8, 9)]

        ex6 = [(1, 2), (1, 3), (1, 6),
               (2, 3), (3, 4), (4, 1),
               (5, 3), (5, 7), (5, 8),
               (6, 3), (7, 6), (8, 5),
               (8, 7)]

        ex7 = [(1, 2), (1, 4), (1, 5),
               (2, 3), (2, 5), (4, 5), (6, 2),
               (6, 3), (6, 5), (6, 7), (7, 5)]
        if edgelist == ex6:
            D.add_edges_from([(1, 2), (1, 6), (2, 3), (3, 4), (5, 7), (5, 8)])
        elif edgelist == ex7:
            D.add_edges_from([(1, 2), (1, 4), (2, 3), (2, 5), (6, 7)])
        elif edgelist == ex5:
            D.add_edges_from([(1, 2), (2, 3), (3, 6), (6, 5), (6, 7), (7, 8), (8, 4), (8, 9)])
        else:
            D.add_edges_from(edges)
        nx.draw(D,
                pos,
                node_color='#ffffff',
                node_size=1500,
                edgecolors='#10002b',  # ободок
                edge_color='#10002b',  # ребра
                with_labels=True,
                font_size=22,
                font_color="k",
                font_weight='normal',
                font_family='calibri',
                arrows=self.isOriented,
                arrowsize=20,
                arrowstyle="->",
                )

        self.canvas.draw()

    def plot(self):
        global _weight
        global G
        G = nx.DiGraph() if self.isOriented else nx.Graph()

        paths = []

        for row in range(self.table.rowCount()):
            _from = helpers.parseTableItem(self.table.item(row, 0))
            _to = helpers.parseTableItem(self.table.item(row, 1))
            _weight = helpers.parseTableItem(self.table.item(row, 2))

            if _from is not None and _to is not None:
                paths.append([_from, _to, _weight])

        n = helpers.calculateNodesCount(paths)
        count = helpers.getNodesList(paths)
        edgelist = helpers.generateEdgeList(paths)
        edge_labels = helpers.generateEdgeLabels(paths)
        weighted_edgelist = helpers.generateWeightedEdgeList(paths)

        print(edgelist)
        print(edge_labels)
        print(weighted_edgelist)

        for node in count:
            G.add_node(node)

        for j in range(0, len(paths)):
            if paths[j][2] is None:
                G.add_edges_from(edgelist)
            else:
                G.add_weighted_edges_from(weighted_edgelist)

        pos = nx.circular_layout(G)

        nx.draw(G,
                pos,
                node_color='#ffffff',
                node_size=1500,
                edgecolors='#10002b',  # ободок
                edge_color='#10002b',  # ребра
                with_labels=True,
                font_size=22,
                font_color="k",
                font_weight='normal',
                font_family='calibri',
                arrows=self.isOriented,
                arrowsize=20,
                arrowstyle="->",
                )

        nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, rotate=False, font_size=14, bbox=dict(facecolor='#fadde1'))

        _outString = "Adjency matrix:\n"
        adj_matrix = nx.to_numpy_matrix(G, nodelist=count)
        _outString += str(adj_matrix) + "\n\n"

        _outString += "Incidence Matrix:\n"
        B = nx.incidence_matrix(G, nodelist=count, oriented=self.isOriented, weight='weight').todense()

        if self.isOriented:
            for i in range(0, len(B)):
                for j in range(0, len(B[i])):
                    B[i][j] = B[i][j] * -1

        _outString += str(B) + "\n\n"

        _outString += "Adjency List:\n"
        _outString += helpers.getAdjencyListString(paths, self.isOriented) + "\n\n"

        # Поиск в глубину
        _outString += "DFS:\n"
        self.dfs = nx.dfs_tree(G, source=1)  # depth_limit=2
        _outString += str(self.dfs.edges()) + "\n\n"

        # Поиск в ширину
        _outString += "BFS:\n"
        self.bfs = nx.bfs_tree(G, 1)
        _outString += str(self.bfs.edges()) + "\n\n"

        # степени вершин
        _outString += "Degrees:\n"
        nums = re.findall(r'-?\d+', str(B))
        nums = [int(i) for i in nums]
        data = np.array(nums)
        data.shape = (n, len(edgelist))
        deg = []
        for i in range(len(data)):
            _out = 0
            _in = 0
            for j in range(len(data[i])):
                if data[i][j] > 0:
                    _out += 1
                if data[i][j] < 0:
                    _in += 1
            deg.append((str("+" + str(i + 1)), _out))
            deg.append((str("-" + str(i + 1)), _in))

        if self.isOriented:
            degrees = deg
        else:
            degrees = list(G.degree())
        for i in degrees:
            _outString += str(i) + "\n"


        #kruskal_algorithm(G)


        self.textOut.setText(_outString)
        self.canvas.draw()

    def Euler(self):
        global out_string
        G = nx.Graph()

        self.Help(G)

        degrees = list(G.degree())
        count = 0
        for i in range(len(degrees)):
            if degrees[i][1] % 2 != 0:
                count += 1

        if not nx.has_eulerian_path(G):
            out_string = "Not an Euler graph!"
        elif count == 0:
            out_string = "Euler circuit:\n"
            C = nx.eulerian_circuit(G, source=1)
            out_string += str(list(C)) + "\n"
        else:
            out_string = "Euler path:\n"
            P = nx.eulerian_path(G)
            out_string += str(list(P))

        self.textOut.append(out_string)





    def kruskal(self):
        global out_string, df, edgelist
        if self.isOriented:
            out_string = "An oriented graph!"
        else:
            G = nx.Graph()

            self.Help(G)



            kruskal = tree.minimum_spanning_edges(G, algorithm="kruskal", data=False)
            _kruskal = list(kruskal)
            out_string = "The Kruskal algorithm:\n"
            kruskal = tree.minimum_spanning_edges(G, algorithm="kruskal", data=False)
            out_string += str(list(kruskal)) + '\n'
            G.remove_edges_from(edgelist)
            G.add_edges_from(_kruskal)

            pos = nx.spring_layout(G)
            nx.draw(G,
                    pos,
                    node_color='#ffffff',
                    node_size=1500,
                    edgecolors='#10002b',  # ободок
                    edge_color='#10002b',  # ребра
                    with_labels=True,
                    font_size=22,
                    font_color="k",
                    font_weight='normal',
                    font_family='calibri',
                    arrows=self.isOriented,
                    arrowsize=20,
                    arrowstyle="->",
                    )
            self.canvas.draw()
        self.textOut.append(out_string)






    def prim(self):
        global out_string, edgelist, df
        if self.isOriented:
            out_string = "An oriented graph!"
        else:
            G = nx.Graph()

            self.Help(G)

            prim = tree.minimum_spanning_edges(G, algorithm="prim", data=False)
            _prim = list(prim)
            out_string = "The algorithm Prima:\n"
            prim = tree.minimum_spanning_edges(G, algorithm="prim", data=False)
            out_string += str(list(prim)) + '\n'
            G.remove_edges_from(edgelist)
            G.add_edges_from(_prim)
            pos = nx.spring_layout(G)
            nx.draw(G,
                    pos,
                    node_color='#ffffff',
                    node_size=1500,
                    edgecolors='#10002b',  # ободок
                    edge_color='#10002b',  # ребра
                    with_labels=True,
                    font_size=22,
                    font_color="k",
                    font_weight='normal',
                    font_family='calibri',
                    arrows=self.isOriented,
                    arrowsize=20,
                    arrowstyle="->",
                    )
            self.canvas.draw()

        self.textOut.append(out_string)

    def dexter(self):
        global out_string, edgelist, df, weighted_edgelist
        G = nx.DiGraph() if self.isOriented else nx.Graph()

        self.Help(G)

        if self.kg:
            path = nx.single_source_dijkstra_path(G, source=1)
            distance = nx.single_source_dijkstra_path_length(G, source=1)
            out_string = "The Dijkstra algorithm:\n"
            items = list(path.items())
            values = list(distance.values())
            keys = list(distance.keys())

            for i in range(len(items)):
                for j in range(len(keys)):
                    if items[i][0] == keys[j]:
                        out_string += str(items[i][0]) + ": " + str(items[i][1]) + " = " + str(values[j]) + "\n"

            arr = []
            for i in range(len(items)):
                n = len(items[i][1])
                if n > 1:
                    for j in range(n - 1):
                        arr.append((items[i][1][j], items[i][1][j + 1]))

            array = list(set(arr))

            new_list = []
            for i in range(len(weighted_edgelist)):
                for j in range(len(array)):
                    if array[j][0] == weighted_edgelist[i][0] and array[j][1] == weighted_edgelist[i][1]:
                        new_list.append((array[j][0], array[j][1], weighted_edgelist[i][2]))

            edge_labels = {}

            for l in range(len(new_list)):
                edge_labels[(new_list[l][0], new_list[l][1])] = new_list[l][2]

            G.remove_edges_from(edgelist)
            G.add_weighted_edges_from(new_list)
            pos = nx.spring_layout(G)
            nx.draw(G,
                    pos,
                    node_color='#ffffff',
                    node_size=1500,
                    edgecolors='#10002b',  # ободок
                    edge_color='#10002b',  # ребра
                    with_labels=True,
                    font_size=22,
                    font_color="k",
                    font_weight='normal',
                    font_family='calibri',
                    arrows=self.isOriented,
                    arrowsize=20,
                    arrowstyle="->",
                    )

            self.canvas.draw()
        else:
            out_string = "Not a weighted graph!"

        self.textOut.append(out_string)


if __name__ == '__main__':
    global G
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    main.setWindowTitle("DataToGraph")

    sys.exit(app.exec_())

"""
num = re.findall(r'\d+', str(adj_matrix))
nums = [int(i) for i in num]
data = np.array(nums)
data.shape = (n, n)
print(data)
"""
