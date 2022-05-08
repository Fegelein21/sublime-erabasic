# Sublime-EraBasic
这是一款在 [Sublime Text 3](http://www.sublimetext.com/) 上为 EraBasic 语言提供语法高亮、全关键字提示、自动补全、跳转定义功能的语法插件包。

插件包中的语法和关键字参照于 [Emuera Wiki](https://osdn.net/projects/emuera/wiki/FrontPage)。

## 安装
方式1：通过 `Package Control: Install Package` 指令找到 `EraBasic` 插件并订阅。

方式2：在此下载安装:
1. 把当前项目文件下载到本地。
2. 打开Sublime，点选菜单栏上的 `首选项 -> 浏览插件目录`。
3. 把下载的压缩包中的文件夹解压到插件目录中，重命名文件夹为 `EraBasic`。

## 使用

### 语法高亮
![highlighting](https://z3.ax1x.com/2021/11/23/opIT56.png)


### 全关键字提示
![full_keyword](https://z3.ax1x.com/2021/11/23/opIHPK.gif)


### 自动补全
![auto_complete](https://z3.ax1x.com/2020/12/07/DxT4iQ.gif)


### 跳转到定义
![goto_definition](https://z3.ax1x.com/2021/11/23/opIq2D.gif)


## Ctags扩展功能
本插件还支持通过Ctags提取关键字以实现自定义函数、全局变量、宏定义的提示和跳转

**使用前请确保您的Sublime处于项目环境**

![ctags](https://z3.ax1x.com/2021/11/23/opIb8O.gif)


### 准备工作
- 在Sublime中订阅 `CTags` 插件。
- 下载 [Universal Ctags](https://github.com/universal-ctags/ctags)，把压缩包中的 `ctags.exe` 程序解压到 `C:\Windows\System32` 目录下。

#### 对于订阅插件的用户：
- 打开Sublime，点选菜单栏上的 `首选项 -> 浏览插件目录`，在打开的文件窗口中上移到 `Sublime Text 3` 目录并进入 `Installed Packages` 文件夹。
- 以压缩包方式打开 `EraBasic.sublime-package` 文件，把压缩包中的 `ctags.d` 文件夹解压到 `C:\Users(用户)\(你的计算机用户名)` 目录下即可。

#### 对于手动安装插件的用户：
- 打开Sublime的插件目录，把EraBasic插件文件夹中的 `ctags.d` 文件夹复制或移动到 `C:\Users(用户)\(你的计算机用户名)` 目录下即可。

### 使用
1. 在左侧的文件窗口中 `鼠标右键` 点选最顶层的ERB文件夹，点选 `Ctags: Rebuild Tags`，等待Ctags插件提取关键字。
2. 提取完毕后会在ERB文件夹下生成 `.tags` 和 `.tags_sorted_by_file` 两个文件。
3. 对代码中的函数、全局变量、宏定义使用 `Ctrl + 鼠标左键` 可快速跳转到定义，再使用 `Ctrl + 鼠标右键` 跳回到之前的光标位置。
4. 每当您在代码中添加或移除了函数、全局变量、宏定义时，记得再次 `Rebuild Tags`（重复步骤1即可）。
