# SyncBack Pro Second Chance: Automated Filepath Scraper and Archiver

![SyncBackPro](https://github.com/steliospavlidis/SyncBackPro/assets/138578903/79c16156-b8ed-4e8a-914f-c182e7f4a1ad)

## Overview

SyncBack Pro Second Chance reads the HTML log that SyncBack Pro exports, pulls out every file path listed in it, and can bundle those files into a single ZIP archive. Use it to grab a second copy of exactly the files a backup run reported, for example the ones that failed or were skipped.

## Features

- **Path extraction:** parses the SyncBack HTML log and saves every file path to a dated text log.
- **ZIP archive:** optionally zips every listed file, **keeping its folder structure** (`C:\Data\a.txt` → `C/Data/a.txt`), so files with the same name never overwrite each other.
- **Missing-file report:** paths that no longer exist are written to `not_found.txt`.
- **Statistics:** shows how many paths were found and how many files were zipped.

## Requirements

```bash
pip3 install beautifulsoup4
```

## Usage

```bash
python3 SyncBack.py
```

1. Enter the path to the SyncBack HTML log file when asked.
2. The script prints how many file paths it found and saves them to `extracted_values_log_<date>_<n>.txt`.
3. Answer `yes` to zip those files into `log_files_<timestamp>.zip`. Any missing files are listed in `not_found.txt`.

## License

[GPL-3.0](LICENSE)
