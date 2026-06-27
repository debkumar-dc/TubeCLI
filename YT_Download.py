from logging import info
import os
import sys
from unittest import result
import yt_dlp
import time
import msvcrt
import subprocess
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from yt_dlp.utils import DownloadError

# global variable
print_after_download_file_name = False

# 🎨 Colors — ANSI escape codes for terminal color formatting

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"
RED = "\033[31m"
BLUE = "\033[34m"
WHITE = "\033[37m"
PURPLE = "\033[35m"
ORANGE  = "\033[38;5;208m"   # 256-color ANSI orange

# 🎵 Icons — Unicode icons for UI and status messages

ICON_PLAY = "▶"
ICON_CHECK = "✔"
ICON_FOLDER = "📂"
ICON_INFO = "ℹ"
ICON_WARN = "⚠"
ICON_ALL = "📜"
ICON_VIDEO = "🎬"
ICON_LIST = "📄"

_USE_ASCII_BAR = False  # Use ASCII-style UI bars if True

# 🎬 Update Tools - Update yt-dlp and ffmpeg via pip
def update_tools():
    """Update yt-dlp and ffmpeg via pip"""
    try:
        print(f"{YELLOW}🔄 Updating yt-dlp and ffmpeg...{RESET}")
        subprocess.run(
            [
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "--upgrade", 
                "yt-dlp",
                "yt-dlp-get-pot",
            ], 
            check=True)
        print(f"{GREEN}✅ Update complete!{RESET}")
    except Exception as e:
        print(f"{RED}❌ Update failed: {e}{RESET}")

# 🗂️ Animate Printing - Prints text with a typing effect
def animate_printing(banner, delay=0.05, sleep_time=0.002):
    """Animate printing of text line by line."""
    for line in banner:
        for ch in line:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(sleep_time)  # typing speed
        print()
        time.sleep(delay)
    print("\n")  # spacing

# 🗂️ Splash Screen - Displays the initial splash screen with animationS
def splash_screen():
    banner = [
        f"{CYAN}{BOLD}╔════════════════════════════════════════════════════════════════════════╗{RESET}",
        f"{CYAN}{BOLD}║{RESET}   {MAGENTA}🎬  YOUTUBE DOWNLOADER: {YELLOW}1080P HDR {GREEN}+ HD AUDIO 5.1 E-AC3 {WHITE}+ SUBTITLE{RESET}    {CYAN}{BOLD}║{RESET}",
        f"{CYAN}{BOLD}║{RESET}   {BLUE}⚡ Powered by yt-dlp + ffmpeg ⚡{RESET}                                     {CYAN}{BOLD}║{RESET}",
        f"{CYAN}{BOLD}║{RESET}   {WHITE}Press {GREEN}[U]{RESET}{WHITE} to Update, {RED}[ESC]{RESET}{WHITE} to Exit, or Paste URL...                {RESET}  {CYAN}{BOLD}║{RESET}",
        f"{CYAN}{BOLD}╚════════════════════════════════════════════════════════════════════════╝{RESET}"
    ]

    # Animate printing line by line
    animate_printing(banner)

