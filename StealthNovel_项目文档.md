# StealthNovel (Python) — 隐蔽小说阅读器

> 在 Windows 上，用 **任务栏标题** 或 **伪装成右下角广告弹窗** 的方式显示小说内容；支持 **→** 逐字、**↓** 逐行、全局热键；可从本地 TXT/粘贴板/URL 读取文本。

---

## 目录

- [功能概览](#功能概览)
- [显示模式](#显示模式)
- [系统限制 & 取舍](#系统限制--取舍)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [使用方法](#使用方法)
- [键位 & 全局热键](#键位--全局热键)
- [实现要点](#实现要点)
- [常见问题](#常见问题)
- [开发路线图](#开发路线图)
- [许可](#许可)

---

## 功能概览

- **两种隐蔽展示方式**
  - **任务栏标题模式**：持续更新主窗口标题（taskbar button text）以显示当前片段。
  - **伪装弹窗模式**：在右下角显示一个 **无边框、置顶、小卡片**，拟态「广告/系统提示」。

- **文本推进**
  - **→（右方向键）**：逐字推进。
  - **↓（下方向键）**：逐行推进。
  - **自动推进**（可选）：设定每 N 毫秒自动前进一个字符/一行。

- **文本来源**
  - 本地 `.txt` 文件（UTF-8）
  - 粘贴板
  - 远端 URL（支持直连纯文本）

- **进度保存**
  - 自动保存当前 **行号**、**字符索引**、**来源** 到本地 `config/state.json`。

- **外观（默认主题）**
  - **主色黑色**（文本/描边）
  - **背景淡绿**（卡片背景/高亮）
  - **辅色淡红**（强调/提示）

---

## 显示模式

### 1) 任务栏标题模式（TaskbarTitle）
- 应用保持一个小型窗口（可缩到 1×1 像素、靠屏幕角落），**持续更新窗口标题** 来承载当前文本切片；Windows 任务栏按钮将显示该标题。
- 优点：最隐蔽、无明显 UI。
- 缺点：**最小化后无法响应键盘**（Windows/前台焦点限制）；标题长度有限，超过将被省略。

### 2) 伪装弹窗模式（FakePopup）
- 在右下角显示一个 **无边框、圆角、半透明** 小卡片，样式拟态系统/广告提示；可设 **自动淡入淡出**。
- 优点：视觉可控，支持点击与悬停，**即使窗口很小也能获得焦点**。
- 缺点：相比标题模式更显眼；需要更谨慎的配色与动效。

> 可在运行时切换模式，或仅启用其一。

---

## 系统限制 & 取舍

- **键盘事件 & 最小化**：当窗口最小化或失去焦点时，普通按键事件无法到达。解决方案：
  - 使用 **全局热键**（`RegisterHotKey` via `pywin32` 或 `keyboard` 模块）来捕捉 **→/↓**（或自定义组合键）。
  - 或保持窗口尺寸极小、位于角落、置顶但透明度较低。

- **任务栏显示宽度**：任务栏按钮标题长度有限。采用 **滑动窗口**（marquee）策略，始终展示末尾的 N 个字符（如 40）。

- **安全与权限**：全局热键在某些环境需要以管理员运行。

---

## 技术栈

- GUI：**PySide6**（或 PyQt5）
- 全局热键：`keyboard`（或 `pywin32` 的 `RegisterHotKey`）
- 系统托盘：PySide6 `QSystemTrayIcon`
- 配置/状态：`json`（`config/*.json`）
- 文本加载：`requests`（URL），`pyperclip`（剪贴板，可选）
- 打包（可选）：**PyInstaller** 生成单文件 exe

---

## 快速开始

### 环境需求
- Windows 10/11
- Python 3.9+（建议 3.11）
- 建议以虚拟环境运行

```powershell
# 1) 克隆项目
git clone https://example.com/StealthNovel.git
cd StealthNovel

# 2) 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 3) 安装依赖
pip install -r requirements.txt

# 4) 运行
python -m stealthnovel
```

**`requirements.txt` 示例**
```
PySide6>=6.6
keyboard>=0.13
requests>=2.31
pyperclip>=1.8
pywin32>=306 ; platform_system == "Windows"
```

> 如果 `keyboard` 在你的环境需要管理员权限，请以管理员启动终端。

---

## 项目结构

```
stealthnovel/
├─ stealthnovel/
│  ├─ __init__.py
│  ├─ app.py                 # 程序入口，解析配置，初始化 UI 与热键
│  ├─ modes/
│  │  ├─ base.py             # 抽象基类：load/render/advance
│  │  ├─ taskbar_title.py    # 任务栏标题模式实现（更新窗口标题）
│  │  └─ fake_popup.py       # 伪装弹窗模式实现（右下角卡片）
│  ├─ core/
│  │  ├─ parser.py           # 文本解析、清洗、行切分
│  │  ├─ title_slice.py      # 滑动窗口/截断算法
│  │  ├─ state.py            # 行/字符索引、序列化/反序列化
│  │  └─ hotkeys.py          # 全局热键注册/注销
│  ├─ ui/
│  │  ├─ tray.py             # 系统托盘菜单（切换模式/加载文本/退出）
│  │  └─ theme.py            # 颜色与样式（黑/淡绿/淡红）
│  ├─ resources/
│  │  └─ icons/              # 托盘/窗口图标
│  └─ utils/
│     ├─ files.py            # 读取本地/URL/剪贴板
│     └─ logger.py
├─ config/
│  ├─ settings.json          # 全局设置（模式/窗口大小/热键/主题/自动推进等）
│  └─ state.json             # 运行时进度（自动生成）
├─ tests/
│  ├─ test_parser.py
│  ├─ test_title_slice.py
│  └─ test_state.py
├─ README.md
├─ LICENSE
└─ requirements.txt
```

---

## 配置说明

**`config/settings.json` 示例**
```json
{
  "mode": "TaskbarTitle",           
  "title_window": 40,               
  "auto_tick": false,               
  "auto_tick_interval_ms": 0,       
  "advance_by": "char",             
  "theme": {
    "text": "#000000",
    "bg": "#E6F4EA",
    "accent": "#F9D9D9",
    "opacity": 0.92
  },
  "hotkeys": {
    "next_char": "right",
    "next_line": "down",
    "toggle_mode": "ctrl+shift+m",
    "toggle_auto": "ctrl+shift+a",
    "reset_progress": "ctrl+shift+r"
  },
  "fake_popup": {
    "width": 360,
    "height": 120,
    "margin": 16,
    "rounded": 14,
    "shadow": true,
    "animate": true
  },
  "taskbar_title": {
    "min_window_size": [1, 1],
    "stick_to_corner": "bottom-left"
  },
  "source": {
    "type": "file",
    "path": "novel.txt",
    "url": ""
  }
}
```

**`config/state.json`（运行时自动生成/更新）**
```json
{
  "line_index": 0,
  "char_index": 0,
  "source_hash": "sha256:..."
}
```

---

## 使用方法

1. **准备文本**：确保为 UTF-8 编码的纯文本（`.txt`）。
2. **选择来源**：在 `config/settings.json` 设置 `source.type` 为 `file` / `clipboard` / `url`；对应填写 `path` 或 `url`。
3. **选择模式**：`mode` 设为 `TaskbarTitle` 或 `FakePopup`。
4. **运行程序**：`python -m stealthnovel`。
5. **键位推进**：按 **→** 逐字、按 **↓** 逐行。可用托盘菜单切换模式、加载新文本、开启/关闭自动推进。
6. **进度续读**：再次启动会从 `state.json` 自动恢复。

---

## 键位 & 全局热键

- **→**：下一字（默认全局热键）
- **↓**：下一行（默认全局热键）
- **Ctrl+Shift+M**：切换显示模式
- **Ctrl+Shift+A**：开/关自动推进
- **Ctrl+Shift+R**：重置进度

> 若与系统/其他软件冲突，请更改 `config/settings.json` 中的按键绑定。

---

## 实现要点

### 1) 标题切片（任务栏可读性）
```python
def to_title_slice(text: str, max_len: int = 40) -> str:
    if len(text) <= max_len:
        return text
    return "…" + text[-max_len:]
```

### 2) 推进逻辑
```python
def next_char(line_idx, char_idx, lines):
    if line_idx >= len(lines):
        return line_idx, char_idx
    if char_idx + 1 < len(lines[line_idx]):
        return line_idx, char_idx + 1
    return min(line_idx + 1, len(lines) - 1), 0

def next_line(line_idx, char_idx, lines):
    return min(line_idx + 1, len(lines) - 1), 0
```

### 3) 全局热键（keyboard）
```python
import keyboard

keyboard.add_hotkey('right', lambda: advance('char'))
keyboard.add_hotkey('down',  lambda: advance('line'))
```

### 4) PySide6 伪装弹窗（右下角）
- 创建 `FramelessWindow` + `Qt.Tool | Qt.WindowStaysOnTopHint`
- 放置到 `QScreen.availableGeometry()` 的右下角，减去 `margin`
- 使用 `QPropertyAnimation` 实现淡入/淡出或位移动画
- 使用样式（黑/淡绿/淡红），例如：

```python
w.setStyleSheet('''
  QWidget { 
    background: #E6F4EA; 
    color: #000; 
    border: 1px solid rgba(0,0,0,0.2); 
    border-radius: 14px; 
  }
  .accent { background: #F9D9D9; }
''')
```

### 5) 任务栏标题模式
- 维护一个不可最小化的小窗口；每次推进时：`window.setWindowTitle(to_title_slice(current_text))`
- 可将窗口尺寸置为 1×1，放于屏幕角落，降低视觉存在感。

### 6) 状态与持久化
- `state.json` 存储行/字符索引；在 `QApplication.aboutToQuit` 钩子中写回。
- 对来源文本计算 `sha256`，切换书源时重置进度。

---

## 常见问题

- **最小化后热键失效？**  
  常规按键事件确实无法触达。使用 **全局热键**（默认已启用），或勿最小化，只将窗口缩到极小且失焦。

- **标题被截断？**  
  受任务栏布局影响是正常现象。请减小 `title_window`，并使用 **滑动窗口** 策略。

- **需要管理员权限？**  
  某些环境下全局热键/键盘钩子需要管理员权限。若失败，请以管理员运行。

- **URL 无法加载？**  
  请确认是可直连的纯文本资源（`text/plain`），或下载为本地 `.txt` 使用。

---

## 开发路线图

- [ ] Marquee 跑马灯：在标题内定时横向滚动
- [ ] 章节/书架管理：多文件队列、进度分别保存
- [ ] 托盘搜索：快速跳转到关键字/章节
- [ ] Windows Toast 通知集成（`winrt`），可把片段投送为通知
- [ ] OCR 辅助：从截图提取文本（实验性）
- [ ] 打包发布脚本：PyInstaller + 版本资源 + 自动更新通道（可选）

---

## 许可

- 代码建议采用 **MIT** 许可证。
- 请确认小说文本版权，仅作个人学习与研究使用。

---

> **提示**：若你需要，我可以基于本文档直接生成 `PySide6` 可运行骨架（`TaskbarTitle`/`FakePopup` 两模式打通、全局热键、托盘菜单、状态持久化），并附 `PyInstaller` 打包配置。


---

## 项目部署与下载页面

本项目计划在提交到 **GitHub** 后，通过 **Vercel** 自动构建并部署为一个静态网站。  
未来会为该网站分配独立域名，申请谷歌Ads，所以要做好SEO。但暂时使用 Vercel 提供的临时子域名访问。  

用户可直接访问该网页，在其中：
- 查看项目简介、功能截图与更新日志；
- 下载最新版本的可执行程序（Windows `.exe`）与源代码压缩包；
- 了解如何使用命令行或配置文件进行个性化设置；
- 底部藏有作者联系方式，email为wanghongxiang23@gmail.com,X为@Rollkey4。 

页面将提供简洁的设计风格，以黑色为主、淡绿色背景、淡红色点缀，延续应用主题。
