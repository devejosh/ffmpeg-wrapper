import os
import subprocess
import logging
from ffmpeg_setup import ffmpeg_setup  # Importing the ffmpeg_setup class
import asyncio

class ffmpeg_wrapper_core:

    def __init__(self):
    
        

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

if __name__ == "__main__":
    wrapper_core  = ffmpeg_wrapper_core()
