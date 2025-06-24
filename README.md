# iPhone Photo Sorter

A Python script that automatically organizes iPhone photos from DCIM subfolders into year-based directories. This tool helps you sort through large collections of iPhone photos by extracting them from their original DCIM folder structure and organizing them by year.

## Features

- 📁 Automatically detects year-based DCIM subfolders
- 📅 Organizes photos into year-based directories
- 📊 Shows progress bar during file copying
- 🔒 Safe copying (preserves original files until manual confirmation)
- 🖥️ User-friendly GUI for folder selection
- ✅ Manual verification step before deletion of originals

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Step 1: Install pip (if not already installed)

#### Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"
3. pip should be installed automatically with Python 3.4+

To verify pip is installed:
```bash
pip --version
```

#### macOS:
```bash
# If you have Python but not pip
python -m ensurepip --upgrade

# Or install via Homebrew
brew install python
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3-pip
```

#### Linux (CentOS/RHEL/Fedora):
```bash
# CentOS/RHEL
sudo yum install python3-pip

# Fedora
sudo dnf install python3-pip
```

### Step 2: Install Required Dependencies

```bash
pip install tqdm
```

Or if you're using Python 3 specifically:
```bash
pip3 install tqdm
```

**Note:** The script also uses the following built-in Python libraries (no installation needed):
- `os`
- `shutil` 
- `pathlib`
- `tkinter`

## Usage

### Step 1: Prepare Your Photos
1. Copy all iPhone DCIM subfolders to a single directory on your computer
2. Ensure the subfolders follow the naming pattern where the first 4 characters represent the year (e.g., "2023__IMPORTED", "2024_Photos", etc.)

### Step 2: Run the Script
```bash
python apple-pic-sorter.py
```

### Step 3: Follow the GUI Prompts
1. **Select Source Folder**: Choose the folder containing all your iPhone DCIM subfolders
2. **Select Destination**: Choose where you want the organized backup to be created
3. **Wait for Processing**: The script will copy all files with a progress bar
4. **Manual Verification**: Check the created 'Iphone_Photo_Backup' folder
5. **Confirm Deletion**: Type 'YES' to delete the original folders (optional)

## How It Works

1. **Folder Detection**: Scans the source directory for subfolders starting with 4-digit years
2. **Year Extraction**: Extracts unique years from folder names
3. **Structure Creation**: Creates an 'Iphone_Photo_Backup' directory with year-based subfolders
4. **File Copying**: Recursively copies all files from source subfolders to appropriate year directories
5. **Safe Deletion**: Only deletes originals after manual confirmation

## Example Directory Structure

### Before (Input):
```
iPhone_Photos/
├── 2021__IMPORTED/
│   ├── IMG_001.jpg
│   └── IMG_002.mov
├── 2022_Backup/
│   ├── IMG_003.jpg
│   └── IMG_004.jpg
└── 2023_Photos/
    ├── IMG_005.jpg
    └── IMG_006.mov
```

### After (Output):
```
Destination_Folder/
└── Iphone_Photo_Backup/
    ├── 2021/
    │   ├── IMG_001.jpg
    │   └── IMG_002.mov
    ├── 2022/
    │   ├── IMG_003.jpg
    │   └── IMG_004.jpg
    └── 2023/
        ├── IMG_005.jpg
        └── IMG_006.mov
```

## Safety Features

- ✅ **Non-destructive copying**: Original files are preserved until manual confirmation
- ✅ **Error handling**: Continues processing even if individual files fail to copy
- ✅ **Progress tracking**: Visual progress bar shows copying status
- ✅ **Manual verification**: Requires user confirmation before deleting originals

## Troubleshooting

### Common Issues:

**"No module named 'tqdm'"**
```bash
pip install tqdm
```

**"tkinter not found" (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

**Permission Errors**
- Ensure you have read access to source folders
- Ensure you have write access to destination folder
- Run terminal/command prompt as administrator if needed

**No GUI dialogs appear**
- Ensure you're running in a graphical environment
- On remote servers, consider using X11 forwarding or modify script for command-line input

## Requirements File

If you want to create a requirements.txt file:
```
tqdm>=4.64.0
```

Then install with:
```bash
pip install -r requirements.txt
```

## License

This script is provided as-is for personal use. Modify and distribute freely.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.