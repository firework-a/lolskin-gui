import os
import shutil
import sys
import winreg

import psutil
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QDialog

from mainWindow import Ui_MainWindow, Ui_Dialog


def get_install_dir():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\LOL")
        value, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        return value
    except Exception as e:
        show_message_box("ERROR", f"无法获取WeGame安装目录：{e}")
        return None


def is_lol_process_running():
    for proc in psutil.process_iter():
        try:
            if "League of Legends.exe" in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    show_message_box("ERROR", "LOL未运行，请在打开游戏后重试")
    return False


def show_message_box(title, text):
    dialog = QDialog()
    dialog.setWindowFlag(Qt.FramelessWindowHint)
    dialog.setAttribute(Qt.WA_TranslucentBackground)
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    ui.label.setText(f"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#ffd700;\">{title}</span></p></body></html>")
    ui.label_2.setText(f"<html><head/><body><p><span style=\" color:#ffd700;\">{text}</span></p></body></html>")
    dialog.exec_()


def inject():
    # 判断LOL进程是否启动
    if not is_lol_process_running():
        return

    # 判断是否是打包后的环境
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    # 文件列表
    files_to_copy = ['game.dll']
    download_dir = get_install_dir()
    if download_dir:
        all_files_exist = True
        for file in files_to_copy:
            file_to_copy = os.path.join(base_path, file)
            if not os.path.exists(file_to_copy):
                all_files_exist = False
                break
        if all_files_exist:
            for file in files_to_copy:
                file_to_copy = os.path.join(base_path, file)
                destination_path = os.path.join(download_dir, file)
                try:
                    shutil.copy2(file_to_copy, destination_path)
                except Exception as e:
                    show_message_box("ERROR", f"注入换肤 {file} 过程中出现错误: {e}")
                    return
            show_message_box("SUCCESS", "注入成功！")
        else:
            show_message_box("ERROR", "部分注入文件未找到。")
    else:
        show_message_box("ERROR", "未找到应用目录。")


def remove():
    # 判断LOL进程是否启动
    if not is_lol_process_running():
        return

    # 获取注入目录
    download_dir = get_install_dir()
    if download_dir:
        # 文件列表
        files_to_remove = ['game.dll']
        all_files_removed = True
        for file in files_to_remove:
            file_path = os.path.join(download_dir, file)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    all_files_removed = False
                    show_message_box("WARNING", "未注入，无需移除。")
            except Exception as e:
                all_files_removed = False
                show_message_box("ERROR", f"移除注入 {file} 时出现错误: {e}")
        if all_files_removed:
            show_message_box("SUCCESS", "注入已成功移除！")
    else:
        show_message_box("ERROR", "未找到应用目录。")


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 主界面
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置应用栏图标
        icon_path = resource_path("img/app_icon.ico")
        icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(icon)

        # 获取鼠标所在屏幕的索引
        screen_number = QDesktopWidget().screenNumber(QDesktopWidget().cursor().pos())
        screen = QDesktopWidget().screenGeometry(screen_number)
        width = screen.width()
        height = screen.height()
        # 计算窗口位置，这里将窗口定位在屏幕中心上方
        x = int((width - self.width()) / 1.9)
        y = int((height - self.height()) / 4)
        self.move(x, y)

        # 用于记录鼠标按下时的位置和窗口初始位置
        self.dragPos = QPoint()
        # 为窗口的鼠标按下、移动和释放事件绑定自定义函数
        self.ui.centralwidget.mousePressEvent = self.mousePressEvent
        self.ui.centralwidget.mouseMoveEvent = self.mouseMoveEvent
        self.ui.centralwidget.mouseReleaseEvent = self.mouseReleaseEvent

        # 注入dll
        self.ui.pushButton_3.clicked.connect(inject)

        # 清除注入
        self.ui.pushButton_4.clicked.connect(remove)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = QPoint()
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