# 🗂️ Video Info - Prints detailed video information
def vd_info(info, url):
    banner = [
        f"{RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}",
        f"{GREEN}▶️ Title:{RESET} {YELLOW}{info.get('title')}{RESET}",
        f"{GREEN}👤 Uploader:{RESET} {YELLOW}{info.get('uploader')}{RESET}",
        f"{GREEN}📺 Channel URL:{RESET} {YELLOW}{info.get('channel_url')}{RESET}",
        f"{GREEN}🎞️ Video URL:{RESET} {YELLOW}{url}{RESET}",
        f"{GREEN}📅 Upload Date:{RESET} {YELLOW}{datetime.strptime(info.get('upload_date', '00010101'), '%Y%m%d').strftime('%d %b %Y') if info.get('upload_date') else 'Unknown'}{RESET}",
        f"{GREEN}⏰ Duration:{RESET} {YELLOW}{info.get('duration')} seconds{RESET}",
        f"{GREEN}📏 Resolution:{RESET} {YELLOW}{info.get('height')}p @ {info.get('fps')} fps{RESET}",
        f"{GREEN}🎥 Video Codec:{RESET} {YELLOW}{info.get('vcodec')}{RESET}",
        f"{GREEN}🎬 Video Bitrate:{RESET} {YELLOW}{info.get('vbr')} kbps{RESET}",
        f"{GREEN}🎵 Audio Codec:{RESET} {YELLOW}{info.get('acodec')}{RESET}",
        f"{GREEN}🔊 Audio Bitrate:{RESET} {YELLOW}{info.get('abr')} kbps{RESET}",
        f"{GREEN}🎶 Audio Channels:{RESET} {YELLOW}{info.get('audio_channels')} Channels{RESET}",
        f"{GREEN}🌐 Language:{RESET} {YELLOW}{info.get('language', 'unknown')}{RESET}",
        f"{GREEN}🗨️ Subtitles:{RESET} {YELLOW}{', '.join(info.get('requested_subtitles', {}).keys()) or 'None'}{RESET}",
        f"{GREEN}📂 Category:{RESET} {YELLOW}{get_category(info.get('duration', 0))}{RESET}",
        f"{GREEN}💽 File Size:{RESET} {YELLOW}{format_size(info.get('filesize_approx'))}{RESET}",
        f"{RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    ]
    # Animate printing line by line
    animate_printing(banner)

# 🗂️ Video Download Start - Prints a banner indicating the start of the download
def vd_down_start():
    banner = [
        f"\n{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}",
        f"{BLUE}━━━━━━━━━━━━━━━━━━━━{YELLOW} ⚡ DOWNLOADING ⚡{WHITE}━━━━━━━━━━━━━━━━━━━━{RESET}",
        f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}",
    ]
    # Animate printing line by line
    animate_printing(banner)

# 🗂️ Video Download End - Prints a banner indicating the end of the download
def vd_down_end():
    banner = [
        f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}",
        f"{WHITE}━━━━━━━━━━━━━━━━━━━━{YELLOW} ⚡ OUTPUT END ⚡{BLUE}━━━━━━━━━━━━━━━━━━━━{RESET}",
        f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}",
    ]

    # Animate printing line by line
    animate_printing(banner)

# 🛠️ Helper Functions — Utility functions for download and UI
def wait_for_enter(prompt=f"{ORANGE}Press Enter to return to menu ...{RESET}"):
    """Flush keyboard buffer and wait for Enter."""
    while msvcrt.kbhit():
        msvcrt.getwch()
    restore_stdin()  # <-- Add this line
    input(prompt)

# 🎬 Restore Stdin - Restore sys.stdin after Tkinter popup on Windows, if possible.
def restore_stdin():
    """Restore sys.stdin after Tkinter popup on Windows, if possible."""
    if sys.platform.startswith('win'):
        try:
            sys.stdin = open('CONIN$', 'r')
        except OSError:
            pass  # Ignore if handle is invalid (e.g., running --noconsole)

# 🎬 Normalize URL - Convert short IDs into full YouTube URLs if possible.
def normalize_url(url: str) -> str:
    """Convert short IDs into full YouTube URLs if possible."""
    if url.startswith(("http://", "https://")):
        return url
    # YouTube video ID check (11 chars, alphanumeric + - or _)
    if len(url) == 11 and all(c.isalnum() or c in "-_" for c in url):
        return f"https://youtu.be/{url}"
    # Playlist ID check
    if url.startswith("PL") and len(url) > 12:
        return f"https://www.youtube.com/playlist?list={url}"
    return url


