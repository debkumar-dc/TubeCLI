@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Get ANSI escape character for colors
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

:: Colors
set "RESET=%ESC%[0m"
set "BOLD=%ESC%[1m"
set "CYAN=%ESC%[36m"
set "YELLOW=%ESC%[33m"
set "GREEN=%ESC%[32m"
set "MAGENTA=%ESC%[35m"
set "RED=%ESC%[31m"
set "BLUE=%ESC%[34m"
set "WHITE=%ESC%[37m"

:: Icons (safe in most Windows terminals)
set "ICON_PLAY=▶"
set "ICON_LIST=📜"
set "ICON_VIDEO=🎬"
set "ICON_ALL=📂"
set "ICON_WARN=⚠"


:: Output folder
set "OUTDIR=%~dp0downloads"

:: Create output directory if not exists
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

:: Path to cookies file
set "COOKIE_DIR=%USERPROFILE%\.yt-dlp"
set "COOKIE_FILE=%COOKIE_DIR%\cookies.txt"

:: Create folder if it does not exist
if not exist "%COOKIE_DIR%" mkdir "%COOKIE_DIR%"

:: Create cookie file if it does not exist
if not exist "%COOKIE_FILE%" echo. > "%COOKIE_FILE%"


:START
cls
echo %CYAN%%BOLD%╔══════════════════════════════════════════════════╗%RESET%
echo %CYAN%%BOLD%║%RESET%   %MAGENTA%🎬 YOUTUBE DOWNLOADER: 1080P HDR WITH HD AUDIO%RESET% %CYAN%%BOLD%║%RESET%
echo %CYAN%%BOLD%╚══════════════════════════════════════════════════╝%RESET%
echo.

:: pip install -U yt-dlp
:: Prompt for URL
set /p "URL=%YELLOW%Enter YouTube video or playlist URL (or type EXIT to quit): %RESET%"

if /i "%URL%"=="EXIT" goto END

:: Playlist / Video detection
set "LFLAG=0"

echo %URL% | findstr /i "list=" >nul
if errorlevel 1 (
    :: No playlist
    set "YTURL=%URL%"
    echo %GREEN%%ICON_VIDEO%  [D]%RESET% %YELLOW%Download Now%RESET%
    echo %CYAN%%ICON_LIST%  [L]%RESET% %YELLOW%View ONLY The Current Formats%RESET%
    set /p "choice=%BLUE%Enter D or L:%RESET% "
    if /i "!choice!"=="L" set "LFLAG=1"
) else (
    :: Playlist detected
    echo %YELLOW%%ICON_WARN% Playlist Detected%RESET%
    echo %GREEN%%ICON_ALL%  [A]%RESET% %YELLOW%Download ALL Videos In The Playlist%RESET%
    echo %GREEN%%ICON_VIDEO%  [C]%RESET% %YELLOW%Download ONLY The Current Video%RESET%
    echo %CYAN%%ICON_LIST%  [L]%RESET% %YELLOW%View ONLY The Current Video Formats%RESET%
    echo %CYAN%%ICON_LIST%  [LA]%RESET% %YELLOW%View ALL Formats From Playlist%RESET%
    set /p "choice=%BLUE%Enter A, C, L, or LA:%RESET% "
    if /i "!choice!"=="A" (
        set "YTURL=%URL%"
    ) else if /i "!choice!"=="C" (
        for /f "tokens=1 delims=?" %%a in ("%URL%") do set "YTURL=%%a"
    ) else if /i "!choice!"=="L" (
        for /f "tokens=1 delims=?" %%a in ("%URL%") do set "YTURL=%%a"
        set "LFLAG=1"
    ) else if /i "!choice!"=="LA" (
        set "YTURL=%URL%"
        set "LFLAG=1"
    ) else (
        echo %RED%%ICON_WARN% Invalid Choice. Exiting.%RESET%
        goto START
    )
)


