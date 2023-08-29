# Import necessary libraries
from pytube import YouTube, Playlist
import subprocess
import eyed3
import requests
import os
import re

# Function to get YouTube URL from user
def get_url():
    validate_url = input('Enter a Youtube URL: ')
    return validate_url

# Function to download a single track or playlist tracks
def get_track():
    # Define regular expression patterns for playlist and track URLs
    playlist_pattern = re.compile(r'^https://www\.youtube\.com/playlist\?list=([A-Za-z0-9_-]+)')
    track_pattern = re.compile(r'^https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]+)')
    
    url = get_url()  # Get user input
    
    # Check if the URL matches a track or playlist pattern
    if track_pattern.match(url):
        yt = YouTube(url)
        print('------------------------Collecting data---------------------------')
        track = yt.streams.filter(only_audio=True).first()
        print('------------------------Successfully downloaded---------------------------')
        return track.download()
    elif playlist_pattern.match(url):
        playlist = Playlist(url)
        for track_url in playlist.video_urls():
            yt = YouTube(track_url)
            stream = yt.streams.filter(only_audio=True).first()
            stream.download()
            print(f'--------------Downloaded {yt.title} from {playlist.title} playlist--------------')

# Function to convert downloaded track to mp3 format and delete original
def convert_track_to_mp3():
    track_path = get_track()  # Get the path of the downloaded track

    # Prepare filenames and paths for the converted mp3 track
    base_filename = os.path.splitext(os.path.basename(track_path))[0]
    output_filename = os.path.join(os.path.dirname(track_path), f'{base_filename}.mp3')
    
    # Provide the full path to the ffmpeg executable (replace with your actual path)
    ffmpeg_executable = r'C:\Users\hp\anaconda3\envs\newenv001\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win64-v4.2.2.exe'
    
    # Define the ffmpeg command to convert the track
    ffmpeg_cmd = [
        ffmpeg_executable,
        '-i', track_path,
        '-vn',
        '-acodec', 'libmp3lame',
        '-ab', '192k',
        '-ar', '44100',
        '-y',
        output_filename
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True)  # Run the ffmpeg command
        print('--------------Successfully Converted!--------------')
        os.remove(track_path)  # Remove the original MP4 file
        print(f'Deleted original MP4 file: {track_path}')
    except subprocess.CalledProcessError as e:
        print('--------------Conversion Failed!--------------')

# Main function to handle user interactions
def main():
    while True:
        option = input("Enter 's' to download a single track, 'p' to download a playlist, or 'q' to quit: ")
        
        if option == 'q':
            print("Quitting the script...")
            break
        elif option == 's' or option == 'p':
            convert_track_to_mp3()  # Convert and process track based on user option
        else:
            print("Invalid option. Please enter 's', 'p', or 'q'.")

# Start the script by calling the main function
if __name__ == "__main__":
    main()