# 🗂️ Format Size - Converts bytes to a human-readable format
def format_size(bytes_val):
    """Convert bytes to human-readable format"""
    if bytes_val is None:
        return "?"
    for unit in ['B', 'KiB', 'MiB', 'GiB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f}TiB"

# 🗂️ Get Video Category - Determines the category of a video based on duration
def get_category(duration):
    """
    🎯 Determine the category of a video based on duration (in seconds)
    
    ⏱ Rules:
    - <= 7 min (420s)   → songs
    - <= 1 hour (3600s) → series
    - > 1 hour          → movies
    """
    if duration < 420:
        return "songs"      # 🎵 Short videos / songs
    elif 420 <= duration <= 3600:
        return "series"     # 📺 Medium videos / series episodes
    else:
        return "movies"     # 🎬 Long videos / movies

# 🎬 Open File - Opens a file with the default application
def open_file(path):
    if sys.platform.startswith("darwin"):  # macOS
        subprocess.run(["open", path])
    elif os.name == "nt":  # Windows
        os.startfile(path)
    elif os.name == "posix":  # Linux
        subprocess.run(["xdg-open", path])

# 🎬 Post-Processor Hooks - Handles post-processing tasks after download
def postprocessor_hooks(d):
    global print_after_download_file_name
    if d['status'] == 'finished' and not print_after_download_file_name:
        filepath = (
            d.get('info_dict', {}).get('filepath')
            or d.get('info_dict', {}).get('_filename')
            or d.get('filename')
        )
        if filepath:
            print(f"📂 File saved at: {os.path.abspath(filepath)}")
            print_after_download_file_name = True
            countdown = 5
            played = False

            for i in range(countdown, 0, -1):
                bar_len = 10
                filled_len = int(bar_len * (countdown - i + 1) / countdown)
                bar = f"{PURPLE}{'█' * filled_len}{PURPLE}{'░' * (bar_len - filled_len)}{RESET}"

                print(f"\r⏳ Press [P] to Play | Auto closing in {i}s [{bar}]  ", end='', flush=True)

                start_time = time.time()
                while time.time() - start_time < 1:
                    if msvcrt.kbhit():
                        key = msvcrt.getwch().lower()
                        if key == 'p':
                            print(f"\r▶ Playing file: {CYAN}{os.path.abspath(filepath)}{RESET}")
                            open_file(os.path.abspath(filepath))
                            played = True
                            break
                if played:
                    break

            if not played:
                print("\r⌛ Countdown finished without playing.")

# 🎬 Progress Hook - Displays download progress and speed with part type
def progress_hook(d):
    """Display download progress bar and speed with part type"""
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0) or 0
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        percent = (downloaded / total * 100) if total else 0

        bar_len = 30
        filled_len = int(bar_len * percent / 100)
        bar = f"{GREEN}{'█' * filled_len}{GREEN}{'░' * (bar_len - filled_len)}{RESET}"

        speed = d.get('speed') or 0
        eta = d.get('eta') or 0

        print(
            f"\r{CYAN}{ICON_PLAY} {bar} {YELLOW}{percent:5.1f}%{RESET} "
            f"{YELLOW}| {format_size(downloaded)} / {format_size(total)}{RESET} "
            f"{GREEN}| {format_size(speed)}/s{RESET} "
            f"{MAGENTA}| ETA {eta if eta else '?'}s{RESET}    ",
            end='',
            flush=True
        )

    elif d['status'] == 'finished':
        filename = d.get('filename', '')
        info = d.get('info_dict', {})

        vcodec = info.get('vcodec', 'none')
        acodec = info.get('acodec', 'none')

        # Detect part type
        if filename.endswith(('.vtt', '.srt')):
            part_type = "Subtitle"
        elif vcodec != 'none' and acodec != 'none':
            part_type = "Video+Audio"
        elif vcodec != 'none' and acodec == 'none':
            part_type = "Video"
        elif vcodec == 'none' and acodec != 'none':
            part_type = "Audio"
        else:
            part_type = "Unknown"

        print(f"\n{GREEN}{ICON_CHECK} {part_type} Download Complete!{RESET}")
        print(f"{GREEN}📂 {part_type} Output Path:{RESET} {YELLOW}{filename}{RESET}")

# def after_download_hook(d):
# def prepare_outtmpl(d):
# def metadata_hook(d):

