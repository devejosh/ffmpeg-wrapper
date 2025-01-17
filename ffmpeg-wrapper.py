# Imports 
import subprocess
import os
import py7zr
from pathlib import Path

class FFmpegWrapper:
    

    #if the repo is cloned as is, it will have a zipped file .7z containing the ffmpeg local libs, we need to extract them first.
    #I am using py7zr for this purpose. 

    def __init__(self, ffmpeg_zipped_file_path):
        # defining self.ffmpeg_path as an empty variable. It will house the ffmpeg path later 
        self.ffmpeg_path = ''

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
            print ("Files have been extracted.")

    #FFMPEG.exe check
    def ffmpeg_exe_checker(self):
        #performing some path manuplation to get an absolute path to the bins. 
        ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg-essential','ffmpeg-essential', 'bin', 'ffmpeg.exe')
        if not os.path.exists(ffmpeg_path) and ffmpeg_path != "ffmpeg-essential/bin/ffmpeg.exe":
            raise FileNotFoundError(f"FFmpeg binary not found at: {ffmpeg_path}")
        else:
            print ("FFMPEG bins found, good to go.")
            self.ffmpeg_path = ffmpeg_path


    def test_ffmpeg(self):
        """Check if that ffmpeg binary is accessible and working."""
        print ("testing ffmpeg by running the version command.")
        try:
            command = [self.ffmpeg_path, "-version"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            print ("Success!")
            print(f"FFmpeg version detected: {result.stdout.splitlines()[0]}")
            return True
        except FileNotFoundError:
            raise FileNotFoundError("FFmpeg binary not found. Ensure it is installed and accessible in PATH.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg test failed: {e.stderr.strip()}")


    def run_command(self, command):
        """Runs a command and returns stdout, stderr, returncode."""
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            logging.info("Command succeeded: %s", " ".join(command))
            return result.stdout, result.stderr, result.returncode
        except subprocess.CalledProcessError as e:
            logging.error("Command failed: %s", " ".join(command))
            logging.error("Error: %s", e.stderr)
            raise RuntimeError(f"FFmpeg command failed: {e.stderr.strip()}") from e

    def validate_file(self, file_path):
        """Ensure the input file exists."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

    def validate_output_dir(self, file_path):
        """Ensure the output directory is writable."""
        output_dir = os.path.dirname(file_path) or "."
        if not os.access(output_dir, os.W_OK):
            raise PermissionError(f"Cannot write to directory: {output_dir}")

    def extract_audio_for_whisper(self, input_file, output_audio_file):
        """Extract audio in a Whisper-compatible format."""
        self.validate_file(input_file)
        self.validate_output_dir(output_audio_file)
        
        command = [
            self.ffmpeg_path, "-i", input_file,
            "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
            output_audio_file
        ]
        stdout, stderr, returncode = self.run_command(command)
        if returncode == 0:
            return output_audio_file
        else:
            raise RuntimeError(f"Failed to extract audio: {stderr}")

    async def run_async_command(self, command):
        """Run a command asynchronously."""
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode(), stderr.decode(), process.returncode

    async def batch_extract_audio(self, input_files, output_dir):
        """Extract audio for multiple files asynchronously."""
        tasks = []
        for input_file in input_files:
            output_audio_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".wav")
            self.validate_file(input_file)
            self.validate_output_dir(output_audio_file)
            
            command = [
                self.ffmpeg_path, "-i", input_file,
                "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
                output_audio_file
            ]
            tasks.append(self.run_async_command(command))
        return await asyncio.gather(*tasks)


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

        #Extraction complete! Now, checking if we are able to access ffmpeg.exe
        ffmpeg.ffmpeg_exe_checker()

        print(f"this will now act as the path for ffempg : {ffmpeg.ffmpeg_path}")
        ffmpeg.test_ffmpeg()

    except Exception as e:
        print (f"Hitting an exception : {e}")
