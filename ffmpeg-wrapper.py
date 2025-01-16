import subprocess
import os

class FFmpegWrapper:
    def __init__(self, ffmpeg_path="ffmpeg"):
        # Ensure the given ffmpeg_path exists
        if not os.path.exists(ffmpeg_path):
            raise FileNotFoundError(f"ffmpeg binary not found at: {ffmpeg_path}")
        self.ffmpeg_path = ffmpeg_path

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
    ffmpeg = FFmpegWrapper(ffmpeg_path="/usr/local/bin/ffmpeg")  # or "ffmpeg" if in PATH

    # Convert video
    stdout, stderr, returncode = ffmpeg.convert_video("input.mp4", "output.mkv")
    print(stdout, stderr, returncode)

    # Extract audio from video
    stdout, stderr, returncode = ffmpeg.extract_audio("input.mp4", "output_audio.mp3")
    print(stdout, stderr, returncode)

    # Get video info
    stdout, stderr, returncode = ffmpeg.get_video_info("input.mp4")
    print(stdout, stderr, returncode)

    # Trim video
    stdout, stderr, returncode = ffmpeg.trim_video("input.mp4", "trimmed_output.mp4", "00:01:00", "00:00:30")
    print(stdout, stderr, returncode)

    # Change video resolution
    stdout, stderr, returncode = ffmpeg.change_video_resolution("input.mp4", "output_resized.mp4", "640x360")
    print(stdout, stderr, returncode)

    # Add watermark to video
    stdout, stderr, returncode = ffmpeg.add_watermark("input.mp4", "output_with_watermark.mp4", "watermark.png", "10:10")
    print(stdout, stderr, returncode)