:: Build readable format string (note vcodec^^= to preserve literal ^)
set "FMT="
set "FMT=!FMT!bv[height<=1080][vcodec^^=vp9.2][ext=mp4]+ba[ext=m4a]/"
set "FMT=!FMT!bv[height<=1080][vcodec^^=vp9.2][ext=webm]+ba[ext=m4a]/"
set "FMT=!FMT!bv[height<=1080][vcodec*=av01][ext=mp4]+ba[ext=m4a]/"
set "FMT=!FMT!bv[height<=1080][vcodec*=av01][ext=webm]+ba[ext=m4a]/"
set "FMT=!FMT!bv[height<=1080][vcodec^^=vp9][ext=mp4]+ba[ext=m4a]/"
set "FMT=!FMT!bv[height<=1080][vcodec^^=vp9][ext=webm]+ba[ext=m4a]/"
set "FMT=!FMT!bv[height<=1080][vcodec^^=vp09][ext=mp4]+ba[ext=mp4]/"
set "FMT=!FMT!bv[height<=1080][vcodec^^=vp09][ext=webm]+ba[ext=mp4]/"
set "FMT=!FMT!bv[height<=1080][ext=mp4]+ba[ext=m4a]/"
set "FMT=!FMT!bv[height<=1080][ext=webm]+ba[ext=m4a]/"
set "FMT=!FMT!b[height<=1080][ext=mp4]"


cls
echo %WHITE%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%
echo %BLUE%━━━━━━━━━━━━━━━━━━━━%YELLOW% ⚡ DOWNLOADING ⚡%WHITE%━━━━━━━━━━━━━━━━━━━━%RESET%
echo %WHITE%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%

echo.

