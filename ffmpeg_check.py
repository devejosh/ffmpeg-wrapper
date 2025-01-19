import os
import py7zr
from pathlib import Path
import logging
import subprocess
import hashlib

# Description : This class specifically handles extraction of the ffmpeg bin files, path setting and integrity check
# Set up logging configuration
logging.basicConfig(level=logging.INFO)

class FFmpegCheck:
    def __init__(self, ffmpeg_zipped_file_path: str):
        """Initializes the FFmpegCheck class.
        
        Args:
            ffmpeg_zipped_file_path (str): Path to the zipped FFmpeg archive.
        """
        self.ffmpeg_path = ''
        self.ffmpeg_zipped_file_path = Path(ffmpeg_zipped_file_path)
        self.output_dir = Path('./ffmpeg-essential')

        # Step 1: Ensure the ffmpeg-essential.7z file exists in the project directory
        if not self.ffmpeg_zipped_file_path.exists():
            raise FileNotFoundError(f"Unable to find ffmpeg (zipped -7z) locally at: {self.ffmpeg_zipped_file_path}.")
        else:
            logging.info("FFMPEG local 7z archive found.")

    def ffmpeg_dir_check(self):
        """Check if the output directory exists and is empty. If not, create it."""
        if not self.output_dir.exists():
            logging.info(f"Directory {self.output_dir} does not exist. Creating it.")
            self.output_dir.mkdir(parents=True)
            logging.info(f"Directory {self.output_dir} created, ready to extract files.")
        else:
            logging.info(f"Directory {self.output_dir} already exists, checking if it is empty.")
            if not any(self.output_dir.iterdir()):
                logging.info("Directory is empty, ready to extract files.")
            else:
                logging.info("Directory is not empty, checking if files need to be overwritten.")

    def extract_ffmpeg(self):
        """Extract FFmpeg files from the .7z archive if not already extracted or outdated."""
        # Check for existing files before extraction and compare hashes if necessary
        extracted_files = list(self.output_dir.rglob('*'))
        
        if extracted_files:
            # Validate file integrity (using hash comparison)
            logging.info("Files already exist. Checking integrity...")
            if self.validate_files(extracted_files):
                logging.info("Files are already correctly extracted. Skipping extraction.")
                return  # Skip extraction if files match

        # If files are missing or outdated, perform extraction
        logging.info(f"Extracting FFmpeg files from {self.ffmpeg_zipped_file_path}...")
        with py7zr.SevenZipFile(self.ffmpeg_zipped_file_path, mode='r') as z:
            z.extractall(path=self.output_dir)
            logging.info("Files have been extracted.")

    def validate_files(self, extracted_files):
        """Validate if the extracted files match the expected content using file hashes."""
        # For simplicity, assume that the ffmpeg directory contains unique and identifiable files
        expected_hashes = self.get_expected_hashes()
        
        for file in extracted_files:
            # Skip directories and validate only files
            if file.is_file():
                current_hash = self.get_file_hash(file)
                if current_hash != expected_hashes.get(file.name, None):
                    logging.warning(f"File {file.name} does not match expected hash. Re-extraction required.")
                    return False
        return True

    def get_expected_hashes(self):
        """Return a dictionary of expected hashes for the FFmpeg files."""
        # These would ideally be pre-determined and provided (example: from a manifest file)
        return {
            'ffmpeg.exe': 'expected_hash_value_1',
            'ffprop.exe': 'expected_hash_value_2',
            # Add more expected file names and hash values here as necessary
        }

    def get_file_hash(self, file_path):
        """Generate an MD5 hash for a given file."""
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def ffmpeg_exe_checker(self):
        """Check if FFmpeg binary exists and is valid."""
        ffmpeg_path = self.output_dir / 'ffmpeg-essential' / 'bin' / 'ffmpeg.exe'
        if not ffmpeg_path.exists():
            raise FileNotFoundError(f"FFmpeg binary not found at: {ffmpeg_path}")
        else:
            logging.info("FFMPEG binaries found, good to go.")
            self.ffmpeg_path = ffmpeg_path

    def test_ffmpeg(self):
        """Test if FFmpeg is accessible and working."""
        logging.info("Testing FFmpeg by running the version command.")
        try:
            command = [str(self.ffmpeg_path), "-version"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            logging.info("Success!")
            logging.info(f"FFmpeg version detected: {result.stdout.splitlines()[0]}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg test failed: {e.stderr.strip()}")
            raise RuntimeError(f"FFmpeg test failed: {e.stderr.strip()}")

if __name__ == "__main__":
    # Ensure this is the correct path to the FFmpeg archive
    ffmpeg_zipped_file_path = "./ffmpeg-essential.7z"
    ffmpeg = FFmpegCheck(ffmpeg_zipped_file_path)

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
