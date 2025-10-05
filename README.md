# StealthNovel (Python) — 隐蔽小说阅读器

> 在 Windows 上，用 **任务栏标题** 或 **伪装成右下角广告弹窗** 的方式显示小说内容；支持 **→** 逐字、**↓** 逐行、全局热键；可从本地 TXT/粘贴板/URL 读取文本。

## 功能特性

- **两种隐蔽展示方式**
  - **任务栏标题模式**：持续更新主窗口标题以显示当前片段
  - **伪装弹窗模式**：在右下角显示小卡片，拟态「广告/系统提示」

- **文本推进**
  - **→（右方向键）**：逐字推进
  - **↓（下方向键）**：逐行推进
  - **自动推进**（可选）：设定定时自动前进

- **文本来源**
  - 本地 `.txt` 文件（UTF-8）
  - 粘贴板
  - 远端 URL

- **进度保存**
  - 自动保存当前阅读进度到本地

## 快速开始

### 环境需求
- Windows 10/11
- Python 3.9+

### 安装步骤

```powershell
# 1) 克隆项目
git clone https://github.com/yourusername/StealthNovel.git
cd StealthNovel

# 2) 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 3) 安装依赖
pip install -r requirements.txt

# 4) 运行
python -m stealthnovel
```

## 使用方法

1. **准备文本**：确保为 UTF-8 编码的纯文本（`.txt`）
2. **选择来源**：在 `config/settings.json` 设置文本来源
3. **选择模式**：设置显示模式为 `TaskbarTitle` 或 `FakePopup`
4. **运行程序**：`python -m stealthnovel`
5. **键位推进**：按 **→** 逐字、按 **↓** 逐行

## 键位说明

- **→**：下一字（全局热键）
- **↓**：下一行（全局热键）
- **Ctrl+Shift+M**：切换显示模式
- **Ctrl+Shift+A**：开/关自动推进
- **Ctrl+Shift+R**：重置进度

## 配置

编辑 `config/settings.json` 自定义各项设置，包括：
- 显示模式
- 热键绑定
- 主题颜色
- 窗口参数
- 文本来源

## 许可

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- Email: wanghongxiang23@gmail.com
- X (Twitter): @Rollkey4

