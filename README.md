# 超星学习通 AI 自动刷课 + 答题工具 | 基于 DrissionPage 实现

[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一款基于 Python + DrissionPage + 通义千问VL 实现的超星学习通自动答题工具，支持可视化GUI操作、图片题目识别、自动选择答案并提交，专注于技术研究与学习交流场景。

## 📋 功能特点
- 🖥️ 可视化GUI界面：基于Tkinter构建，支持课程链接输入、静音模式选择，操作简单易上手
- 🌐 浏览器自动化：通过DrissionPage控制Chrome浏览器，自动访问学习通、定位题目、截图保存
- 🤖 AI智能答题：调用阿里云通义千问qwen3-vl-plus多模态模型，识别图片题目并返回精准答案
- 🎵 灵活配置：支持静音模式开关，适配不同使用场景的声音需求
- 📝 实时日志：GUI内实时显示彩色运行日志，便于查看进度和排查问题

## 🛠️ 运行环境
- Python 版本：3.10（推荐，3.8+版本可兼容）
- 浏览器：Google Chrome（需提前安装，DrissionPage依赖Chrome内核）
- 系统兼容：Windows（最佳体验）、macOS、Linux

## 🚀 安装步骤
### 1. 下载项目源码
直接下载项目压缩包

### 2. 安装依赖包
执行以下命令安装项目所需第三方依赖：
```bash
pip install -r requirements.txt
```

### 3. 配置通义千问API密钥
1. 注册并登录[阿里云通义千问控制台](https://dashscope.aliyuncs.com/)，完成实名认证后获取`API_KEY`（需开通qwen3-vl-plus模型调用权限）；
2. 打开项目中的`.env`文件，替换默认的`Qwen_API_KEY`：
   ```.env
   Qwen_API_KEY=你的阿里云通义千问API密钥
   ```

## 📖 使用方法
### 1. 启动程序
在项目根目录执行以下命令启动GUI程序：
```bash
python main.py
```

### 2. 界面操作流程
1. 在「输入课程链接」输入框中填写超星学习通课程章节链接（示例：`https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?courseid=256769914&clazzid=131228143&cpi=385745908&enc=8df8c8bd25aad2e628f36426603d16ac&t=1772804008136&pageHeader=0&v=2&hideHead=0`）；
2. 选择「是否静音」（默认开启静音模式，播放视频无声音）；
3. 点击「运行程序」按钮，工具会自动启动Chrome浏览器并执行以下操作：
   - 访问学习通课程页面
   - 定位章节任务点和视频题目
   - 截图题目并转换为Base64格式
   - 调用AI模型识别题目并获取答案
   - 自动选择答案并提交
4. 运行日志会实时显示在界面下方的文本框中，可查看每一步执行状态。

## ⚠️ 重要注意事项
1. **仅限学习使用**：本工具仅用于Python自动化、AI接口调用等技术研究，禁止用于刷课、违规答题等违反超星学习通用户协议的行为，违者后果自负；
2. **API密钥安全**：请勿将包含`API_KEY`的代码提交至公共代码仓库，生产环境建议使用`python-dotenv`加载环境变量；
3. **浏览器兼容性**：确保Chrome浏览器为最新版本，避免DrissionPage操作异常；
4. **目录权限**：确保项目根目录下的`自动下载题库`文件夹存在，工具会将题目截图保存至该目录；
5. **运行干扰**：程序运行期间请勿手动操作Chrome浏览器，避免打断自动化流程；
6. **网络要求**：需保证网络畅通，API调用依赖外网访问，国内用户建议使用稳定网络环境。

## 📄 许可证
本项目采用 MIT 开源许可证 - 详见项目根目录下的 [LICENSE](LICENSE) 文件。

## ❗ 免责声明
1. 本项目为开源学习项目，仅提供技术研究参考，不承担因使用本工具导致的账号封禁、违规处罚等任何责任；
2. 使用前请仔细阅读超星学习通用户协议及阿里云通义千问服务条款，遵守相关法律法规；
3. 作者不对工具的准确性、稳定性、可用性做任何承诺，使用风险由用户自行承担。

## 🙏 致谢
- [DrissionPage](https://github.com/g1879/DrissionPage)：轻量高效的Python浏览器自动化库
- [OpenAI Python SDK](https://github.com/openai/openai-python)：兼容通义千问API的客户端工具
- [通义千问](https://dashscope.aliyuncs.com/)：提供多模态大模型能力支持
- [Pillow](https://python-pillow.org/)：Python图像处理核心库

---