# 🎬 Get YouTube-DL Options -  YouTube-DL options for downloading videos
def get_ydl_opts():
    format_selection = (
        "bv[height<=1080][vcodec^=vp9.2][ext=mp4]+ba[ext=m4a]/"
        "bv[height<=1080][vcodec^=vp9.2][ext=webm]+ba[ext=m4a]/"
        "bv[height<=1080][vcodec*=av01][ext=mp4]+ba[ext=m4a]/"
        "bv[height<=1080][vcodec*=av01][ext=webm]+ba[ext=m4a]/"
        "bv[height<=1080][vcodec^=vp9][ext=mp4]+ba[ext=m4a]/"
        "bv[height<=1080][vcodec^=vp9][ext=webm]+ba[ext=m4a]/"
        "bv[height<=1080][vcodec^=vp09][ext=mp4]+ba[ext=m4a]/"
        "bv[height<=1080][vcodec^=vp09][ext=webm]+ba[ext=m4a]/"
        "bv[height<=1080][ext=mp4]+ba[ext=m4a]/"
        "bv[height<=1080][ext=webm]+ba[ext=m4a]/"
        "b[height<=1080][ext=mp4]"
    )

    COOKIE_DIR = os.path.join(os.environ["USERPROFILE"], ".yt-dlp")
    COOKIE_FILE = os.path.join(COOKIE_DIR, "cookies.txt")
    
    return {
        'cookies': COOKIE_FILE,  
        'format': format_selection,
        'format_sort': ["res:1080", "filesize", "aext", "abr"],

        # ⚠ Warnings / Errors
        'quiet': True,           
        'no_warnings': True,     
        'ignoreerrors': True,    
        'no_call_home': True,    

        # 🖼 Thumbnails / Metadata
        'embedthumbnail': True,  
        'writeinfojson': True,   
        'embedmetadata': True,   

        # 🖥 Console
        'consoletitle': True,    

        # 📦 Output / Post-processing
        'merge_output_format': "mp4",  
        'postprocessors': [{'key': 'FFmpegMetadata'}],

        # 📜 Subtitles
        'writesubtitles': True,        
        'writeautomaticsub': True,     
        'subtitleslangs': ["en.*", "bn.*"],  
        'subtitlesformat': "best",     
        'embedsubtitles': True,        

        # ⏱ Hooks
        # 'pre_hooks': [prepare_outtmpl],  # << hook to set outtmpl dynamically
        'progress_hooks': [progress_hook],         
        'postprocessor_hooks': [postprocessor_hooks],  

        # 📂 Playlist / Output
        'noplaylist': False,
        'outtmpl': ""  # will override later
    }

