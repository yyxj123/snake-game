#!/bin/bash
# 打包脚本 - 构建 exe 和 dmg 文件

echo "🐍 Super Snake 打包脚本"
echo "========================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

echo "📦 安装依赖..."
pip install pygame pyinstaller

# 创建 dist 目录
mkdir -p dist

# ===== Windows 打包 =====
echo ""
echo "🏗️ 打包 Windows 版本 (.exe)..."

# Windows 打包
pyinstaller --name="SuperSnake-Windows" \
    --windowed \
    --onefile \
    --add-data=".:." \
    --clean \
    main.py

if [ -f "dist/SuperSnake-Windows.exe" ]; then
    echo "✅ Windows 版本打包成功: dist/SuperSnake-Windows.exe"
else
    echo "❌ Windows 打包失败"
fi

# ===== macOS 打包 =====
echo ""
echo "🏗️ 打包 macOS 版本 (.app)..."

# macOS 打包
pyinstaller --name="SuperSnake-macOS" \
    --windowed \
    --onefile \
    --add-data=".:." \
    --clean \
    --osx-bundle-identifier="com.supersnake.app" \
    main.py

if [ -f "dist/SuperSnake-macOS" ]; then
    echo "✅ macOS 版本打包成功: dist/SuperSnake-macOS"
    
    # 尝试创建 dmg（如果安装了 create-dmg）
    if command -v create-dmg &> /dev/null; then
        echo "📦 创建 DMG 镜像..."
        create-dmg "dist/SuperSnake-macOS.app" --volname "SuperSnake"
        if [ -f "dist/SuperSnake-macOS.dmg" ]; then
            echo "✅ DMG 镜像创建成功: dist/SuperSnake-macOS.dmg"
        fi
    else
        echo "ℹ️  未安装 create-dmg，跳过 DMG 创建"
        echo "   安装方法: brew install create-dmg"
    fi
else
    echo "❌ macOS 打包失败"
fi

echo ""
echo "========================"
echo "🎉 打包完成！"
echo ""
echo "输出文件:"
ls -lh dist/
