import subprocess
import os
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

class FFmpegWrapper:
    def __init__(self, ffmpeg_path="ffmpeg"):
        # Ensure the given ffmpeg_path exists
        if not os.path.exists(ffmpeg_path) and ffmpeg_path != "ffmpeg":
            raise FileNotFoundError(f"FFmpeg binary not found at: {ffmpeg_path}")
        self.ffmpeg_path = ffmpeg_path

    def test_ffmpeg(self):
        """Check if the ffmpeg binary is accessible and working."""
        try:
            command = [self.ffmpeg_path, "-version"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            logging.info(f"FFmpeg version detected: {result.stdout.splitlines()[0]}")
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
    try:
        ffmpeg = FFmpegWrapper(ffmpeg_path="ffmpeg")  # Adjust path if necessary
        if ffmpeg.test_ffmpeg():
            print("FFmpeg is correctly configured and working.")

        # Extract audio for Whisper
        output_file = ffmpeg.extract_audio_for_whisper("input.mp4", "output.wav")
        print(f"Audio extracted to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
