# lolskin-gui

使用pyqt5实现的lol换肤面板gui（在此只研究了gui的实现以及理论上dll注入和移除的实现，未涉及真实换肤功能），希望各位作者能借鉴此风格，此项目较为简陋，在此抛砖引玉。

<img src="assets\lolskin-gui.png" style="zoom:67%;" />

## 特点

- 优美的gui界面
- 醒目的功能布局

## 先决条件

- Python 3.8+
- 虚拟环境（推荐）

## 部署

1. 克隆存储库
2. 创建并激活虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. 安装依赖项：

```bash
pip install -r requirements.txt
```

## 运行应用程序

直接运行main.py即可

## 打包exe

使用pyinstaller进行打包，命令如下（无命令行以及设置图标），main.sepc为打包的配置文件。以下为示例命令，具体打包的图标需要指明本地图片路径和配置main.sepc内的图片路径。

```bash
pyinstaller -F -w -i logo.ico main.py
```

## 贡献

1. 分叉存储库
2. 创建特征分支
3. 提交你的更改
4. 推到分支
5. 创建新的Pull Request

## 许可证

该项目根据MIT许可证获得许可。
