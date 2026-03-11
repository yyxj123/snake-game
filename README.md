# 🐍 Super Snake - 超级贪吃蛇

一个美观、功能丰富的贪吃蛇游戏，使用 Python + Pygame 开发。

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 特性

- 🎮 **流畅的游戏体验** - 60 FPS 流畅运行
- 🎨 **精美的视觉效果** - 现代渐变配色、粒子特效
- 🔊 **音效系统** - eat、gameover、button点击音效
- 🏆 **计分系统** - 实时分数、最高分记录
- 🌙 **暗色主题** - 护眼的深色界面
- ⌨️ **快捷键支持** - WASD 或方向键控制
- 📊 **排行榜** - 本地最高分记录

## 🖼️ 游戏截图

```
┌─────────────────────────────┐
│  🐍 SUPER SNAKE           │
│  Score: 0  |  Best: 100   │
├─────────────────────────────┤
│                             │
│    ████  ← 蛇头           │
│    ████ ████  ← 蛇身      │
│         ████               │
│                             │
│         ⭐ ← 食物          │
│                             │
│  [SPACE] 暂停  [ESC] 退出  │
└─────────────────────────────┘
```

## 📦 安装

### 1. 安装 Python

需要 Python 3.8 或更高版本。

```bash
# 检查 Python 版本
python3 --version
```

如果未安装，请到 [python.org](https://www.python.org/downloads/) 下载。

### 2. 安装依赖

```bash
# 克隆或下载项目后，进入目录
cd snake-game

# 安装 pygame
pip install pygame
```

### 3. 运行游戏

```bash
python main.py
```

## 🎮 操作说明

| 按键 | 功能 |
|------|------|
| ↑ / W | 向上移动 |
| ↓ / S | 向下移动 |
| ← / A | 向左移动 |
| → / D | 向右移动 |
| Space | 暂停/继续 |
| ESC | 退出游戏 |
| Enter | 开始游戏/重新开始 |

## 🎯 游戏规则

1. 使用方向键或 WASD 控制蛇的移动
2. 吃到食物得分，蛇身变长
3. 撞到墙壁或自己的身体则游戏结束
4. 吃到特殊食物获得额外分数
5. 速度会随着分数增加而略微加快

## 📁 项目结构

```
snake-game/
├── main.py           # 游戏主入口
├── snake/            # 游戏核心代码
│   ├── __init__.py
│   ├── game.py      # 游戏主逻辑
│   ├── snake.py     # 蛇类
│   ├── food.py      # 食物类
│   ├── particle.py  # 粒子特效
│   └── sound.py     # 音效管理
├── assets/          # 资源文件
│   ├── sounds/      # 音效文件
│   └── fonts/       # 字体文件
├── requirements.txt # Python依赖
└── README.md        # 说明文档
```

## 🛠️ 打包发布

### Windows (.exe)

```bash
# 安装 pyinstaller
pip install pyinstaller

# 打包
pyinstaller --name="SuperSnake" --windowed --onefile main.py
```

### macOS (.app / .dmg)

```bash
# 安装 pyinstaller
pip install pyinstaller

# 打包为 app
pyinstaller --name="SuperSnake" --windowed --onefile main.py

# 转换为 dmg（需要安装 create-dmg）
create-dmg "dist/SuperSnake.app"
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License - 自由使用、修改和分发。

---

Made with ❤️ by 小吴虾 🦐
