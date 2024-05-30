'''
Simple youtube downloader for mp4 & mp3 formats
Enter your directory on line 45 under 'def download_video' by simply by copying the desired address from the explorer
might require installation of modules
This program was made as a part of my python studies and is not complete or made for an end user
'''

import os
import time
import re
from pytube import YouTube
from moviepy.editor import VideoFileClip

def validate_youtube_url(url): # validates copied url
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    pattern = re.compile(youtube_regex)

    if re.match(pattern, url):
        return True
    else:
        return False

def on_progress_callback(stream, chunk, bytes_remaining): # progress bar
    bytes_downloaded = stream.filesize - bytes_remaining
    percent_downloaded = bytes_downloaded / stream.filesize * 100
    print(f"Download progress: {percent_downloaded:.2f}%")


# not used yet
def get_output_directory():
    output_directory = input("Enter the output directory: ")
    while not os.path.exists(output_directory) or not os.path.isdir(output_directory):
        print("Invalid directory. Please try again.")
        output_directory = input("Enter the output directory: ")
    return output_directory

def sanitize_title(title): # sanitizing title so that the name contains no errors for windows directories
    return re.sub(r'[\\/:*?"<>|]', '', title)

def download_video(output_format):
    output_directory = r"-Your output adress here-"  # !-------- Default output directory here ---------!

# have not fully finished the output directory input save function, please copy paste above.
    if not os.path.exists(output_directory):
        print(f"Output directory '{output_directory}' does not exist.")
        output_directory = get_output_directory()
    else:
        print(f"Using output directory: {output_directory}")

    video_file_path = os.path.join(output_directory, "temp.mp4")

    url = input("Paste YouTube URL: ")
    while not validate_youtube_url(url):
        print("Invalid YouTube URL. Please try again.")
        url = input("Paste YouTube URL: ")

    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            print(f"Output directory '{output_directory}' created.")

        video = YouTube(url, on_progress_callback=on_progress_callback)
        stream = video.streams.get_highest_resolution()

        if output_format == 'mp3':
            print("Downloading video...")
            stream.download(output_path=output_directory, filename="temp.mp4")
            print("Video downloaded successfully.")

            timeout = 60
            start_time = time.time()
            while time.time() - start_time < timeout:
                if os.path.exists(video_file_path):
                    break
                time.sleep(1)

            if not os.path.exists(video_file_path):
                raise TimeoutError("Timeout waiting for the downloaded file.")

            video_clip = VideoFileClip(video_file_path)
            title = video.title.replace('/', '_').replace('?', '')
            title = sanitize_title(title)
            output_file_path = os.path.join(output_directory, f"{title}.mp3")
            print("Converting to MP3...")
            video_clip.audio.write_audiofile(output_file_path, codec='mp3')
            print(f"Downloaded and converted video to MP3: {output_file_path}")

        elif output_format == 'mp4':
            print("Downloading video...")
            stream.download(output_path=output_directory, filename="temp.mp4")
            print("Video downloaded successfully.")
            os.rename(video_file_path, os.path.join(output_directory, f"{video.title}.mp4"))
            print(f"Downloaded video: {video.title}.mp4")

        else:
            print("Invalid output format.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        if 'video_clip' in locals():  # Stop using temp file for cleanup
            video_clip.close()

        if os.path.exists(video_file_path): # removes the temp file
            os.remove(video_file_path)
            print("Temporary file deleted.")

    with open("output_directory.txt", "w") as file:
        file.write(output_directory)
        print("Output directory saved in the code.")

def main(): # main loop for menu & inputs
    while True:
        print("Select the output format:")
        print("1. MP3")
        print("2. MP4")
        choice = input("Enter your choice (1/2): ")

        if choice == '1':
            download_video('mp3')
        elif choice == '2':
            download_video('mp4')
        else:
            print("Invalid choice.")


        while True:
            response = input("Do you want to download another video? (yes/no): ").lower()
            if response in ('yes', 'no'):
                break
            else:
                print("Invalid response. Please enter 'yes' or 'no'.")

        if response == 'no':
            break

main()