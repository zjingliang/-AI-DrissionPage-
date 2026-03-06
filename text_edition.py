import sys
import tkinter as tk
from tkinter import ttk


# 全局变量存储打印函数和重定向器
_color_print = None
_redirector = None


def setup_color_print(text_widget):
    """初始化颜色打印功能，需要传入main.py中的文本组件"""
    global _color_print, _redirector

    class ColorPrintRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.original_stdout = sys.stdout
            self.default_color = "black"
            self.created_tags = set()

        def write(self, message, color=None):
            self.text_widget.config(state=tk.NORMAL)
            use_color = color or self.default_color

            if use_color not in self.created_tags:
                self.text_widget.tag_configure(use_color, foreground=use_color)
                self.created_tags.add(use_color)

            self.text_widget.insert('end', message, use_color)
            self.text_widget.see('end')
            self.text_widget.config(state=tk.DISABLED)

        def flush(self):
            pass

        def restore(self):
            sys.stdout = self.original_stdout

    _redirector = ColorPrintRedirector(text_widget)

    # 定义全局可用的颜色打印函数
    def color_print(*args, color=None, sep=' ', end='\n'):
        message = sep.join(map(str, args)) + end
        _redirector.write(message, color=color)

    _color_print = color_print
    return _redirector


def get_color_print():
    """供其他模块获取颜色打印函数"""
    global _color_print
    if _color_print is None:
        # 如果未初始化，返回普通print
        return print
    return _color_print


def restore_original_print():
    """恢复原始print功能"""
    global _redirector
    if _redirector:
        _redirector.restore()


class DeselectableRadiobuttonGroup:
    def __init__(self, parent, variable=None):
        self.parent = parent
        self.var = variable if variable else tk.StringVar(value="")
        self.buttons = []
        self.last_selected = ""

    def add_radiobutton(self, text, value):
        btn = ttk.Radiobutton(
            self.parent,
            text=text,
            variable=self.var,
            value=value,
            command=lambda v=value: self.on_click(v)
        )
        self.buttons.append(btn)
        return btn

    def on_click(self, current_value):
        if current_value == self.last_selected:
            self.var.set(0)
            self.last_selected = 0
        else:
            self.last_selected = current_value
