import os
import yt_dlp
import random
import pygame
from hyperlink import URL
from colorama import init, Fore, Style

pygame.mixer.init()

def download_song(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [show_progress],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def show_progress(d):
    if d['status'] == 'downloading':
        progress = d['_percent_str']
        print(f"Downloading: {progress}", end='\r') 
    elif d['status'] == 'finished':
        print("Download complete!              ")

def search_songs(query):
    ydl_opts = {
        'quiet': True,
        'default_search': 'ytsearch10',
        'skip_download': True,
        'noplaylist': True,
        'extract_flat': 'in_playlist',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        return result['entries']

def display_playlist(playlist):
    if not playlist:
        print("Your playlist is empty.")
        return
    for index, song in enumerate(playlist):
        print(f"{index+1}. {os.path.basename(song)}")

def play_song(song_path, playlist):
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        print(f"Now Playing: {os.path.basename(song_path)}")

        while True:  
            if not pygame.mixer.music.get_busy():
                break  
            command = input("Enter command (pause, resume, next, prev, exit): ").lower()
            if command == 'pause':
                pygame.mixer.music.pause()
                print("Song paused.")
                while True:  
                    command = input("Enter command (resume, next, prev, exit): ").lower()
                    if command in ['resume', 'next', 'prev', 'exit']:
                        break
                    else:
                        print("Invalid command.")
                if command == 'resume':
                    pygame.mixer.music.unpause()
                    print("Song resumed.")
            elif command == 'resume':
                print("Song is not paused.")
            elif command == 'next':
                current_index = playlist.index(song_path)
                next_index = (current_index + 1) % len(playlist)
                return playlist[next_index]
            elif command == 'prev':
                current_index = playlist.index(song_path)
                prev_index = (current_index - 1) % len(playlist)
                return playlist[prev_index]
            elif command == 'exit':
                pygame.mixer.music.stop()
                print("Exiting player.")
                return None
            else:
                print("Invalid command.")
    except pygame.error as e:
        print(f"Error playing song: {e}")

def main():
    ascii_art = r"""
 ______     __         __        __    __     __  __     ______     __     ______ 
/\  ___\   /\ \       /\ \      /\ "-./  \   /\ \/\ \   /\  ___\   /\ \   /\  ___\
\ \ \____  \ \ \____  \ \ \     \ \ \-./\ \  \ \ \_\ \  \ \___  \  \ \ \  \ \ \____
 \ \_____\  \ \_____\  \ \_\     \ \_\ \ \_\  \ \_____\  \/\_____\  \ \_\  \ \_____\
  \/_____/   \/_____/   \/_/      \/_/  \/_/   \/_____/   \/_____/   \/_/   \/_____/
    """
    print(f'{Fore.RED}{ascii_art}{Style.RESET_ALL}')
    downloads_path = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(downloads_path, exist_ok=True)
    playlist = [os.path.join(downloads_path, f) for f in os.listdir(downloads_path) if f.endswith('.mp3')]

    while True:
        github_link = URL.from_text("GitHub")
        github_link = f"\x1b]8;;{github_link}https://github.com/sankeer28/CLI-MUSIC\x1b\\{github_link}\x1b]8;;\x1b\\"
        print(f'{Fore.GREEN}{github_link}{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}Menu:{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}1. Search for a Song{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}2. View Playlist{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}3. Shuffle Playlist{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}4. Exit{Style.RESET_ALL}')

        choice = input(f'{Fore.GREEN}Enter your choice: {Style.RESET_ALL}')

        if choice == '1':
            query = input(f'{Fore.RED}Enter song title or artist (press Enter to go back): {Style.RESET_ALL}')
            if query.strip() == '':
                continue  
            results = search_songs(query)

            print("\nSearch Results:")
            for i, result in enumerate(results):
                print(f"{i+1}. {result['title']}")

            song_choice = input(f'{Fore.RED}Enter the number of the song to download (or press Enter to go back): {Style.RESET_ALL}')
            
            if song_choice.strip() == '':  
                continue  
            elif song_choice.isdigit() and 1 <= int(song_choice) <= len(results):
                selected_song = results[int(song_choice) - 1]
                download_song(selected_song['url'], downloads_path)
                playlist.append(os.path.join(downloads_path, f"{selected_song['title']}.mp3"))
                print(f"{selected_song['title']} downloaded successfully!")

        elif choice == '2':
            display_playlist(playlist)
            if playlist:
                song_index = input(f'{Fore.RED}Enter the number of the song to play (or press Enter to go back): {Style.RESET_ALL}')
                if song_index.isdigit() and 1 <= int(song_index) <= len(playlist):
                    song_path = playlist[int(song_index) - 1]
                    while song_path:
                        song_path = play_song(song_path, playlist)
                else:
                    print("Invalid song selection.")

        elif choice == '3':
            if playlist:
                random.shuffle(playlist)
                print("Playlist shuffled!")
            else:
                print("Playlist is empty.")
        elif choice == '4':
            print("Exiting Music Player. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
