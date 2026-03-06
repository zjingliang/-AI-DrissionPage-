"""
=============================================================
AI 图片做题工具 - 主窗口程序 (main.py)
=============================================================
【核心功能】
    1. 基于 TKinter 构建可视化图形界面（GUI）
    2. 支持本地图片选择（拖拽/文件选择框）
    3. 调用阿里云通义千问（qwen3-vl-plus）API 解析图片题目并返回解答
    4. 界面展示解题结果、用量信息，支持结果导出/复制
【运行环境】
    - Python 版本：3.8+（兼容 TKinter 新版特性）
    - 依赖包：
        pip install openai tkinter pillow  # pillow 用于图片预览
【使用说明】
    1. 修改.env文件中 Qwen_API_KEY 为你的阿里云 DashScope 有效密钥
    2. 直接运行本文件：python main.py
    3. 界面操作：
       - 点击「选择图片」按钮上传本地题目图片（支持png/jpg/jpeg）
       - 点击「开始解题」按钮调用AI接口
       - 结果区域查看解题答案，支持「复制结果」「导出文本」
【配置说明】
    - API_KEY：阿里云 DashScope 平台获取（https://dashscope.aliyun.com/）
    - base_url：固定为 https://dashscope.aliyuncs.com/compatible-mode/v1
    - 支持的图片格式：png、jpg、jpeg（最大不超过10MB）
【注意事项】
    1. 确保网络正常，API 密钥未过期且有足够调用额度
    2. TKinter 窗口适配主流系统（Windows/macOS/Linux），不同系统字体/布局可能略有差异
    3. 请勿泄露 API_KEY，建议通过环境变量加载（生产环境）
=============================================================
作者：猫哥烤鱼
创建日期：2026-03-06
版本：v1.0
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ai_solve_question import homework
from text_edition import setup_color_print, get_color_print


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    try:
        # 1. 加载图片 - 替换为你的图片路径
        image = Image.open("请勿修改此文件夹/logo.png")
        # 2. 调整图片大小（根据需要）
        resized_image = image.resize((20, 20))
        # 3. 转换为Tkinter可用格式
        tk_image = ImageTk.PhotoImage(resized_image)
        # 4. 创建标签并显示图片
        image_label = tk.Label(root, image=tk_image)
        image_label.pack(pady=1)  # 根据你的布局调整放置方式

    except FileNotFoundError:
        print("错误：未找到图片文件，请检查路径是否正确")
    except Exception as e:
        print(f"加载图片时出错：{e}")
    root.title('超星学习通助手')
    root.geometry('500x500')    # 设置尺寸
    root.resizable(False, False)    # 设置尺寸不可调节

    # 设置字体
    font_config = ('SimHei', 10)

    # 创建输入框架
    input_frame = ttk.LabelFrame(root, text='输入课程链接', padding=(20, 10))
    # 用pack布局方法将框架放到主窗口内
    input_frame.pack(fill=tk.X, padx=20, pady=10)

    # 配置列权重
    input_frame.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(0, weight=0)

    # 作文题号输入
    ttk.Label(input_frame, text='课程链接：', font=font_config).grid(
        row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10)
    )
    title_entry = ttk.Entry(input_frame, width=60, font=font_config)
    title_entry.grid(
        row=0, column=1, sticky=tk.W + tk.E,
        pady=5, padx=(0, 20)
    )

    # 是否静音
    model_var = tk.BooleanVar(value=True)
    ttk.Label(input_frame, text='是否静音：', font=font_config).grid(
        row=2, column=0, sticky=tk.W, pady=5, padx=(0, 5)
    )
    model_frame = ttk.Frame(input_frame)
    model_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
    ttk.Radiobutton(model_frame, text='是', variable=model_var, value=True).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(model_frame, text='否', variable=model_var, value=False).pack(side=tk.LEFT, padx=5)

    # 按钮触发测试
    def run_tasks():
        try:
            essay_num = title_entry.get()
            model_type = model_var.get()
            homework(essay_num, model_type)  # 调用导入模块的函数
        except ValueError:
            messagebox.showerror('提示', '请保证输入内容完整！')

    # 运行按钮
    calculate_button = ttk.Button(root, text='运行程序', command=run_tasks)
    calculate_button.pack(pady=5)

    # 结果显示框架
    result_frame = ttk.LabelFrame(root, text='程序运行结果', padding=(20, 10))
    result_frame.pack(fill=tk.X, padx=20, pady=10)

    result_var = tk.StringVar(value='运行程序前，请预先下载安装谷歌浏览器')
    ttk.Label(result_frame, textvariable=result_var, font=font_config, foreground='blue').pack(anchor=tk.W)

    # 创建文本框和滚动条
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    text_widget = tk.Text(frame, wrap=tk.WORD, font=("SimHei", 10))
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # 初始化颜色打印功能，关联到当前文本框
    redirector = setup_color_print(text_widget)
    color_print = get_color_print()

    color_print('欢迎使用学习通助手，本程序仅供技术分享使用，请诚信考试', color="blue")
    color_print('版本号：1.0.0', color="blue")
    color_print('作者：猫哥烤鱼', color="blue")

    # 进入事件主循环
    root.mainloop()
