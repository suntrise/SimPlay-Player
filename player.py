import flet as ft
import platform, os, time

from lib import cfg
cfg.loadConfig()

from lib import work, log_init, update, platform_check
log_init.logging.info("Basic libs imported at player.py")

from i18n import lang
log_init.logging.info("Languages imported at player.py")

ver = "2.0.0_pre2"
audioFile = None
lyricFile = ""
audioListShown = False
firstPlay = True
audioLoaded = None
toastImportError = False
currentDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentDir)

log_init.logging.info("Variable initialization complete at player.py")

page = ft.Page

def main(page):
    page.window_left = 200
    page.window_top = 100
    page.window_height = 600
    page.window_width = 800
    page.window_min_height = 360
    page.window_min_width = 540
    page.padding = 10
    page.title = "Simplay Player"
    page.window.center()
    # page.window_title_bar_hidden = True
    log_init.logging.info("Window created")

    if cfg.cfgData["appearances"][0]["mode"] == "sys":
        page.theme_mode = ft.ThemeMode.SYSTEM
    elif cfg.cfgData["appearances"][0]["mode"] == "light":
        page.theme_mode = ft.ThemeMode.LIGHT
    elif cfg.cfgData["appearances"][0]["mode"] == "dark":
        page.theme_mode = ft.ThemeMode.DARK

    if cfg.cfgData["appearances"][0]["rtl"] == True:
        page.rtl = True
    else:
        page.rtl = False

    page.theme = ft.Theme(color_scheme_seed = ft.Colors.BLUE)
    if lang.langInfo["font"] == "":
        page.fonts = {"Inter": "./asset/Inter.ttc"}
        page.theme = ft.Theme(font_family = "Inter")
    else:
        if platform_check.currentOS == "windows":
            page.theme = ft.Theme(font_family = lang.langInfo["font"][0]["windows"])
        elif platform_check.currentOS == "darwin":
            page.theme = ft.Theme(font_family = lang.langInfo["font"][0]["macos"])
        else:
            page.theme = ft.Theme(font_family = lang.langInfo["font"][0]["linux"])
    log_init.logging.info("Assets loaded")

    # 快捷键
    def keyboardEventTrack(e: ft.KeyboardEvent):
        log_init.logging.info("Keyboard event")
        if f"{e.key}" == " ":
            playOrPauseMusic(0)  
            log_init.logging.info("Press space bar to play/pause audio")
        if f"{e.ctrl}" == "True" and f"{e.key}" == "H":
            hideShowMenuBar(0)           
            log_init.logging.info("Press Ctrl-H to hide/show menu bar")

    page.on_keyboard_event = keyboardEventTrack
    log_init.logging.info("keyboardEventTrack loaded")

    def windowEvent(e):
        if e.data == "close":
            closeWindow(0)

    page.window_prevent_close = True
    page.on_window_event = windowEvent
    log_init.logging.info("windowEvent loaded")

    def closeWindow(e):
        page.window_destroy()
        log_init.logging.info("Window destoryed")

    def hideShowMenuBar(e):
        if menuBar.visible == True:
            menuBar.visible = False
            log_init.logging.info("Made menu bar disappeared")
            '''
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["resetMenuBar"]))
            page.snack_bar.open = True
            log_init.logging.info("Snack Bar loaded - resetMenuBar")
            '''
        elif menuBar.visible == False:
            menuBar.visible = True
            log_init.logging.info("Made menu bar shown")
        page.update()
        log_init.logging.info("Page updated")

    def alwaysOnTop(e):
        if page.window_always_on_top == False:
            page.window_always_on_top = True
            windowOnTop_btn.icon = ft.Icons.PUSH_PIN
            windowOnTop_btn.tooltip = lang.tooltips["cancelAlwaysOnTop"]
            '''
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenTop"]))
            page.snack_bar.open = True
            '''
        elif page.window_always_on_top == True:
            page.window_always_on_top = False
            windowOnTop_btn.icon = ft.Icons.PUSH_PIN_OUTLINED
            windowOnTop_btn.tooltip = lang.tooltips["alwaysOnTop"]
            '''
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenUntop"]))
            page.snack_bar.open = True
            '''
        page.update()
        log_init.logging.info("Page updated")
    
    def windowsToastNotify():
        toaster = WindowsToaster('Simplay Player')
        sysToast = Toast()
        if os.path.exists("./asset/simplay.png"):
            log_init.logging.info("./asset/simplay.png exist")
            sysToast.AddImage(ToastDisplayImage.fromPath('./asset/simplay.png'))
            log_init.logging.info("Toast image loaded")
        else:
            log_init.logging.warning("Cannot load toast image")
        sysToast.text_fields = [lang.mainMenu["songLoaded"], work.audioArtistText + " - " + work.audioTitleText]
        toaster.show_toast(sysToast)
        log_init.logging.info("Toast Notify")

    def pickFileResult(e: ft.FilePickerResultEvent):
        global audioPathTemp
        audioPathTemp = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else None
        )
        if audioPathTemp == None:
            log_init.logging.warning("Nothing Loaded")
            pass
        else:
            songlist_tiles.controls.append(audioTile(audioPathTemp))
            readSong(audioPathTemp)

    def readSong(audioPathTemp):
        global audioFile, lyricFile, firstPlay, getReturn
        page.splash = ft.ProgressBar()
        log_init.logging.info("Splash progress bar enabled")
        page.update()
        log_init.logging.info("Page updated")
        getReturn = False  
        audioFile = audioPathTemp
        lyricFile = ''.join(audioPathTemp.split('.')[:-1]) + ".lrc"
        lyrics_before.value = ""
        lyrics_text.value = ""
        lyrics_after.value = ""
        log_init.logging.info("File path loaded")
        log_init.logging.info("Audio path: " + audioFile)
        log_init.logging.info("Lyric path: " + lyricFile)
        if firstPlay == True:
            page.overlay.append(work.playAudio)
            log_init.logging.info("Append playAudio")
            firstPlay = False
        audioPathTemp = None
        audioInfoUpdate()
        page.title = work.audioArtistText + " - " + audioTitleText + " | Simplay Player"
        log_init.logging.info("Window title changed")
        if platform_check.currentOS == 'windows' and toastImportError == False:
            windowsToastNotify()
            log_init.logging.info("Load Windows toast")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["songLoaded"] + "\n" + audioArtistText+ " - " + audioTitleText))
            page.snack_bar.open = True
            log_init.logging.info("Snack Bar loaded - resetMenuBar")
        page.splash = None
        log_init.logging.info("Splash progress bar disabled")
        page.update()
        log_init.logging.info("Page updated")
        log_init.logging.info("File picked")
        if work.audioState == True:
            playOrPauseMusic(0)
        if cfg.cfgData["play"][0]["immediatelyPlay"] == True:
            global audioLoaded
            while(True):
                time.sleep(0.001)
                if audioLoaded == True:
                    playOrPauseMusic(0)
                    audioLoaded = False
                    break
    
    def loadAudio(e):
        global audioLoaded, audioFile, audioArtistText, audioTitleText
        audioLoaded = True
        log_init.logging.info("Audio loaded: " + audioFile + " => " + audioArtistText + " - " + audioTitleText)

    def pickFolderResult(e: ft.FilePickerResultEvent):
        allowed_extensions = ['mp3']
        songList = []
        songlistPathTemp = e.path if e.path else None
        if songlistPathTemp != None:
            for root, dirs, files in os.walk(songlistPathTemp):
                for f in files:
                    if f.split('.')[-1] in allowed_extensions:
                        file_path = os.path.join(root, f)
                        songList.append(file_path)
            readSong(songList[0])
            songListTiles(songList)
        
    pickFilesDialog = ft.FilePicker(on_result = pickFileResult)
    log_init.logging.info("Append pickFilesDialog")  
    pickSonglistDialog = ft.FilePicker(on_result = pickFolderResult) 
    page.overlay.extend([pickFilesDialog, pickSonglistDialog])

    # 本地音频信息更新
    def audioInfoUpdate():
        work.audioInfoUpdate(audioFile)
        audioCover.src_base64 = work.audioCoverBase64
        audioCover.src = work.audioCover_src
        audioTitle.value = work.audioTitleText
        if work.audioAlbumText != None:
            audioArtistAndAlbum.value = work.audioArtistText + " · " + work.audioAlbumText
        else:
            audioArtistAndAlbum.value = work.audioArtistText
        audioCover.update()
        onlineAudioSign.visible = False
        page.update()

    # 网络音频信息更新
    def audioFromUrlInfo(e):
        global audioFile, lyricFile, getReturn, firstPlay
        songID_text = songID_input.value
        songID = songID_text
        getReturn = work.audioFromUrlInfo(songID)
        if getReturn == True:
            if firstPlay == True:
                page.overlay.append(work.playAudio)
                log_init.logging.info("Append playAudio")
                firstPlay = False
            audioFile = work.audioUrl
            lyricFile = ""
            audioCover.src_base64 = ""
            audioCover.src = work.audioCover_src
            audioTitle.value = work.audioTitleText
            if work.audioAlbumText != None:
                audioArtistAndAlbum.value = work.audioArtistText + " · " + work.audioAlbumText
            else:
                audioArtistAndAlbum.value = work.audioArtistText
            songID_input.error_text = ""
            audioCover.update()
            lyricUrlRead(songID)
            onlineAudioSign.visible = True
            closeSongWeb_dlg(e)
            if work.audioState == True:
                playOrPauseMusic(0)
            if cfg.cfgData["play"][0]["immediatelyPlay"] == True:
                global audioLoaded
                while(True):
                    time.sleep(0.001)
                    if audioLoaded == True:
                        playOrPauseMusic(0)
                        audioLoaded = False
                        break
        elif getReturn == "vipSongOrNoCopyright":
            songID_input.error_text = lang.dialog["vipOrNoCopyrightAlert"]
        elif getReturn == False:
            songID_input.error_text = lang.dialog["errorPrompt"]
        page.update()

    # 播放列表类
    class audioTile(ft.Container):                                # ft.UserControl已经被废弃, 现在程序无法工作估计就是它的原因了
        def __init__(self, song):
            super().__init__()
            self.song = song
            self.songName = song.split('\\')[-1]

        def playSong(self,e):
            readSong(self.song)
            playOrPauseMusic(e)
            self.update()

        def build(self):
            return ft.Row(controls = [
                        ft.Icon(name = ft.Icons.MUSIC_NOTE_OUTLINED),
                        ft.Text(self.songName, width = 200),
                        ft.IconButton(icon = ft.Icons.PLAY_CIRCLE_FILLED_OUTLINED, on_click = self.playSong)
                    ],
                    width = 300
                )
        
    def songListTiles(songList):
        for song in songList:
            songlist_tiles.controls.append(audioTile(song))

    # 本地歌词读取    
    def lyricExistAndRead():
        if os.path.exists(lyricFile):
            work.lyricRead(lyricFile)
            lyrics_before.value = work.lyricsBefore
            lyrics_text.value = work.lyricsText
            lyrics_after.value = work.lyricsAfter
        else:
            pass
    
    # 网络歌词读取
    def lyricUrlRead(songID):
        readRes = work.lyricUrlRead(songID)
        if readRes == True:
            lyrics_before.value = work.lyricsBefore
            lyrics_text.value = work.lyricsText
            lyrics_after.value = work.lyricsAfter
        if readRes == False:
            lyrics_before.value = ""
            lyrics_text.value = ""
            lyrics_after.value = ""
    
    # 网络歌词处理（主要部分在work.py）
    def lyricsProcess():
        work.lyricsProcess()
        lyrics_before.value = work.lyricsBefore
        lyrics_text.value = work.lyricsText
        lyrics_after.value = work.lyricsAfter

    # 歌词显示/隐藏
    def lyricShow(e):
        if lyrics_text.visible == True:
            lyrics_before.visible = False
            lyrics_text.visible = False
            lyrics_after.visible = False
            lyrics_btn.icon = ft.Icons.LYRICS_OUTLINED
        elif lyrics_text.visible == False:
            lyrics_before.visible = True
            lyrics_text.visible = True
            lyrics_after.visible = True
            lyrics_btn.icon = ft.Icons.LYRICS
        page.update()

    def ctrlRowUpdate():
        playPause_btn.icon = work.playPause_btn_icon
        page.title = work.page_title
  
    # 歌曲播放/暂停
    def playOrPauseMusic(e):
        if audioFile != None:
            work.playOrPauseMusic(audioFile)
            ctrlRowUpdate()
        page.update()
    
    def autoStopKeepAudioProgress(e):
        work.autoStopKeepAudioProgress
        page.update()

    def autoKeepAudioProgress(e):
        work.autoKeepAudioProgress(e)
        audioProgressBar.value = work.audioProgressBar_value
        audioProgressStatus.value = work.audioProgressStatus_value
        if lyricFile != "":
            lyricExistAndRead()
        elif getReturn == True:
            lyricsProcess()
        if work.audioStateType == "completed":
            work.resetPlay()
            ctrlRowUpdate()
        page.update()

    def progressCtrl(e):
        work.progressCtrl(audioProgressBar.value)     
        page.update()

    # 单曲循环设置
    def enableOrDisableRepeat(e):
        work.enableOrDisableRepeat(e)
        if work.loopOpen == False:
            playInRepeat_btn.icon = ft.Icons.REPEAT_ONE_OUTLINED
        elif work.loopOpen == True:
            playInRepeat_btn.icon = ft.Icons.REPEAT_ONE_ON_OUTLINED
        page.update()
        log_init.logging.info("Page updated")
    
    # 打开音量面板
    def openVolumePanel(e):
        if volume_panel.visible == True:
            volume_panel.visible = False
            log_init.logging.info("Volume panel not visiable")
        elif volume_panel.visible == False:
            volume_panel.visible = True
            log_init.logging.info("Volume panel visiable")
        page.update()
        log_init.logging.info("Page updated")

    # 改变音量
    def volumeChange(e):
        work.volumeChange(volume_silder.value)
        volume_btn.icon = work.volume_btn
        page.update()

    # 播放列表
    def audioListCtrl(e):
        if audioListShown == False:
            showAudioList(0)
        elif audioListShown == True:
            hideAudioList(0)

    def showAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(0, 0)
        audioListShown = True
        log_init.logging.info("Audio list shown")
        audioList_menu.update()
        log_init.logging.info("audioList_menu updated")

    def hideAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(-2, 0)
        audioListShown = False
        log_init.logging.info("Audio list disappeared")
        audioList_menu.update()
        log_init.logging.info("audioList_menu updated")
   
    # 关闭窗口
    def closeSongWeb_dlg(e):
        songWeb_dlg.open = False
        page.update()

    songID_hint = ft.Text(value=lang.dialog["songIdHint"]) 
    songID_input = ft.TextField(label = "", error_text = "", autofocus = True, on_submit = audioFromUrlInfo)
    songWeb_dlg = ft.AlertDialog(
        adaptive = True,
        title = ft.Text(value = lang.dialog["songIdInput"]),
        content = ft.Column(
                controls = [
                    songID_hint,
                    songID_input
                ],
                height = 100,
                width = 400
            ),
            actions = [
                ft.TextButton(text = lang.dialog["cancel"], icon = ft.Icons.CLOSE_OUTLINED, on_click = closeSongWeb_dlg),
                ft.FilledButton(text = lang.dialog["ok"], icon = ft.Icons.CHECK_OUTLINED, on_click = audioFromUrlInfo)
            ],
            actions_alignment = ft.MainAxisAlignment.END
        )

    def getSongFromWebsite(e):
        page.dialog = songWeb_dlg
        songWeb_dlg.open = True
        log_init.logging.info("Dialog songWeb_dlg opened")
        page.update()
        log_init.logging.info("Page updated")

    # 媒体信息
    def openAudioInfoDlg(e):
        audioInfo_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["moreInfo"]),
            content = ft.Text(value = work.audioInfo, size = 10)
        )
        page.dialog = audioInfo_dlg
        audioInfo_dlg.open = True
        log_init.logging.info("Dialog audioInfo_dlg opened")
        page.update()
        log_init.logging.info("Page updated")
    
    # 检查更新
    def checkForUpdate(e):
        def closeFindUpdDlg(e):
            findUpd_dlg.open = False
            page.update()
            log_init.logging.info("Dialog findUpd_dlg closed")
        global ver
        content = update.update(ver)
        if content == "ERR":
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.dialog["updateTimeout"]))
            page.snack_bar.open = True
            page.update()
            log_init.logging.info("Snack Bar loaded - updateTimeout")
        elif content == "NUL":
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.dialog["youAreUsingLatest"]))
            page.snack_bar.open = True
            log_init.logging.info("Snack Bar pop-up(VLT)")
            page.update()
        else:
            downloadUrl = update.get_link()
            # 定义“发现更新”窗口
            findUpd_dlg = ft.AlertDialog(
                title = ft.Text(value = lang.dialog["findUpdate"]),
                content = ft.Column(controls = [ft.Markdown(content, selectable = True)], scroll = ft.ScrollMode.AUTO, width = 450),
                actions = [
                    ft.Row(controls = [
                        ft.TextButton(
                            text = lang.dialog["cancel"],
                            icon = ft.Icons.CLOSE_OUTLINED,
                            on_click = closeFindUpdDlg
                        ),
                        ft.FilledButton(
                            text = lang.dialog["update"],
                            icon = ft.Icons.UPLOAD_OUTLINED,
                            url = downloadUrl
                        )
                    ],
                    alignment = ft.MainAxisAlignment.END
                    )
                ],
            )
            page.dialog = findUpd_dlg  # 打开“发现更新”窗口
            findUpd_dlg.open = True
            page.update()
            log_init.logging.info("Dialog findUpd_dlg opened")

    # 关于信息
    def openAboutDlg(e):
        about_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["about"]),
            content = ft.Markdown("__Simplay Player__\n\rMaintained by suntrise & open source community\n\rFormally by WhatDamon\n\r- Version: " + ver + "\n\r- Powered by: Flet, Tinytag\n\r- Python: " + platform.python_version() + "\n\r- OS: " + platform.platform() + "-" + platform.machine(), selectable = True),
            actions = [
                ft.Row(controls = [
                    ft.TextButton(
                        text = lang.dialog["githubRepo"],
                        icon = ft.Icons.COLLECTIONS_BOOKMARK_OUTLINED,
                        url = "https://github.com/suntrise/Simplay-Player/"
                    )
                ],
                alignment = ft.MainAxisAlignment.END
                )
            ]
        )
        page.dialog = about_dlg
        about_dlg.open = True
        log_init.logging.info("Dialog about_dlg opened")
        page.update()
        log_init.logging.info("Page updated")

    def displaySettings(e):
        page.views.append(settingsPage.settings_pageView)
        page.go("/settings")
        log_init.logging.info("Set to page: settings")
        page.update
        log_init.logging.info("Page updated")

    def viewPop(e):
        page.views.pop()
        topView = page.views[-1]
        page.go(topView.route)
        log_init.logging.info("View go backward")


    """
    titleBar = ft.Row(
        [
            ft.WindowDragArea(
                ft.Container(
                    ft.Row(controls = [
                        ft.Row(controls = [ft.Icon(ft.Icons.MUSIC_NOTE_OUTLINED, size = 20), ft.Text(page.title)]),
                        ft.Row(controls = [ft.IconButton(ft.Icons.CLOSE, icon_size = 16, on_click = closeWindow)])
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),
                expand = True
            )
        ],
        height = 24
    )
    """

    # 窗口置顶按钮
    windowOnTop_btn = ft.IconButton(
        icon = ft.Icons.PUSH_PIN_OUTLINED,
        tooltip = lang.tooltips["alwaysOnTop"],
        on_click = alwaysOnTop
    )

    # 机翻警告
    machineTranslateWarning_icon = ft.Icon(
        ft.Icons.WARNING_AMBER_OUTLINED,
        color = ft.Colors.AMBER,
        tooltip = lang.infomation["machineTranslate"],
        visible = False
    )

    if lang.langInfo["machineTranslated"] == True:
        machineTranslateWarning_icon.visible = True
        log_init.logging.info("Add machine translate warning")

    # 菜单栏
    menuBar = ft.MenuBar(
        expand = True,
        controls = [
            ft.Row(controls = [
                ft.SubmenuButton(
                    content = ft.Text(value = lang.menuBar["files"]),
                    controls = [
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["openFile"]),
                            leading = ft.Icon(ft.Icons.FILE_OPEN_OUTLINED),
                            on_click = lambda _: pickFilesDialog.pick_files(allowed_extensions = ["mp3", "flac", "m4a", "wav", "aac"]),
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["openSonglist"]),
                            leading = ft.Icon(ft.Icons.PLAYLIST_ADD_OUTLINED),
                            on_click = lambda _: pickSonglistDialog.get_directory_path(),
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["getFromMusicWebsite"]),
                            leading = ft.Icon(ft.Icons.TRAVEL_EXPLORE_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["getWebMusic"]),
                                    leading = ft.Icon(ft.Icons.MUSIC_NOTE_OUTLINED),
                                    on_click = getSongFromWebsite
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["getWebAlbum"]),
                                    leading = ft.Icon(ft.Icons.ALBUM_OUTLINED)
                                )
                            ]
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["exit"]),
                            leading = ft.Icon(ft.Icons.EXIT_TO_APP_OUTLINED),
                            on_click = closeWindow
                        )
                    ]
                ),
                ft.SubmenuButton(
                    content = ft.Text(value = lang.menuBar["play"]),
                    controls = [
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["channels"]),
                            leading = ft.Icon(ft.Icons.TUNE_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["balance"]),
                                    leading = ft.Icon(ft.Icons.WIDTH_NORMAL),
                                    on_click = work.balanceMiddle
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shiftLeft"]),
                                    leading = ft.Icon(ft.Icons.ARROW_BACK_OUTLINED),
                                    on_click = work.balanceLeft
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shiftRight"]),
                                    leading = ft.Icon(ft.Icons.ARROW_FORWARD_OUTLINED),
                                    on_click = work.balanceRight
                                )
                            ]
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["position"]),
                            leading = ft.Icon(ft.Icons.TIMER_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["forward10s"]),
                                    leading = ft.Icon(ft.Icons.ARROW_FORWARD_OUTLINED),
                                    on_click = work.audioForward10sec
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["back10s"]),
                                    leading = ft.Icon(ft.Icons.ARROW_BACK_OUTLINED),
                                    on_click = work.audioBack10sec
                                )
                            ]
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["speed"]),
                            leading = ft.Icon(ft.Icons.SPEED_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["0.5x"]),
                                    leading = ft.Icon(ft.Icons.ARROW_BACK_OUTLINED),
                                    on_click = work.rateChangeTo05
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["1x"]),
                                    leading = ft.Icon(ft.Icons.ONE_X_MOBILEDATA_OUTLINED),
                                    on_click = work.rateChangeTo10
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["1.5x"]),
                                    leading = ft.Icon(ft.Icons.ARROW_FORWARD_OUTLINED),
                                    on_click = work.rateChangeTo15
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["2x"]),
                                    leading = ft.Icon(ft.Icons.ROCKET_LAUNCH_OUTLINED),
                                    on_click = work.rateChangeTo20
                                )
                            ]
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["volume"]),
                            leading = ft.Icon(ft.Icons.VOLUME_UP_OUTLINED),
                            on_click = openVolumePanel
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["lyrics"]),
                            leading = ft.Icon(ft.Icons.LYRICS_OUTLINED),
                            on_click = lyricShow
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["mode"]),
                            leading = ft.Icon(ft.Icons.PLAYLIST_PLAY_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["playInOrder"]),
                                    leading = ft.Icon(ft.Icons.PLAYLIST_PLAY_OUTLINED),
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["loop"]),
                                    leading = ft.Icon(ft.Icons.REPEAT_OUTLINED),
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["repeat"]),
                                    leading = ft.Icon(ft.Icons.REPEAT_ONE_OUTLINED),
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shuffle"]),
                                    leading = ft.Icon(ft.Icons.SHUFFLE_OUTLINED),
                                )
                            ]
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["audioInfo"]),
                            leading = ft.Icon(ft.Icons.INFO_OUTLINE),
                            on_click = openAudioInfoDlg
                        )
                    ]
                ),
                ft.SubmenuButton(
                    content = ft.Text(value = lang.menuBar["help"]),
                    controls = [
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["update"]),
                            leading = ft.Icon(ft.Icons.UPLOAD_OUTLINED),
                            on_click = checkForUpdate
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["about"]),
                            leading = ft.Icon(ft.Icons.QUESTION_MARK_OUTLINED),
                            on_click = openAboutDlg
                        )
                    ]
                ),
                windowOnTop_btn,
                ft.IconButton(
                        icon = ft.Icons.KEYBOARD_ARROW_UP_OUTLINED,
                        tooltip = lang.tooltips["hideMenuBar"],
                        on_click = hideShowMenuBar
                ),
                machineTranslateWarning_icon
                ]
            )
        ],
        visible = True,
        style = ft.MenuStyle(shape = ft.RoundedRectangleBorder(radius = 8))
    )

    audioCover = ft.Image(src = "./asset/track.png", width = 128, height = 128, border_radius = 8)
    audioTitle = ft.Text(audioTitleText, weight = ft.FontWeight.BOLD, size = 25, overflow = ft.TextOverflow.ELLIPSIS)
    onlineAudioSign = ft.Icon(ft.Icons.WIFI_OUTLINED, size = 16, visible = False, tooltip = lang.tooltips["onlineMusic"])
    audioArtistAndAlbum = ft.Text(audioArtistText, size = 18, opacity = 0.9)
    audioProgressStatus = ft.Text("00:00/00:00", size = 15, opacity = 0.9)
    audioDetail = ft.Column(controls = [ft.Row(controls = [audioTitle, onlineAudioSign]), audioArtistAndAlbum, audioProgressStatus])
    audioBasicInfo = ft.Container(content = ft.Row(controls = [audioCover, audioDetail]), padding = 3)
    audioProgressBar = ft.Slider(min = 0, max = 1000, tooltip = lang.tooltips["audioPosition"], on_change_start = autoStopKeepAudioProgress, on_change_end = progressCtrl)
    work.playAudio.on_loaded = loadAudio
    work.playAudio.on_position_changed = autoKeepAudioProgress
    
    skipPrevious_btn = ft.IconButton(
        icon = ft.Icons.SKIP_PREVIOUS_OUTLINED,
        tooltip = lang.tooltips["skipPrevious"],
        icon_size = 25,
        disabled = True,
        # on_click = playOrPauseMusic
    )

    playPause_btn = ft.IconButton(
        icon = ft.Icons.PLAY_CIRCLE_FILLED_OUTLINED,
        tooltip = lang.tooltips["playOrPause"],
        icon_size = 35,
        on_click = playOrPauseMusic
    )

    skipNext_btn = ft.IconButton(
        icon = ft.Icons.SKIP_NEXT_OUTLINED,
        tooltip = lang.tooltips["skipNext"],
        icon_size = 25,
        disabled = True,
        # on_click = playOrPauseMusic
    )

    volume_btn = ft.IconButton(
        icon = ft.Icons.VOLUME_UP_OUTLINED,
        tooltip = lang.tooltips["volume"],
        icon_size = 20,
        on_click = openVolumePanel
    )

    volume_silder = ft.Slider(min = 0, max = 100, divisions = 100, label = "{value}", value = cfg.cfgData["play"][0]["defaultVolume"], scale = 0.9, opacity = 0.9, on_change = volumeChange)

    volume_panel = ft.Card(
        content = volume_silder,
        visible = False,
        height = 46,
        width = 200,
        shape = ft.RoundedRectangleBorder(radius = 100)
    )
    
    lyrics_btn = ft.IconButton(
        icon = ft.Icons.LYRICS,
        tooltip = lang.tooltips["lyrics"],
        icon_size = 20,
        visible = True,
        on_click = lyricShow
    )

    playInRepeat_btn = ft.IconButton(
        icon = ft.Icons.REPEAT_ONE_OUTLINED,
        tooltip = lang.tooltips["playRepeat"],
        icon_size = 20,
        visible = True,
        on_click = enableOrDisableRepeat
    )

    audioList_btn = ft.IconButton(
        icon = ft.Icons.LIBRARY_MUSIC_OUTLINED,
        tooltip = lang.tooltips["songList"],
        icon_size = 20,
        on_click = audioListCtrl
    )
    songlist_tiles = ft.Column(controls = [],
        height = 380,
        spacing = 0,
        scroll = ft.ScrollMode.AUTO
    )
    audioList_menu = ft.Container(
        content = ft.Column(controls = [
                ft.Row(
                    controls = [
                        ft.Text(value = lang.songList["songList"], size = 20, weight = ft.FontWeight.BOLD),
                        ft.IconButton(icon = ft.Icons.CLOSE, on_click = hideAudioList)
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                songlist_tiles
            ],
        ),
        left = 10,
        top = 65,
        width = 300,
        height = 450,
        bgcolor = ft.Colors.ON_SURFACE_VARIANT,
        border_radius = 6,
        padding = 8,
        offset = ft.transform.Offset(-2, 0),
        animate_offset = ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT_CUBIC),
    )
    
    audioInfo_btn = ft.IconButton(
            icon = ft.Icons.INFO_OUTLINE,
            tooltip = lang.tooltips["audioInfo"],
            icon_size = 20,
            on_click = openAudioInfoDlg
        )

    settings_btn = ft.IconButton(
            icon = ft.Icons.SETTINGS_OUTLINED,
            tooltip = lang.tooltips["settings"],
            icon_size = 20,
            on_click = displaySettings
        )
    
    lyrics_before = ft.Text(size = 16, visible = True, color = ft.Colors.GREY)
    lyrics_text = ft.Text(size = 20, visible = True, weight = ft.FontWeight.BOLD)
    lyrics_after = ft.Text(size = 16, visible = True, color = ft.Colors.GREY)

    playbackCtrl_row = ft.Row(controls = [skipPrevious_btn, playPause_btn, skipNext_btn, volume_btn, volume_panel],spacing=1)
    moreBtns_row = ft.Row(controls = [lyrics_btn, playInRepeat_btn, audioList_btn, audioInfo_btn, settings_btn])
    btns_row = ft.Row(controls = [playbackCtrl_row, moreBtns_row], alignment = ft.MainAxisAlignment.SPACE_BETWEEN)

    releaseWarning = ft.Text(visible = False, size = 10, color = ft.Colors.GREY)

    if "pre" in ver:
        releaseWarning.value = "Pre-release version for testing purposes only! Current Version: " + ver
        log_init.logging.warning("You are using a pre-release version")
        releaseWarning.visible = True
        log_init.logging.info("Set releaseWarning as visible")
    if "debug" in ver:
        releaseWarning.value = "Debug version for development use! Current Version: " + ver
        log_init.logging.warning("You are using a debug version")
        releaseWarning.visible = True
        log_init.logging.info("Set releaseWarning as visible")
    if "experiment" in ver:
        releaseWarning.value = "Experimental version for develop and testing! Current Version: " + ver
        log_init.logging.warning("You are using a experiment version")
        releaseWarning.visible = True
        log_init.logging.info("Set releaseWarning as visible")

    page.overlay.append(audioList_menu)
    log_init.logging.info("Append audioList_menu")
    main_pageView = ft.View("/", controls = [ft.Column(controls = [ft.Row(controls = [menuBar]), audioBasicInfo, releaseWarning, audioProgressBar, btns_row, lyrics_before, lyrics_text, lyrics_after])], scroll = ft.ScrollMode.AUTO)
    page.views.append(main_pageView)
    page.go("/")
    log_init.logging.info("Set to page: main")
    page.on_view_pop = viewPop
    log_init.logging.info("Window initialization complete")

    if cfg.cfgData["lyrics"][0]["lyricsDefaultVisible"] == False:
        lyricShow(0)
    if cfg.cfgData["play"][0]["defaultPlayInLoop"] == True:
        enableOrDisableRepeat(0)

if __name__ == '__main__':
    log_init.logging.info("Program start")
    platform_check.detectOS()
    lang.loadLang()
    if platform_check.currentOS == 'wsl':
        print(lang.infomation["wslWarning"])
        log_init.logging.warning("Using WSL")
    if platform_check.currentOS == 'cygwin':
        print(lang.infomation["cygwinWarning"])
        log_init.logging.warning("Using Cygwin")
    if platform_check.currentOS == "windows":
        try:
            from windows_toasts import Toast, ToastDisplayImage, WindowsToaster
        except ImportError:
            toastImportError = True
        log_init.logging.info("Lib Windows-Toasts imported")
        from sys import getwindowsversion
        windowsBuild = getwindowsversion().build
        log_init.logging.info("Windows build: " + str(windowsBuild))
        if windowsBuild > 10240:
            # from lib import smtc
            pass
        del windowsBuild
    else:
        print(lang.infomation["nonTestWarning"])
        log_init.logging.warning("Non-test OS")
    
    audioTitleText = lang.mainMenu["unknownMusic"]
    audioArtistText = lang.mainMenu["unknownArtist"]
    work.audioInfo = lang.mainMenu["none"]
    log_init.logging.info("Basic initialization complete")
    log_init.logging.info("You are using " + ver)
    from pages import settingsPage
    settingsPage.transferPage(page)
    log_init.logging.info("Imported settingsPage")
    ft.app(target = main)
