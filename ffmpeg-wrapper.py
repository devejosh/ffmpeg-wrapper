# Imports 
import subprocess
import os
import py7zr
from pathlib import Path

class FFmpegWrapper:

    #if the repo is cloned as is, it will have a zipped file .7z containing the ffmpeg local libs, we need to extract them first.
    #I am using py7zr for this purpose. 

    def __init__(self, ffmpeg_zipped_file_path):
         # Step 1 : Make sure the ffmpeg-essential.7z file is in project dir
        if not os.path.exists(ffmpeg_zipped_file_path):
            raise FileNotFoundError(f"Unable to find ffmpeg (zipped -7z) locally at: {ffmpeg_zipped_file_path}.")
            print ("what to do : Check your project directory and make sure ffmpeg-essential.7z is present.")
        
        else:
            print ("FFMPEG local 7z archive found.")
            #Now that its ensured we have local archive of ffmpeg bins present, begin extraction of the files into the project dir

    
    #method definition for using py7zr to extract the ffmpeg-archive
    def ffmpeg_dir_check (self, ffmpeg_zipped_file_path, output_dir):
        #first, check if ./ffmpeg-essential (dir) exists, if not, create one. 
        if not os.path.exists(output_dir):
            print ("directory /ffmpeg-essential does not exist. creating it.")
            #create the directory. 
            os.makedirs(output_dir)
            input("Directory created, ready to extract files")
        else:
            print("Directory already exists, checking if the directory is empty")
            if not any (Path(output_dir).iterdir()):
                print ("Directory is empty, ready to extract files")
            else:
                print ("Directory is not empty, the files would have to be overwritten")


    # FFMPEG EXTRACTOR CORE 
    def extract_ffmpeg(self, ffmpeg_zipped_file_path, output_dir):
        # Open the .7z file in read mode and extract
        with py7zr.SevenZipFile(ffmpeg_zipped_file_path, mode='r') as z:
            z.extractall(path=output_dir)  # Extract all files to the output directory



    def run_command(self, command):
        """Runs a command and returns stdout, stderr, returncode."""
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            return result.stdout, result.stderr, result.returncode
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr, e.returncode
    
    def convert_video(self, input_file, output_file, codec="libx264", crf=23, audio_codec="aac", audio_bitrate="192k"):
        """Convert a video file to a different format."""
        command = [
            self.ffmpeg_path, "-i", input_file,
            "-c:v", codec, "-crf", str(crf),
            "-c:a", audio_codec, "-b:a", audio_bitrate,
            output_file
        ]
        return self.run_command(command)

    def extract_audio(self, input_file, output_audio_file, audio_codec="aac", audio_bitrate="192k"):
        """Extract audio from a video file."""
        command = [
            self.ffmpeg_path, "-i", input_file,
            "-vn", "-c:a", audio_codec, "-b:a", audio_bitrate,
            output_audio_file
        ]
        return self.run_command(command)
    
    def get_video_info(self, input_file):
        """Get detailed information about a video file."""
        command = [
            self.ffmpeg_path, "-i", input_file,
            "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams"
        ]
        return self.run_command(command)
    
    def trim_video(self, input_file, output_file, start_time, duration):
        """Trim a video from the start time for the given duration."""
        command = [
            self.ffmpeg_path, "-i", input_file,
            "-ss", start_time, "-t", duration,
            "-c", "copy", output_file
        ]
        return self.run_command(command)

    def change_video_resolution(self, input_file, output_file, resolution="1280x720"):
        """Change the resolution of the video."""
        command = [
            self.ffmpeg_path, "-i", input_file,
            "-s", resolution, "-c:v", "libx264", "-c:a", "aac",
            output_file
        ]
        return self.run_command(command)

    def add_watermark(self, input_file, output_file, watermark_image, position="top-left"):
        """Add a watermark to a video."""
        command = [
            self.ffmpeg_path, "-i", input_file,
            "-i", watermark_image, "-filter_complex", f"overlay={position}",
            output_file
        ]
        return self.run_command(command)


# Example Usage
if __name__ == "__main__":
    # Added the static path to the local ffmpeg-bins. please do not change it 
    # Note : This is a static path to FFMPEG, the wrapper was specifically made to work with local ffmpeg bins without the need to install ffmpeg globally. 
    ffmpeg_zipped_file_path="./ffmpeg-essential.7z"

    #Class initialized.
    ffmpeg = FFmpegWrapper(ffmpeg_zipped_file_path)
    #We checked and found the 7z file, good, lets set the output directory to tell py7zr where to extract the files. 
    
    print ("Checking if output dir - ./ffmpeg-wrapper exists, if it does, is it empty?")
    output_dir='./ffmpeg-essential'
    try:
        ffmpeg.ffmpeg_dir_check(ffmpeg_zipped_file_path, output_dir)
        input ("directory check passed : waiting to proceed further")

        #directory check complete, performing extraction
        ffmpeg.extract_ffmpeg(ffmpeg_zipped_file_path, output_dir)

    except Exception as e:
        print (f"Hitting an exception : {e}")
