import subprocess
import os
import py7zr
from pathlib import Path
import logging
import asyncio

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

class FFmpegWrapper:
    def __init__(self, ffmpeg_zipped_file_path: str):
        # Define the path for FFmpeg binary and the zipped file.
        self.ffmpeg_path = ''
        self.ffmpeg_zipped_file_path = ffmpeg_zipped_file_path
        self.output_dir = './ffmpeg-essential'

        # Step 1: Ensure the ffmpeg-essential.7z file exists in the project directory
        if not os.path.exists(self.ffmpeg_zipped_file_path):
            raise FileNotFoundError(f"Unable to find ffmpeg (zipped -7z) locally at: {self.ffmpeg_zipped_file_path}.")
        else:
            logging.info("FFMPEG local 7z archive found.")

    def ffmpeg_dir_check(self):
        """Check if output directory exists; if not, create it."""
        if not os.path.exists(self.output_dir):
            logging.info("Directory /ffmpeg-essential does not exist. Creating it.")
            os.makedirs(self.output_dir)
            logging.info("Directory created, ready to extract files.")
        else:
            logging.info("Directory already exists, checking if it is empty.")
            if not any(Path(self.output_dir).iterdir()):
                logging.info("Directory is empty, ready to extract files.")
            else:
                logging.info("Directory is not empty, files would have to be overwritten.")

    def extract_ffmpeg(self):
        """Extract FFmpeg files from the .7z archive."""
        logging.info(f"Extracting FFmpeg files from {self.ffmpeg_zipped_file_path}...")
        with py7zr.SevenZipFile(self.ffmpeg_zipped_file_path, mode='r') as z:
            z.extractall(path=self.output_dir)  # Extract all files to the output directory
        logging.info("Files have been extracted.")

    def ffmpeg_exe_checker(self):
        """Check if FFmpeg binary exists and is valid."""
        ffmpeg_path = os.path.join(self.output_dir, 'ffmpeg-essential', 'bin', 'ffmpeg.exe')
        if not os.path.exists(ffmpeg_path):
            raise FileNotFoundError(f"FFmpeg binary not found at: {ffmpeg_path}")
        else:
            logging.info("FFMPEG bins found, good to go.")
            self.ffmpeg_path = ffmpeg_path

    def test_ffmpeg(self):
        """Test if FFmpeg is accessible and working."""
        logging.info("Testing FFmpeg by running the version command.")
        try:
            command = [self.ffmpeg_path, "-version"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            logging.info("Success!")
            logging.info(f"FFmpeg version detected: {result.stdout.splitlines()[0]}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg test failed: {e.stderr.strip()}")
            raise RuntimeError(f"FFmpeg test failed: {e.stderr.strip()}")

    def run_command(self, command):
        """Run a command and return stdout, stderr, returncode."""
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            logging.info(f"Command succeeded: {' '.join(command)}")
            return result.stdout, result.stderr, result.returncode
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {' '.join(command)}")
            logging.error(f"Error: {e.stderr}")
            raise RuntimeError(f"FFmpeg command failed: {e.stderr.strip()}") from e

    def validate_file(self, file_path: str):
        """Ensure the input file exists."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

    def validate_output_dir(self, file_path: str):
        """Ensure the output directory is writable."""
        self.output_dir = os.path.dirname(file_path) or "."
        if not os.access(self.output_dir, os.W_OK):
            raise PermissionError(f"Cannot write to directory: {self.output_dir}")

    def extract_audio_for_whisper(self, input_file: str, output_audio_file: str):
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

    async def batch_extract_audio(self, input_files):
        """Extract audio for multiple files asynchronously."""
        tasks = []
        for input_file in input_files:
            output_audio_file = os.path.join(self.output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".wav")
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
    # Added the static path to the local ffmpeg-bins. Please do not change it 
    # Note: This is a static path to FFmpeg; the wrapper was specifically made to work with local FFmpeg bins without the need to install FFmpeg globally.

    ffmpeg_zipped_file_path = "./ffmpeg-essential.7z"  # Ensure this is correct
    ffmpeg = FFmpegWrapper(ffmpeg_zipped_file_path)

    logging.info("Checking if output dir './ffmpeg-essential' exists, and if it is empty.")
    try:
        ffmpeg.ffmpeg_dir_check()
        logging.info("Directory check passed, ready to extract.")

        # Perform extraction
        ffmpeg.extract_ffmpeg()

        # Check if ffmpeg.exe is accessible
        ffmpeg.ffmpeg_exe_checker()

        logging.info(f"FFmpeg path set to: {ffmpeg.ffmpeg_path}")

        # Test FFmpeg
        ffmpeg.test_ffmpeg()

    except Exception as e:
        logging.error(f"An exception occurred: {e}")