:: List formats if needed
if "%LFLAG%"=="1" (
    echo %CYAN%%ICON_LIST% Listing formats for:%RESET% %GREEN%%YTURL%%RESET%
    yt-dlp ^
      --cookies "%COOKIE_FILE%" ^
      --no-warnings ^
      --no-call-home ^
      --ignore-errors ^
      --embed-thumbnail ^
      --write-info-json ^
      --console-title ^
      --merge-output-format mp4 ^
      --write-sub ^
      --write-auto-sub ^
      --sub-lang "en.*,bn.*" ^
      --sub-format "best" ^
      --embed-subs ^
      --embed-metadata ^
      --list-formats ^
      --simulate ^
      --progress-template "%ESC%[36m▶ %(progress._percent_str)s%ESC%[0m %ESC%[33m| %(progress._downloaded_bytes_str)s / %(progress._total_bytes_str)s%ESC%[0m %ESC%[32m| %(progress._speed_str)s%ESC%[0m %ESC%[35m| ETA %(progress._eta_str)s%ESC%[0m" ^
      -S "res:1080,filesize,aext,abr" ^
      -f  "!FMT!" ^
      -o "%OUTDIR%\%%(audio_channels)s\%%(title)s\%%(title)s.%%(ext)s" ^
      --print "%GREEN%⏳ Download Started!%RESET% %CYAN%: %RESET% %CYAN%[ 🎥 Video Info 🎥 ]%RESET%" ^
      --print "%GREEN%🎬 Downloading Video:%RESET% %YELLOW%%%(playlist_index|1)s Out Of %%(playlist_count|1)s%RESET%" ^
      --print "%RED%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%" ^
      --print "%GREEN%▶️ Title:%RESET% %YELLOW%%%(title)s%RESET%" ^
      --print "%GREEN%👤 Uploader:%RESET% %YELLOW%%%(uploader)s%RESET%" ^
      --print "%GREEN%📺 Channel URL:%RESET% %YELLOW%%%(channel_url)s%RESET%" ^
      --print "%GREEN%🎞️ Video URL:%RESET% %YELLOW%%YTURL%%RESET%" ^
      --print "%GREEN%📅 Upload Date:%RESET% %YELLOW%%%(upload_date>%%Y-%%m-%%d)s%RESET%" ^
      --print "%GREEN%⏰ Duration:%RESET% %YELLOW%%%(duration>%%H:%%M:%%S)s%RESET%" ^
      --print "%GREEN%📏 Resolution:%RESET% %YELLOW%%%(height)s p @ %%(fps)s fps%RESET%" ^
      --print "%GREEN%🎥 Video Codec:%RESET% %YELLOW%%%(vcodec)s%RESET%" ^
      --print "%GREEN%🎬 Video Bitrate:%RESET% %YELLOW%%%(vbr)s kbps%RESET%" ^
      --print "%GREEN%🎵 Audio Codec:%RESET% %YELLOW%%%(acodec)s%RESET%" ^
      --print "%GREEN%🔊 Audio Bitrate:%RESET% %YELLOW%%%(abr)s kbps%RESET%" ^
      --print "%GREEN%🎶 Audio Channels:%RESET% %YELLOW%%%(language)s %%(audio_channels)s Channels%RESET%" ^
      --print "%GREEN%💽 File Size:%RESET% %YELLOW%%%(filesize_approx)s bytes%RESET%" ^
      --print "%RED%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%" ^
      "%YTURL%"
)
if "%LFLAG%"=="0" (
    yt-dlp ^
      --cookies "%COOKIE_FILE%" ^
      --no-warnings ^
      --no-call-home ^
      --ignore-errors ^
      --embed-thumbnail ^
      --write-info-json ^
      --console-title ^
      --merge-output-format mp4 ^
      --write-sub ^
      --write-auto-sub ^
      --sub-lang "en.*,bn.*" ^
      --sub-format "best" ^
      --embed-subs ^
      --embed-metadata ^
      --progress-template "%ESC%[36m▶ %(progress._percent_str)s%ESC%[0m %ESC%[33m| %(progress._downloaded_bytes_str)s / %(progress._total_bytes_str)s%ESC%[0m %ESC%[32m| %(progress._speed_str)s%ESC%[0m %ESC%[35m| ETA %(progress._eta_str)s%ESC%[0m" ^
      -S "res:1080,filesize,aext,abr" ^
      -f  "!FMT!" ^
      -o "%OUTDIR%\%%(audio_channels)s\%%(title)s\%%(title)s.%%(ext)s" ^
      --print "%GREEN%⏳ Download Started!%RESET% %CYAN%: %RESET% %CYAN%[ 🎥 Video Info 🎥 ]%RESET%" ^
      --print "%GREEN%🎬 Downloading Video:%RESET% %YELLOW%%%(playlist_index|1)s Out Of %%(playlist_count|1)s%RESET%" ^
      --print "%RED%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%" ^
      --print "%GREEN%▶️ Title:%RESET% %YELLOW%%%(title)s%RESET%" ^
      --print "%GREEN%👤 Uploader:%RESET% %YELLOW%%%(uploader)s%RESET%" ^
      --print "%GREEN%📺 Channel URL:%RESET% %YELLOW%%%(channel_url)s%RESET%" ^
      --print "%GREEN%🎞️ Video URL:%RESET% %YELLOW%%YTURL%%RESET%" ^
      --print "%GREEN%📅 Upload Date:%RESET% %YELLOW%%%(upload_date>%%Y-%%m-%%d)s%RESET%" ^
      --print "%GREEN%⏰ Duration:%RESET% %YELLOW%%%(duration>%%H:%%M:%%S)s%RESET%" ^
      --print "%GREEN%📏 Resolution:%RESET% %YELLOW%%%(height)s p @ %%(fps)s fps%RESET%" ^
      --print "%GREEN%🎥 Video Codec:%RESET% %YELLOW%%%(vcodec)s%RESET%" ^
      --print "%GREEN%🎬 Video Bitrate:%RESET% %YELLOW%%%(vbr)s kbps%RESET%" ^
      --print "%GREEN%🎵 Audio Codec:%RESET% %YELLOW%%%(acodec)s%RESET%" ^
      --print "%GREEN%🔊 Audio Bitrate:%RESET% %YELLOW%%%(abr)s kbps%RESET%" ^
      --print "%GREEN%🎶 Audio Channels:%RESET% %YELLOW%%%(language)s %%(audio_channels)s Channels%RESET%" ^
      --print "%GREEN%💽 File Size:%RESET% %YELLOW%%%(filesize_approx)s bytes%RESET%" ^
      --print "%RED%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%" ^
      --print after_move:"%GREEN%✔ Download Complete!%RESET% %CYAN%: %RESET% %CYAN%[ 😊 Hurray 😊 ]%RESET%" ^
      --print after_move:"%GREEN%📂 Output Path:%RESET% %YELLOW%%OUTDIR%\%%(audio_channels)s\%%(title)s%RESET%" ^
      "%YTURL%"
)

echo.

echo %WHITE%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%
echo %WHITE%━━━━━━━━━━━━━━━━━━━━━%YELLOW% ⚡ OUTPUT END ⚡%BLUE%━━━━━━━━━━━━━━━━━━━━%RESET%
echo %WHITE%━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%RESET%

echo %MAGENTA%Returning to menu...%RESET%

pause
goto START

:END
echo.
echo %RED%✖ Goodbye!%RESET%
timeout /t 2 >nul