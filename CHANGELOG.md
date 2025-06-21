# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Documentation setup
- CI/CD configuration

## [0.1.0] - 2023-11-01

### Added
- Initial release
- Hash utilities: `stable_hash`, `md5`, `partial_file_hash`
- File utilities: `is_bad_folder_name`, `is_bad_llm_caption`
- System utilities: `suppress_stdout_stderr`, `suppress_c_stdout_stderr`
- Formatting utilities: `calculate_tokens`, `safe_format`
- Debug utilities: `get_python_execution_info`, `get_class_info`, `print_execution_info`, `print_class_info`
- Arithmetic utilities: `get_mode`
- Common patterns: `ResolutionPreset` (moved to media module), `Verbosity` (moved to separate file), `mock_when`, `fail_recover`, `custom_retry`, `BadInputException`
- Removed: `TruncatedPrettyPrinter` (use Python's standard `pprint` module instead)