# 🎬 Download Video - Main function to download a video
def download_video(url):
    """Download a video or playlist with full options"""
    vd_down_start()
    ydl_opts = get_ydl_opts()
    # ydl_opts['outtmpl'] = os.path.join(os.environ['USERPROFILE'], 'Videos', 'YT Download','Download', 'TMP', '%(id)s/%(title)s.%(ext)s')  # 🗂 Output filename template

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        global print_after_download_file_name
        try:
            # 🟢 Fetch metadata before downloading
            info = ydl.extract_info(url, download=False)

            # 📄 Print detailed info BEFORE download
            print(f"{GREEN}⏳ Download Started!{RESET} {CYAN}: {RESET} {CYAN}[ 🎥 Video Info 🎥 ]{RESET}")
            print(f"{GREEN}🎬 Downloading Video:{RESET} {YELLOW}{info.get('playlist_index', 1)} Out Of {info.get('playlist_count', 1)}{RESET}")

            # 🖥️ Display video info
            vd_info(info, url)

            # 🗂️ Prepare output directory and template
            base_dir = os.path.join(os.environ['USERPROFILE'], 'Videos', 'YT Download')
            duration = info.get('duration') or 0
            language = info.get('language') or 'unknown'
            category = get_category(duration)
            title = info.get('title') or 'unknown'
            file_name = f"{title}.{info.get('ext', 'mp4')}"

            # Build outtmpl safely
            if category == 'songs':
                store_path = os.path.join(base_dir, category, language)     # 🎵 Short videos / songs
            elif category == 'series':
                store_path = os.path.join(base_dir, category, language, '%(title)s')     # 📺 Medium videos / series episodes
            else:
                store_path = os.path.join(base_dir, category, language, '%(title)s')     # 🎬 Long videos / movies

            # If you want yt-dlp to sanitize automatically, set:
            outtmpl = os.path.join(store_path, '%(title)s.%(ext)s')
        
            if not outtmpl:
                return  # user cancelled
            ydl.params['outtmpl'] = {'default': outtmpl}
            ydl.params['paths'] = {'home': store_path}  # optional, clearer

            # yt-dlp also has its own sanitization, you can enable:
            ydl.params['restrictfilenames'] = False  # or True for strict safe names

            # Set up progress hooks
            countdown = 5
            hold = False
            stop = False

            print("Press H to hold ⏸, S to download ⬇️ immediately, X to cancel ❌. Auto download in 5 seconds...")

            for i in range(countdown, 0, -1):
                # Timer bar style
                bar_len = 10
                filled_len = int(bar_len * (countdown - i + 1) / countdown)
                bar = f"{BLUE}{'█' * filled_len}{BLUE}{'░' * (bar_len - filled_len)}{RESET}"

                print(f"\r⏳ Auto select D in {YELLOW}{i}s{RESET} [{bar}]", end='', flush=True)
                
                start_time = time.time()
                while time.time() - start_time < 1:
                    if msvcrt.kbhit():
                        key = msvcrt.getwch().lower()
                        if key == 'h':
                            hold = True
                            print("\n⏸ Hold activated.")
                            print("Press S to start download ⬇️ or X to stop ❌.")
                            break
                        elif key == 's':
                            print("\n⬇️ Download starting immediately!")
                            hold = False
                            countdown = 0
                            break
                        elif key == 'x':
                            stop = True
                            break
                if hold:
                    while True:
                        # Hold display with blinking effect
                        for dot in ['.', '..', '...']:
                            print(f"\r⏸ Waiting{dot}  ", end='', flush=True)
                            time.sleep(0.5)
                            if msvcrt.kbhit():
                                key = msvcrt.getwch().lower()
                                if key == 's':
                                    print("\n⬇️ Download starting!", flush=True)
                                    hold = False
                                    break
                                elif key == 'x':
                                    stop = True
                                    break
                        if not hold or stop:
                            break
                    break
                if stop:
                    break

            if stop:
                print("\n❌ Download cancelled by user.")
            elif not hold:
                print("\n⬇️ Auto download starting now!")
                # ✅ Start download
                result = ydl.download([url])
                # Check if the download was successful
                if result == 0:
                    print(f"{GREEN}✔ Download Complete!{RESET} {CYAN}: {RESET} {CYAN}[ 😊 Hurray 😊 ]{RESET}")
                else:
                    print(f"{RED}❌ Download failed!{RESET}")

        except Exception as e:
            print(f"{RED}❌ Error: {e}{RESET}")
    vd_down_end()
    print_after_download_file_name = False

# 🎬 Preview Formats - Show available video formats
def preview_formats(url, all_videos=False):
    """Preview available formats for a single video or a playlist"""
    vd_down_start()
    ydl_opts = get_ydl_opts()
    ydl_opts['listformats'] = True

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"{MAGENTA}📄 Available Formats for URL:{RESET} {YELLOW}{url}{RESET}")

            # 🟢 Fetch metadata before downloading
            info = ydl.extract_info(url, download=False)


            # 📄 Print detailed info BEFORE download
            print(f"{GREEN}🎬 Previewing Video:{RESET} {YELLOW}{info.get('playlist_index', 1)} Out Of {info.get('playlist_count', 1)}{RESET}")

            print(f"{GREEN}✅ Format preview completed!{RESET}")
        except DownloadError as e:
            print(f"{RED}❌ Error fetching formats: {e}{RESET}")
        except Exception as e:
            print(f"{RED}❌ Unexpected error: {e}{RESET}")
    vd_down_end()


