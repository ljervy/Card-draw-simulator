# 小紫爱抽卡

## 项目简介
小紫爱抽卡是一个基于 Python 和 Tkinter 的抽卡模拟器。用户可以进行单抽、十连抽，并查看抽卡统计数据和图鉴。项目支持保存和加载抽卡统计数据。

## 功能特点
- **单抽**：模拟一次抽卡。
- **十连抽**：模拟十次连续抽卡。
- **统计数据**：显示抽卡总次数、平均传奇抽数、抽中传奇概率等。
- **图鉴**：查看所有抽卡物品及其稀有度。
- **重置统计**：清空所有统计数据。

## 环境要求
- Python 3.8 或更高版本
- 必要的依赖库：
  - `tkinter`
  - `Pillow`
  - `PyInstaller`

## 文件结构
- `xiaozi_gui.py`：主程序文件，包含 GUI 界面逻辑。
- `xiaozi_game.py`：抽卡逻辑和数据处理。
- `package_script.py`：用于打包程序的脚本。
- `uninstall.js`：清理打包生成的文件。
- `.vscode/tasks.json`：VS Code 的任务配置文件。

## 使用说明

### 运行程序
1. 确保已安装 Python 和必要的依赖库。
2. 在终端中运行以下命令启动程序：
   ```bash
   python xiaozi_gui.py
   ```

### 打包程序
1. 使用 VS Code 打开项目目录。
2. 在 VS Code 的任务面板中选择 `run build script` 任务。
3. 任务会调用 `package_script.py`，使用 PyInstaller 打包程序为单个可执行文件。

### 清理打包文件
1. 在 VS Code 的任务面板中选择 `uninstall` 任务。
2. 任务会调用 `uninstall.js`，删除 `build` 和 `dist` 目录。

## 注意事项
- 打包时需要确保 `background.png` 和 `xiaozi.ico` 文件存在于项目目录中。
- 打包后的可执行文件会包含所有必要的资源，用户无需额外配置。

## 贡献
欢迎提交问题和建议，帮助改进项目！