import logging
from ffmpeg_check import FFmpegCheck  # Import FFmpegCheck

class ffmpeg_setup:
    def __init__(self, ffmpeg_zipped_file_path: str):
        """Initializes the ffmpeg_core class with FFmpegCheck."""
        # Initialize the FFmpegCheck class with the zipped FFmpeg file path
        self.ffmpeg_check = FFmpegCheck(ffmpeg_zipped_file_path)
        self.ffmpeg_path = None  # To store the path of the FFmpeg binary


if __name__ == "__main__":
    # Define the path to the FFmpeg 7z archive
    ffmpeg_zipped_file_path = "./ffmpeg-essential.7z"  # Modify this to your actual path
    
    # Create an instance of the ffmpeg_core class
    ffmpeg_instance = ffmpeg_setup(ffmpeg_zipped_file_path)

    #check ffmpeg-dir
    ffmpeg_instance.ffmpeg_check.ffmpeg_dir_check()
    logging.info("Directory check passed, ready to extract.")

    # Perform extraction
    ffmpeg_instance.ffmpeg_check.extract_ffmpeg()

    # Check if ffmpeg.exe is accessible
    ffmpeg_instance.ffmpeg_check.ffmpeg_exe_checker()

    logging.info(f"FFmpeg path set to: {ffmpeg_instance.ffmpeg_check.ffmpeg_path}")

    # Test FFmpeg
    ffmpeg_instance.ffmpeg_check.test_ffmpeg()
    logging.info("Test complete, you are good to go!")
