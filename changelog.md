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
- implemented extraction.

### Fixed
- Resolved minor issue where non-existent file paths would not raise a `FileNotFoundError`.
- simplified cli prompts to streamline user inteaction. 


Thank you for providing both the initial and final versions of the file. Based on the differences between the two versions, I have generated the following `changelog.md` to describe the changes made.

---


## [1.1.0] - 2025-01-17/2
### 1. **Introduction of `self.ffmpeg_path` in the Constructor**
   - **Initial Version:**
     - `self.ffmpeg_path` was not defined in the constructor.
   - **Final Version:**
     - The `__init__` method now initializes `self.ffmpeg_path` as an empty string (`self.ffmpeg_path = ''`). This ensures that `self.ffmpeg_path` is available later in the class for use.

   **Reason for Change:** To provide a place for storing the FFmpeg binary path after extraction and verification.

---

### 2. **Addition of `ffmpeg_exe_checker` Method**
   - **Initial Version:**
     - The method `ffmpeg_exe_checker` was incomplete and had a syntax error.
   - **Final Version:**
     - The method was fully implemented to check if the `ffmpeg.exe` binary exists in the expected location.
     - The method performs path manipulation to generate an absolute path to `ffmpeg.exe` and checks its existence.
     - If the file is not found, a `FileNotFoundError` is raised. If it is found, the path is saved to `self.ffmpeg_path`.

   **Reason for Change:** This method is crucial for ensuring the FFmpeg executable is available for subsequent operations, such as running FFmpeg commands.

---

### 3. **Introduction of `test_ffmpeg` Method**
   - **Initial Version:**
     - There was no method to verify if FFmpeg was working after extracting and setting the path.
   - **Final Version:**
     - The `test_ffmpeg` method was added to run `ffmpeg -version` to verify if the binary is accessible and working correctly.
     - If the FFmpeg binary is accessible, the version is printed to confirm successful detection.
     - If there are any errors, appropriate exceptions are raised to provide feedback.

   **Reason for Change:** To ensure that the FFmpeg binary works after extraction and to handle potential errors gracefully.

---

### 4. **Removal of Unused or Broken Code**
   - **Initial Version:**
     - There was an incomplete `check_ffmpeg_exe` method with a broken `if not` condition.
   - **Final Version:**
     - The method `check_ffmpeg_exe` was removed and replaced by the `ffmpeg_exe_checker` method (described above).
   
   **Reason for Change:** The new method `ffmpeg_exe_checker` is more comprehensive and replaces the broken code, ensuring clarity and correctness.

---

### 5. **General Code Refinements**
   - **Final Version:**
     - Minor adjustments in the code structure, including clearer print statements for better debugging and user feedback (e.g., confirming when directories are created, or when FFmpeg bins are found).
     - Improved exception handling and error messages, making the code more robust and user-friendly.
     - Minor cleanup of redundant `else` blocks for clearer control flow.

   **Reason for Change:** These refinements improve the readability, usability, and robustness of the code, making it easier to debug and maintain.

---

### 6. **Example Usage Section Enhancement**
   - **Initial Version:**
     - The example usage section did not call the `ffmpeg_exe_checker()` method after extraction, which would leave the path unset.
   - **Final Version:**
     - After extracting the FFmpeg files, the `ffmpeg_exe_checker()` method is now called to verify and set the `ffmpeg_path`.
     - The code now correctly prints the path of `ffmpeg.exe` and tests its functionality.

   **Reason for Change:** To ensure that the example usage is consistent with the updated logic and verifies the correct operation of FFmpeg.

---

### 7. **New Exception Handling for FFmpeg Test**
   - **Initial Version:**
     - There was no handling for FFmpeg test failures.
   - **Final Version:**
     - The `test_ffmpeg` method now catches `FileNotFoundError` and `subprocess.CalledProcessError` exceptions and provides detailed error messages.
   
   **Reason for Change:** To improve error handling and provide clearer feedback to the user if FFmpeg is not installed or cannot be executed correctly.

---

## Summary of Changes:
- **Added:** 
  - `ffmpeg_exe_checker` method for validating and setting the FFmpeg binary path.
  - `test_ffmpeg` method to verify that the FFmpeg binary is working.
- **Refined:** 
  - The overall structure of the code for better clarity and error handling.
  - Example usage to ensure the `ffmpeg_path` is correctly set and tested.
- **Removed:** 
  - Broken or incomplete methods (`check_ffmpeg_exe`).
  
Here is a **Changelog** to represent the changes made to the original code:

---


### [1.1.0] - 2025-01-18/1
#### Added:
- **Logging Framework**: Replaced `print` statements with Python's built-in `logging` module for better flexibility and maintainability. Logging levels (`INFO`, `ERROR`, etc.) are now used for feedback.
- **Type Annotations**: Added type hints to function signatures for better clarity and improved code readability.
- **Async Command Handling**: Updated `run_async_command` and `batch_extract_audio` methods to use `asyncio.create_subprocess_exec` for non-blocking execution when running commands asynchronously.

#### Changed:
- **Fixed Typo in Directory Check**: Corrected `self.self.output_dir` to `self.output_dir` in the `ffmpeg_dir_check` method.
- **Refactored Directory Creation Logic**: Simplified and clarified the directory check and creation logic in the `ffmpeg_dir_check` method.
- **Removed Blocking `input()` Calls**: Removed unnecessary `input()` calls that paused execution in production code, making it more suitable for automated or headless environments.
- **Refined Error Handling**: Improved error handling to provide more specific and meaningful error messages.
- **Replaced Hardcoded File Paths**: Corrected hardcoded paths to dynamically use the class instance's `output_dir` property and the provided `ffmpeg_zipped_file_path`.
  
#### Fixed:
- **Fixed `validate_output_dir` Method**: Corrected a typo where `validate_self.output_dir` was incorrectly used instead of `validate_output_dir`.
- **Fixed Path Calculation**: Updated the `ffmpeg_exe_checker` method to dynamically calculate the correct path for `ffmpeg.exe`, ensuring it works across various setups.
  
#### Removed:
- **Deprecated `input()` Pause Calls**: Removed `input()` calls used for pausing execution during directory creation and extraction.

