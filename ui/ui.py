"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *
from ttkbootstrap import *
from pytkUI.widgets import *
class WinGUI(Window):
    def __init__(self):
        super().__init__(themename="cosmo", hdpi=False)
        self.__win()
        self.tk_button_open = self.__tk_button_open(self)
        self.tk_button_colse = self.__tk_button_colse(self)
        self.tk_label_lvj29xd8 = self.__tk_label_lvj29xd8(self)
        self.tk_button_lvj2bp5b = self.__tk_button_lvj2bp5b(self)
    def __win(self):
        self.title("自解压工具 壁纸引擎特供版 by bili codeJack")
        # 设置窗口大小、居中
        width = 912
        height = 437
        # 设置窗口图标
        self.iconbitmap('Tools/icon.ico')
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.minsize(width=width, height=height)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def new_style(self,widget):
        ctl = widget.cget('style')
        ctl = "".join(random.sample('0123456789',5)) + "." + ctl
        widget.configure(style=ctl)
        return ctl
    def __tk_button_open(self,parent):
        # success
        btn = Button(parent, text="启动", takefocus=False,bootstyle="secondary")
        btn.place(relx=0.2248, rely=0.5538, relwidth=0.2566, relheight=0.1236)
        return btn
    def __tk_button_colse(self,parent):
        btn = Button(parent, text="关闭", takefocus=False,bootstyle="secondary")
        btn.place(relx=0.5439, rely=0.5538, relwidth=0.2566, relheight=0.1236)
        return btn
    def __tk_label_lvj29xd8(self,parent):
        label = Label(parent,text="自动解压工具 壁纸引擎特供版",anchor="center", bootstyle="primary")
        label.place(relx=0.1206, rely=0.2174, relwidth=0.7917, relheight=0.1625)
        return label
    def __tk_button_lvj2bp5b(self,parent):
        btn = Button(parent, text="BY bili codeJack", takefocus=False,bootstyle="default outline")
        btn.place(relx=0.8520, rely=0.9130, relwidth=0.1371, relheight=0.0709)
        return btn
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_open.bind('<Button-1>',self.ctl.openFn)
        self.tk_button_colse.bind('<Button-1>',self.ctl.closeFn)
        self.tk_button_lvj2bp5b.bind('<Button-1>',self.ctl.openbiliFn)
        pass
    def __style_config(self):
        sty = Style()
        sty.configure(self.new_style(self.tk_button_open),font=("微软雅黑",-24,"bold"))
        sty.configure(self.new_style(self.tk_button_colse),font=("微软雅黑",-24,"bold"))
        sty.configure(self.new_style(self.tk_label_lvj29xd8),font=("微软雅黑",-30,"bold"))
        sty.configure(self.new_style(self.tk_button_lvj2bp5b),font=("微软雅黑",-12))
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()