# Sublime-EraBasic
这是一款在 [Sublime Text 3](http://www.sublimetext.com/) 上为 EraBasic 语言提供语法高亮、全关键字提示、自动补全、跳转定义功能的语法插件包。
插件包中的语法和关键字参照于 [Emuera Wiki](https://osdn.net/projects/emuera/wiki/FrontPage)。

## 安装
方式1：通过 `Package Control: Install Package` 指令找到 `EraBasic` 插件并订阅

方式2：在此下载安装:
1. 把当前项目文件下载到本地
2. 打开Sublime Text 3，点击菜单栏上的 `首选项 -> 浏览插件目录`
3. 在插件目录中新建一个名为 `EraBasic` 的文件夹，把下载的压缩包文件解压到文件夹中即可

## 使用

### 语法高亮
![](example_highlighting.png)


### 全关键字提示
![](example_full_keyword.gif)


### 自动补全
![](example_auto_complete.gif)


### 跳转到定义
![](example_goto_definition.gif)


**注意，跨文件跳转定义需要在项目环境下才能生效:**
1. 点击菜单栏上的 `项目 -> 添加文件夹到项目`
2. 在弹出的选择文件夹窗口中选择最顶层的 `ERB` 文件夹
3. 保存创建好的项目，`项目 -> 项目另存为...`，将 `文件名.sublime-project` 文件保存在适当位置(建议与ERB文件夹同级)
4. 下次打开时，点选 `项目 -> 快速切换项目` 以快速选择，或者点选 `项目 -> 开启项目...` 并选择已保存的 `文件名.sublime-project` 文件即可

## Ctags扩展功能
本插件还支持通过Ctags提取关键字以实现自定义函数、全局变量、宏定义跳转及关键字提示

**使用前请确保您的Sublime处于项目环境，并在Sublime中订阅 `CTags` 插件**

![](example_ctags.gif)


### 准备工作
1. 前往 [Exuberant Ctags](http://ctags.sourceforge.net/) 官网下载Ctags（下载按钮位于官网左侧栏的`Download - Releases`）
2. 打开下载到的 `ctags58.zip` 压缩包，把压缩包中的 `ctags.exe` 程序解压到 `C:\Windows\System32` 中
4. 打开Sublime的插件目录，找到 `EraBasic` 文件夹
5. 找到文件夹中的`.ctags` 文件，将其复制或移动到 `C:\Users(用户)\(你的计算机用户名)` 中即可

### 使用
1. 在左侧的文件窗口中 鼠标右键 点选最顶层的ERB文件夹，点选 `Ctags: Rebuild Tags`，等待Ctags插件提取关键字
2. 提取完毕后会在ERB文件夹下生成 `.tags` 和 `.tags_sorted_by_file` 两个文件
3. 对代码中的函数，全局变量使用 `Ctrl + 鼠标左键` 查看是否能成功跳转，再使用 `Ctrl + 鼠标右键` 跳回到之前的光标位置
4. 每当您在代码中添加或移除了函数、全局变量、宏定义时，记得再次 `Rebuild Tags`（重复步骤1即可）
