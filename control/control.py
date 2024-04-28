"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
# 示例下载 https://www.pytk.net/blog/1702564569.html
import webbrowser
from utils.set_menu import check_menu, set_menu, del_menu, set_cmd_ascii_color
import os
import sys
exe_path = os.path.dirname(sys.argv[0])

class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: object
    def __init__(self):
        pass
    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui

        set_cmd_ascii_color()

        self.isopen = None

        if check_menu():
            self.ui.tk_button_open.config(bootstyle='success')
            self.ui.tk_button_colse.config(bootstyle='secondary')
            self.isopen = True
        else:
            self.ui.tk_button_open.config(bootstyle='secondary')
            self.ui.tk_button_colse.config(bootstyle='success')
            self.isopen = False

    def openFn(self,evt):
        # print("<Button-1>事件未处理:",evt)
        if self.isopen:
            return
        if set_menu(os.path.join(exe_path, 'Tools', "menuScript.exe"), os.path.join(exe_path, 'Tools', "icon.ico")):
            self.ui.tk_button_open.config(bootstyle='success')
            self.ui.tk_button_colse.config(bootstyle='secondary')
            self.isopen = True

    def closeFn(self,evt):
        # print("<Button-1>事件未处理:",evt)
        if not self.isopen:
            return
        if del_menu():
            self.ui.tk_button_open.config(bootstyle='secondary')
            self.ui.tk_button_colse.config(bootstyle='success')
            self.isopen = False
        
    def openbiliFn(self,evt):
        # print("<Button-1>事件未处理:",evt)
        # 打开网页
        webbrowser.open('https://space.bilibili.com/3546656381340250')