# 🖥️ Main Loop — User input and menu logic
if __name__ == "__main__":
    while True:
        os.system('cls')
        splash_screen()

        buffer = ""
        print(
             f"{YELLOW}🎬 Enter YouTube URL / ID / Playlist "
             f"{CYAN}⚡ [U=Update]{YELLOW}, "
             f"{RED}❌ [Q/ESC/EXIT=Quit]{RESET}: ",
             end="",
             flush=True
        )

        # read keystrokes manually
        while True:
            key = msvcrt.getwch()
            if key == "\r":  # Enter pressed
                print()  # newline
                break
            elif key == "\x1b":  # ESC pressed
                print(f"\n{RED}✖ Goodbye!{RESET}")
                sys.exit(0)
            elif key == "\b":  # Backspace
                if buffer:
                    buffer = buffer[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                buffer += key
                sys.stdout.write(key)
                sys.stdout.flush()

        URL = buffer.strip()

        # Empty input check
        if not URL:
            print(f"{RED}⚠ No URL entered. Please try again.{RESET}\n")
            time.sleep(2)
            continue

        # EXIT command
        if URL.upper() == "EXIT":
            print(f"{RED}✖ Goodbye!{RESET}")
            sys.exit(0)

        # Update command
        if URL.upper() == "U":
            print(f"\n{CYAN}⚡ Update requested...{RESET}")
            update_tools()
            continue

        # Normalize potential video/playlist ID
        URL = normalize_url(URL)

        # Final confirmation
        print(f"{GREEN}👉 Final URL to process:{RESET} {URL}\n")

        # 🔥 Now you can call your yt-dlp functions with URL
        # ───────── Single video ─────────
        if "list=" not in URL:
            YTURL = URL
            print(f"{GREEN}{ICON_VIDEO}  [D]{RESET} {YELLOW}Download Now{RESET}")
            print(f"{CYAN}{ICON_LIST}  [L]{RESET} {YELLOW}View ONLY The Current Formats{RESET}")

            choice = ""
            start_time = time.time()
            print(f"Enter D or L (default D in 5s): ", end='', flush=True)
            while time.time() - start_time < 5:
                if msvcrt.kbhit():
                    choice = msvcrt.getwch().upper()
                    print(choice, end='', flush=True)
                    break
                # Countdown progress bar
                i = 5 - int(time.time() - start_time)
                bar_len = 10
                filled_len = int(bar_len * (5 - i + 1) / 5)
                bar = f"{YELLOW}{'█' * filled_len}{YELLOW}{'░' * (bar_len - filled_len)}{RESET}"
                print(f"\r⏳ Auto select D in {YELLOW}{i}s{RESET} [{bar}]", end='', flush=True)
                time.sleep(0.1)

            if choice != "L":
                choice = "D"

            if choice == "L":
                preview_formats(YTURL, all_videos=False)
                wait_for_enter()
            else:
                download_video(YTURL)
                wait_for_enter()
            continue

        # ───────── Playlist detected ─────────
        else:
            print(f"{YELLOW}{ICON_WARN} Playlist Detected{RESET}")
            print(f"{GREEN}{ICON_ALL}  [A]{RESET} {YELLOW}Download ALL Videos In The Playlist{RESET}")
            print(f"{GREEN}{ICON_VIDEO}  [C]{RESET} {YELLOW}Download ONLY The Current Video{RESET}")
            print(f"{CYAN}{ICON_LIST}  [L]{RESET} {YELLOW}View ONLY The Current Video Formats{RESET}")
            print(f"{CYAN}{ICON_LIST}  [LA]{RESET} {YELLOW}View ALL Formats From Playlist{RESET}")

            choice = ""
            start_time = time.time()
            print(f"Enter A, C, L, or LA (default C in 5s): ", end='', flush=True)
            while time.time() - start_time < 5:
                if msvcrt.kbhit():
                    choice = msvcrt.getwch().upper()
                    print(choice, end='', flush=True)
                    break
                # Countdown progress bar
                i = 5 - int(time.time() - start_time)
                bar_len = 10
                filled_len = int(bar_len * (5 - i + 1) / 5)
                bar = f"{MAGENTA}{'█' * filled_len}{MAGENTA}{'░' * (bar_len - filled_len)}{RESET}"
                print(f"\r⏳ Auto select C in {YELLOW}{i}s{RESET} [{bar}]", end='', flush=True)
                time.sleep(0.1)

            if choice not in ["A", "L", "LA"]:
                choice = "C"

            if choice == "A":
                YTURL = URL
                download_video(YTURL)
                wait_for_enter()
            elif choice == "C":
                YTURL = URL.split('?')[0]
                download_video(YTURL)
                wait_for_enter()
            elif choice == "L":
                YTURL = URL.split('?')[0]
                preview_formats(YTURL, all_videos=False)
                wait_for_enter()
            elif choice == "LA":
                YTURL = URL
                preview_formats(YTURL, all_videos=True)
                wait_for_enter()
            else:
                print(f"{RED}{ICON_WARN} Invalid Choice. Returning to menu.{RESET}")
                wait_for_enter()
            continue