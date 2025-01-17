## [Unreleased]
### Added
- Added a method to extract FFmpeg binaries from `.7z` archive using `py7zr`.

### Fixed
- Fixed a bug in the `run_command` method where the output was incorrectly returned when an error occurred.

## [1.1.0] - 2025-01-17
### Added
- Created `FFmpegWrapper` class to manage FFmpeg operations.
- Implemented `.7z` archive extraction for FFmpeg binaries.
- Added user prompt after FFmpeg extraction to confirm directory creation.

### Fixed
- Resolved minor issue where non-existent file paths would not raise a `FileNotFoundError`.
