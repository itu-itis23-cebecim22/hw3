import os
import sys
import urllib.request
import zipfile
import stat

def download_ffmpeg():
    # Create a directory for ffmpeg if it doesn't exist
    os.makedirs('ffmpeg_bin', exist_ok=True)
    
    # Download ffmpeg
    url = "https://evermeet.cx/ffmpeg/ffmpeg-6.1.zip"
    zip_path = "ffmpeg_bin/ffmpeg.zip"
    
    print("Downloading ffmpeg...")
    urllib.request.urlretrieve(url, zip_path)
    
    # Extract the zip file
    print("Extracting ffmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('ffmpeg_bin')
    
    # Make ffmpeg executable
    ffmpeg_path = 'ffmpeg_bin/ffmpeg'
    st = os.stat(ffmpeg_path)
    os.chmod(ffmpeg_path, st.st_mode | stat.S_IEXEC)
    
    # Add ffmpeg directory to PATH
    os.environ['PATH'] = os.path.abspath('ffmpeg_bin') + os.pathsep + os.environ['PATH']
    
    print("ffmpeg setup complete!")
    print(f"ffmpeg installed at: {os.path.abspath('ffmpeg_bin')}")

if __name__ == "__main__":
    download_ffmpeg()
