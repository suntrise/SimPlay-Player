<img width="32" height="32" align="left" style="float: left; margin: 0 10px 0 0;" alt="Simplay Player Logo" src="https://github.com/WhatDamon/Simplay-Player/blob/main/asset/simplay.png">  

# Simplay Player

> [!IMPORTANT]  
> WIP! 大部分功能还在开发中, 并且目前也存在着非常严重的恶性 BUG 需要修复, 基本处于勉勉强强可用的状态

这是一个 __闲得发慌时__ 开发出来的小作品, 而我动手做这玩意的原因是我周围的人大多都在写类似的项目

最早被称为 __Simply Player__ 即 __简单的播放器__, __Simplay__ 是在码字过程中意外中得到名字

支持 `MP3`、`M4A`、`FLAC`、`WAV`、`AAC` 格式 (已测试的所有格式中, `APE`、`MP2`、`WMA`、`OGG`有不同程度的不支持, 其他格式也有可能支持)

如果喜欢可以点个 Star, 当然目前我还是更希望各位可以为项目开发添砖加瓦, 多来点 PR

## 要求

__Python 3.8 及更高版本__, 推荐 3.10 及更高版本以保障其正常运行 (Action 中我们使用了 Python 3.11 进行编译测试)

开发使用前 __*nix系统__ 需要先执行...

~~~Bash
pip install -r requirements.txt
~~~

而 __Windows__ 则需要执行...

~~~Bash
pip install -r requirements_win.txt
~~~

___注：区分的原因是 `Windows-Toasts` 库只能在 Windows 下生效!___

此外, 该软件 __不能在含有 CJK 文本的路径下正常开发与运行__!

## TODO

- [x] 基本逻辑
- [x] 吐司通知 (Windows 独占性功能, 其它系统使用 `SnackBar` 替代)
- [x] 快进与倍速播放
- [x] GitHub Actions 自动测试编译工作流 (使用 __Nuitka__ 实现, 详见[本项目 Actions](https://github.com/WhatDamon/Simplay-Player/actions))
- [ ] 循环播放 (遇到技术性难题, 暂时注释了 `enableOrDisable` 函数 (函数临时被注释), 预留了占位按钮 `playInLoop_btn` (组件已隐藏) 和状态变量 `loopOpen`)
- [ ] 设置 (目前已有占位按钮 `settings_btn`, 并隐藏)
- [ ] 歌词显示与滚动 (已预留了歌词路径变量 `lyricFile` 和读取函数 `lyricExistAndRead`(函数临时被注释))
- [ ] 歌单 (施工中)
- [ ] 日志输出
- [ ] 系统托盘 (预计使用 `pystray` 实现)
- [ ] 检查更新 (基于 __Github API__)
- [ ] 界面自动取色
- [ ] 混音器
- [ ] 在线获取歌曲 (__网易云__) (目前已有占位菜单按钮, 但代码还没开写)

## BUG 列表

以下内容不一定完全, 可能存在更多不在这个列表的 BUG!

- [x] 打开歌曲后需要连续点击三次播放键才可以进入播放状态 (通过调整代码逻辑修复)
- [ ] 读取存在封面的歌曲后再打开无封面歌曲不会替换成占位的 `track.png`
- [ ] 隐藏顶栏或者 `Ctrl` + `H` 快捷键等操作以后后歌曲进度条无法工作, 并无法彻底关闭软件
- [ ] 加载歌曲或更换歌曲后前可能会有些不是特别影响的报错
- [ ] 窗口标题有时不能按希望的方式显示 (实际解决很简单, 但是我希望能够整合一下)

## 急切的任务

- [ ] 代码整理与注释, 功能分单独代码文件

## 使用到的第三方项目

- [flet](https://github.com/flet-dev/flet) (Apache-2.0 license)
- [TinyTag](https://github.com/devsnd/tinytag) (MIT license)
- [Windows-Toasts](https://github.com/DatGuy1/Windows-Toasts) (Apache-2.0 license)