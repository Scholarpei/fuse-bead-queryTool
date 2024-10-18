import sys
import csv
import re
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QSizePolicy,
)
from PyQt5.QtGui import QColor, QBrush

class ColorSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mard色号拼豆位置查询工具")

        # 布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 搜索框
        self.search_label = QLabel("输入色号（如A1）:")
        self.layout.addWidget(self.search_label)

        self.search_entry = QLineEdit()
        self.layout.addWidget(self.search_entry)

        # 连接回车键事件
        self.search_entry.returnPressed.connect(self.on_search)

        # 搜索按钮
        self.search_button = QPushButton("查找")
        self.search_button.clicked.connect(self.on_search)
        self.layout.addWidget(self.search_button)

        # 创建表格（QTableWidget）
        self.results_table = QTableWidget()
        self.results_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略为Expanding
        self.layout.addWidget(self.results_table)

        # 数据读取
        self.data = self.read_data("data.csv")

        # 设置表格头部的自动拉伸
        self.results_table.horizontalHeader().setStretchLastSection(True)

    def read_data(self, file_path):
        """读取数据文件"""
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rgb = row[0]  # 直接读取十六进制颜色字符串
                name = row[1]  # 名字
                box_number = row[2]  # 盒号
                row_num = row[3]  # 行
                col = row[4]  # 列
                data.append((rgb, name, box_number, row_num, col))
        return data

    def fuzzy_search(self, query):
        """模糊搜索功能"""
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        results = [item for item in self.data if pattern.search(item[1])]  # 模糊匹配名字
        return results

    def on_search(self):
        """搜索按钮功能"""
        query = self.search_entry.text()  # 获取搜索词
        results = self.fuzzy_search(query)  # 搜索数据
        self.update_results(results)  # 更新显示结果

    def update_results(self, results):
        """更新结果表格显示"""
        self.results_table.clear()  # 清空旧结果
        self.results_table.setRowCount(0)  # 重置行数
        self.results_table.setColumnCount(5)  # 设置列数
        self.results_table.setColumnWidth(0, 100)  # 设置颜色列宽
        self.results_table.setColumnWidth(1, 100)  # 设置名字列宽
        self.results_table.setColumnWidth(2, 100)  # 设置盒号列宽
        self.results_table.setColumnWidth(3, 100)  # 设置行列宽
        self.results_table.setColumnWidth(4, 100)  # 设置列宽
        # 设置表头
        self.results_table.setHorizontalHeaderLabels(["颜色", "色号", "盒号", "行", "列"])

        # 存储匹配到的数据到本地文件
        with open("results.csv", "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for result in results:
                rgb, name, box_number, row_num, col = result
                row_position = self.results_table.rowCount()  # 获取当前行数
                self.results_table.insertRow(row_position)  # 插入新行

                # 设置颜色单元格
                color_item = QTableWidgetItem()
                color_item.setBackground(QBrush(QColor(*[int(rgb[i:i + 2], 16) for i in (1, 3, 5)])))  # 转换RGB
                self.results_table.setItem(row_position, 0, color_item)  # 添加颜色单元格

                # 设置其他单元格内容
                self.results_table.setItem(row_position, 1, QTableWidgetItem(name))
                self.results_table.setItem(row_position, 2, QTableWidgetItem(box_number))
                self.results_table.setItem(row_position, 3, QTableWidgetItem(row_num))
                self.results_table.setItem(row_position, 4, QTableWidgetItem(col))

                writer.writerow(result)  # 写入文件

        if not results:
            self.results_table.setRowCount(1)  # 如果没有结果，添加一行
            self.results_table.setItem(0, 0, QTableWidgetItem("No results found."))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ColorSearchApp()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec_())
