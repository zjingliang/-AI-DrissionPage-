"""
    该文件用于AI自动答题
"""
from DrissionPage import Chromium, ChromiumOptions
import time
from text_edition import get_color_print
from config import API_KEY
from openai import OpenAI
import base64
import os


def image_to_base64(image_path):
    """
    将本地图片转换为Base64编码的Data URL（模型可识别格式）
    :param image_path: 本地图片路径（如 ./自动下载题库/img.png）
    :return: Base64编码的Data URL
    """
    # 检查文件是否存在
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在：{image_path}")

    # 获取图片格式（png/jpg/jpeg等）
    img_ext = image_path.split(".")[-1].lower()
    if img_ext not in ["png", "jpg", "jpeg", "gif", "bmp"]:
        raise ValueError(f"不支持的图片格式：{img_ext}，仅支持png/jpg/jpeg/gif/bmp")

    # 读取图片并转换为Base64
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    # 构造Data URL（模型要求的格式）
    data_url = f"data:image/{img_ext};base64,{img_base64}"
    return data_url


def homework(url="https://i.chaoxing.com/", model_type=True):
    # 调用千问
    # 初始化OpenAI客户端
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    prompts = """
                请你回答下列问题，并给出答案，只用回答选项的索引（从1开始），若答案有多个选项，应只回答索引数字，不要有任何分隔符或空格。
                例如：
                    多选题：
                        以下哪些书籍属于四书五经。
                        A、《大学》
                        B、《中庸》
                        C、《墨子》
                        D、《春秋》
                你的回答应为：124
            """

    color_print = get_color_print()
    # 实例化一个浏览器对象
    co = ChromiumOptions()
    # 设置不加载图片、静音
    co.no_imgs(False).mute(model_type)
    # 默认窗口最大化
    co.set_argument('--start-maximized')
    browser = Chromium(addr_or_opts=co)
    chaoxing = browser.latest_tab
    i = 0

    # 封装用于答题的函数
    def answer_question():
        question_count = len(chaoxing.eles("xpath=//*[@id=\"ZyBottom\"]/div[*]"))
        for number in range(question_count):
            color_print(f"开始检查题目{number + 1}...")
            time.sleep(0.5)
            chaoxing.ele(
                f"xpath=/html/body/div[6]/div/div[2]/div/form/div/div[{number + 1}]").get_screenshot(
                path=rf"./自动下载题库/img_{number + 1}.png")
            color_print(f"题目{number + 1}检查成功！")
            img_file = rf"./自动下载题库/img_{number + 1}.png"
            img_data_url = image_to_base64(img_file)
            color_print("题库下载成功！")
            # 调用API回答问题
            completion = client.chat.completions.create(
                model="qwen3-vl-plus",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img_data_url
                                },
                            },
                            {"type": "text", "text": prompts},
                        ],
                    },
                ],
                stream=False,
                # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
                extra_body={
                    'enable_thinking': False,
                    "thinking_budget": 81920},
            )
            answers_num = completion.choices[0].message.content.replace("A", "1").replace("B",
                                                                                          "2").replace(
                "C", "3").replace("D", "4").replace("E", "5").replace("F", "6").replace("G",
                                                                                        "7").replace(
                "H", "8").replace("I", "9")
            # color_color_print("最终答案：", completion.choices[0].message.content.replace("1", "A").replace("2", "B").replace("3", "C").replace("4", "D").replace("5", "E").replace("6", "F").replace("7", "G").replace("8", "H").replace("9", "I"))
            color_print(answers_num)
            for answer in answers_num:
                if chaoxing.ele(
                        f"xpath=//*[@id=\"ZyBottom\"]/div[{number + 1}]/div/div[2]//li[{answer}]/label/span",
                        timeout=0.3):
                    chaoxing.ele(
                        f"xpath=//*[@id=\"ZyBottom\"]/div[{number + 1}]/div/div[2]//li[{answer}]/label/span").click()
                else:
                    color_print("选择按钮失效！")
                    break
                "//*[@id=\"ZyBottom\"]/div[4]/div/div[2]/div/ul/li[1]/label/span"
        if chaoxing.ele("@text()=提交", timeout=0.5):
            chaoxing.ele("@text()=提交").click()
            time.sleep(1)
            if chaoxing.ele("xpath=//*[@id=\"popok\"]", timeout=1):
                try:
                    chaoxing.ele("xpath=//*[@id=\"popok\"]").click()
                except Exception as e:
                    color_print("第二次提交按钮失效！")
                    pass
        else:
            color_print("第一次提交按钮失效！")
            pass

    # 封装回答课上习题的函数
    def class_answer():
        if chaoxing.ele("xpath=//*[@class=\"tkItem\"]", timeout=0.1):
            chaoxing.ele(
                "@class=tkItem").get_screenshot(
                path=rf"./自动下载题库/img.png")
            color_print(f"课堂在线题目检查成功！")
            img_file = rf"./自动下载题库/img.png"
            img_data_url = image_to_base64(img_file)
            color_print("题库下载成功！")

            # 调用API回答问题
            # 创建聊天完成请求
            completion = client.chat.completions.create(
                model="qwen3-vl-plus",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img_data_url
                                },
                            },
                            {"type": "text", "text": prompts},
                        ],
                    },
                ],
                stream=False,
                # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
                extra_body={
                    'enable_thinking': False,
                    "thinking_budget": 81920},
            )

            answers_num = completion.choices[0].message.content.replace("A", "1").replace("B",
                                                                                          "2").replace(
                "C", "3").replace("D", "4").replace("E", "5").replace("F", "6").replace("G",
                                                                                        "7").replace(
                "H", "8").replace("I", "9")
            color_print("最终答案：", completion.choices[0].message.content.replace("1", "A").replace("2",
                                                                                                 "B").replace(
                "3", "C").replace("4", "D").replace("5", "E").replace("6", "F").replace("7",
                                                                                        "G").replace(
                "8", "H").replace("9", "I"))
            try:
                for answer in answers_num:
                    answer_list = chaoxing.eles(f"xpath=//*[@class=\"tkItem\"]",
                                 timeout=0.5)
                    answer_list[int(answer) - 1].click()
                chaoxing.ele("@text()=提交", timeout=0.5).click()
                if chaoxing.ele("xpath=//*[@id=\"video\"]/div[*]/button/span[2]",
                                timeout=600).text == "播放":
                    chaoxing.ele("xpath=//*[@id=\"video\"]/div[*]/button/span[2]", timeout=0.5).click()
            except Exception as e:
                pass
        else:
            pass

    while True:
        chaoxing.get(url)
        chaoxing.ele("@text():章节", timeout=180).click()
        chaoxing.listen.start(targets="mooc1.chaoxing.com/ananas/video-editor/sub?objectid")
        chaoxing.listen.stop()
        time.sleep(1)
        chaoxing.listen.start(targets="mooc1.chaoxing.com/ananas/video-editor/sub?objectid")
        if chaoxing.eles("xpath=//span[@class=\"catalog_points_yi\"]", timeout=1):
            if len(chaoxing.eles("xpath=//span[@class=\"catalog_points_yi\"]", timeout=1)) >= i:
                chaoxing.eles("xpath=//span[@class=\"catalog_points_yi\"]", timeout=1)[i].click()
                if chaoxing.ele("xpath=//*[@id=\"RightCon\"]/div[1]/div[1]", timeout=2):
                    if chaoxing.ele("xpath=//*[@id=\"RightCon\"]/div[1]/div[1]", timeout=1).text == "章节测验":
                        answer_question()
                        continue
                else:
                    try:
                        if chaoxing.ele("@text()=视频", timeout=1.5):
                            chaoxing.ele("@text()=视频", timeout=1).click()
                        else:
                            color_print("无法查找到视频控件！")
                            pass
                    except Exception as e:
                        pass

                    try:
                        location = chaoxing.ele("@title=播放视频").rect.location
                        chaoxing.actions.move_to(location).click()
                        time.sleep(1)
                    except Exception as e:
                        i += 1
                        continue

                    while True:
                        time.sleep(0.1)
                        if chaoxing.ele("xpath=//*[@id=\"video\"]/div[*]/button/span[2]", timeout=0.1):
                            # 校验：回答课上习题
                            class_answer()
                            if chaoxing.ele("xpath=//*[@id=\"video\"]/div[*]/button/span[2]", timeout=0.1).text == "播放":
                                try:
                                    chaoxing.ele("xpath=//*[@id=\"video\"]/div[*]/button/span[2]", timeout=0.1).click()
                                except Exception as e:
                                    pass
                            # # 回答课上习题
                            # class_answer()

                            if chaoxing.ele("@aria-label=任务点已完成", timeout=0.1):
                                color_print("任务点已完成")
                                break
                    if chaoxing.ele("@text()=章节测验", timeout=1):
                        try:
                            chaoxing.ele("@text()=章节测验", timeout=0.5).click()
                            time.sleep(1)
                            if chaoxing.ele("@aria-label=任务点已完成", timeout=0.3):
                                color_print("任务点已完成")
                                continue
                            else:
                                answer_question()
                        except Exception as e:
                            continue
            else:
                continue
        else:
            break
