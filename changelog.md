# Changelog

## [Unreleased]
## [1.1.0] - 2025-01-19
### Added
- **File Hash Validation for Extraction**: Implemented file hash validation to ensure that previously extracted FFmpeg files are not re-extracted if they have not changed. This prevents unnecessary re-extraction and speeds up the process.
- **File Integrity Check**: Added functionality to compare the MD5 hash of extracted files against expected hashes before deciding to extract files.
- **Cross-Platform Path Handling**: Replaced `os.path` calls with `pathlib` for consistent, cross-platform file path management.
- **FFmpeg Extraction from `.7z` Archive**: Added a method to extract FFmpeg binaries from `.7z` archive using `py7zr`.

### Fixed
- **Path Handling**: Fixed potential issues with path handling by using `pathlib.Path` consistently instead of mixing `os.path` and `pathlib`.
- **Redundant File Existence Check**: Removed redundant checks and ensured the flow of execution is streamlined.
- **Improved Error Handling**: Fixed a bug in the `run_command` method where the output was incorrectly returned when an error occurred.

## [1.1.0] - 2025-01-17
### Added
- Created `FFmpegWrapper` class to manage FFmpeg operations.
- Implemented `.7z` archive extraction for FFmpeg binaries.
- Added user prompt after FFmpeg extraction to confirm directory creation.
- Implemented extraction logic.

### Fixed
- Resolved minor issue where non-existent file paths would not raise a `FileNotFoundError`.
- Simplified CLI prompts to streamline user interaction.

---

## [1.1.0] - 2025-01-18
### Added
- **Logging Framework**: Replaced `print` statements with Python's built-in `logging` module for better flexibility and maintainability. Logging levels (`INFO`, `ERROR`, etc.) are now used for feedback.
- **Type Annotations**: Added type hints to function signatures for better clarity and improved code readability.
- **Async Command Handling**: Updated `run_async_command` and `batch_extract_audio` methods to use `asyncio.create_subprocess_exec` for non-blocking execution when running commands asynchronously.

### Changed
- **Fixed Typo in Directory Check**: Corrected `self.self.output_dir` to `self.output_dir` in the `ffmpeg_dir_check` method.
- **Refactored Directory Creation Logic**: Simplified and clarified the directory check and creation logic in the `ffmpeg_dir_check` method.
- **Removed Blocking `input()` Calls**: Removed unnecessary `input()` calls that paused execution in production code, making it more suitable for automated or headless environments.
- **Refined Error Handling**: Improved error handling to provide more specific and meaningful error messages.
- **Replaced Hardcoded File Paths**: Corrected hardcoded paths to dynamically use the class instance's `output_dir` property and the provided `ffmpeg_zipped_file_path`.

### Fixed
- **Fixed `validate_output_dir` Method**: Corrected a typo where `validate_self.output_dir` was incorrectly used instead of `validate_output_dir`.
- **Fixed Path Calculation**: Updated the `ffmpeg_exe_checker` method to dynamically calculate the correct path for `ffmpeg.exe`, ensuring it works across various setups.

### Removed
- **Deprecated `input()` Pause Calls**: Removed `input()` calls used for pausing execution during directory creation and extraction.

---

## [1.0.0] - 2025-01-17
### Added
- **Basic FFmpeg Extraction Logic**: Initial release to extract FFmpeg binaries from `.7z` archives and check if the necessary files exist.

### Fixed
- **Initial Setup**: Fixed the initial setup, ensuring that `ffmpeg_zipped_file_path` is correctly provided and checked.

