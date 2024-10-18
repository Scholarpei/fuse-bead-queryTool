import sys
import csv
import re

from PyQt5.QtCore import Qt
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
    QHBoxLayout,
    QDialog,
    QHeaderView
)
from PyQt5.QtGui import QColor, QBrush

class ColorSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mard色号拼豆位置查询工具")
        self.resize(1200, 800)

        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
            }
            QLineEdit {
                padding: 5px;
                font-size: 16px;
                border: 1px solid #B0B0B0;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton[checked="true"] {
                background-color: #A9A9A9;
                color: black;
            }
            QTableWidget {
                border: 1px solid #B0B0B0;
                gridline-color: #E0E0E0;
                font-size: 14px;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
        """)

        self.selected_items = []  # 存储选中的项目

        # 布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 搜索框、标签和按钮的横向布局
        self.search_layout = QHBoxLayout()  # 创建一个水平布局

        self.search_label = QLabel("输入色号（如A1）:")
        self.search_layout.addWidget(self.search_label)  # 将标签添加到水平布局

        self.search_entry = QLineEdit()
        self.search_layout.addWidget(self.search_entry)  # 将搜索框添加到水平布局

        self.search_button = QPushButton("查找")
        self.search_button.clicked.connect(self.on_search)
        self.search_layout.addWidget(self.search_button)  # 将按钮添加到水平布局

        self.layout.addLayout(self.search_layout)  # 将水平布局添加到主布局

        # 连接回车键事件
        self.search_entry.returnPressed.connect(self.on_search)

        # 创建表格（QTableWidget）
        self.results_table = QTableWidget()
        self.results_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略为Expanding
        self.layout.addWidget(self.results_table)

        # 创建确认色号按钮
        self.confirm_button = QPushButton("确认色号")
        self.confirm_button.clicked.connect(self.show_selected_items)
        self.layout.addWidget(self.confirm_button)

        # 数据读取
        self.data = self.read_data("data.csv")

        # 设置表格头部的自动拉伸
        self.results_table.horizontalHeader().setStretchLastSection(True)

    def closeEvent(self, event):
        event.accept()  # 确保程序退出
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
        results = [item for item in self.data if pattern.search(item[1]) or query == ""]  # 模糊匹配名字
        return results

    def on_search(self):
        """搜索按钮功能"""
        query = self.search_entry.text().strip()  # 获取搜索词
        results = self.fuzzy_search(query)  # 搜索数据
        self.update_results(results)  # 更新显示结果

    def update_results(self, results):
        """更新结果表格显示"""
        self.results_table.clear()  # 清空旧结果
        self.results_table.setRowCount(0)  # 重置行数
        self.results_table.setColumnCount(6)  # 设置列数 (加上按钮列)
        self.results_table.setColumnWidth(0, 100)  # 设置颜色列宽
        self.results_table.setColumnWidth(1, 100)  # 设置名字列宽
        self.results_table.setColumnWidth(2, 100)  # 设置盒号列宽
        self.results_table.setColumnWidth(3, 100)  # 设置行列宽
        self.results_table.setColumnWidth(4, 100)  # 设置列宽
        self.results_table.setColumnWidth(5, 150)  # 设置“加入列表”按钮列宽

        # 设置表头
        self.results_table.setHorizontalHeaderLabels(["颜色", "色号", "盒号", "行", "列", "操作"])

        # 存储匹配到的数据到本地文件
        with open("results.csv", "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for result in results:
                rgb, name, box_number, row_num, col = result
                row_position = self.results_table.rowCount()  # 获取当前行数
                self.results_table.insertRow(row_position)  # 插入新行

                # 设置颜色单元格
                color_item = QTableWidgetItem()
                color_item.setBackground(QBrush(QColor("#" + rgb)))  # 添加前导“#”
                self.results_table.setItem(row_position, 0, color_item)  # 添加颜色单元格

                # 设置其他单元格内容
                self.results_table.setItem(row_position, 1, QTableWidgetItem(name))
                self.results_table.setItem(row_position, 2, QTableWidgetItem(box_number))
                self.results_table.setItem(row_position, 3, QTableWidgetItem(row_num))
                self.results_table.setItem(row_position, 4, QTableWidgetItem(col))

                # 添加“加入列表”按钮
                add_button = QPushButton("加入列表")
                add_button.setCheckable(True)  # 设置按钮为可切换状态
                add_button.clicked.connect(lambda checked, r=result, b=add_button: self.toggle_item(r, b))
                self.results_table.setCellWidget(row_position, 5, add_button)

                writer.writerow(result)  # 写入文件

        if not results:
            self.results_table.setRowCount(1)  # 如果没有结果，添加一行
            self.results_table.setItem(0, 0, QTableWidgetItem("No results found."))

    def toggle_item(self, item, button):
        """切换加入或取消加入列表"""
        if button.isChecked():
            button.setText("取消加入")
            button.setStyleSheet("background-color: #A9A9A9; color: black;")
            self.add_to_list(item)
        else:
            button.setText("加入列表")
            button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.remove_from_list(item)

    def add_to_list(self, item):
        """将选中的色号加入列表"""
        if item not in self.selected_items:
            self.selected_items.append(item)

    def remove_from_list(self, item):
        """将选中的色号从列表中移除"""
        if item in self.selected_items:
            self.selected_items.remove(item)

    def show_selected_items(self):
        """展示选中的色号"""
        dialog = QDialog(self)
        dialog.setWindowTitle("已选色号")
        dialog.resize(1200, 800)

        layout = QVBoxLayout(dialog)
        table = QTableWidget(len(self.selected_items), 6, dialog)
        table.setHorizontalHeaderLabels(["颜色", "色号", "盒号", "行", "列","数量（可编辑）"])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, item in enumerate(self.selected_items):
            rgb, name, box_number, row_num, col = item
            color_item = QTableWidgetItem()
            if len(rgb) == 6 and all(c in '0123456789ABCDEFabcdef' for c in rgb):
                color_item.setBackground(QBrush(QColor("#" + rgb)))  # 添加前导“#”
            else:
                # 如果颜色格式不正确，显示默认颜色或错误提示
                color_item.setText("Invalid Color")
            table.setItem(i, 0, color_item)
            table.setItem(i, 1, QTableWidgetItem(name))
            table.setItem(i, 2, QTableWidgetItem(box_number))
            table.setItem(i, 3, QTableWidgetItem(row_num))
            table.setItem(i, 4, QTableWidgetItem(col))
            quantity_item = QTableWidgetItem("0")  # 默认值为1，可以根据需要修改
            quantity_item.setBackground(QBrush(QColor(255, 255, 200)))
            table.setItem(i, 5, quantity_item)

        layout.addWidget(table)

        # 添加返回按钮
        return_button = QPushButton("返回")
        return_button.clicked.connect(lambda: self.return_to_main(dialog))
        layout.addWidget(return_button)

        # 隐藏主窗口并打开对话框
        self.hide()
        dialog.finished.connect(self.show)  # 对话框关闭时重新显示主窗口

        dialog.exec_()

    def dialog_close_event(self, event, dialog):
        """处理对话框关闭事件"""
        dialog.hide()  # 隐藏对话框而不是退出程序
        event.ignore()  # 忽略关闭事件

    def return_to_main(self, dialog):
        """返回主界面"""
        dialog.close()  # 关闭对话框
        self.show()  # 重新显示主窗口

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorSearchApp()
    window.show()
    sys.exit(app.exec_())
