# iPhone Photo Sorter 📱📸

A powerful and user-friendly Python application with GUI for organizing iPhone photos from DCIM folders into year-based directories. This tool automatically sorts your iPhone photos while maintaining a comprehensive log of all operations.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🖥️ **Modern GUI Interface**
- Clean, intuitive user interface with real-time progress tracking
- Preview mode to analyze folders before processing
- Live status updates and detailed progress visualization
- Responsive design that works on all screen sizes

### 📊 **Comprehensive Logging System**
- **Detailed log files** automatically saved in the backup directory
- **Timestamped entries** with complete operation history
- **Summary statistics** including success rates and file counts
- **Real-time status display** in the application window
- **Error tracking** with detailed failure reports

### 🔄 **Smart Backup Management**
- **Automatic detection** of existing `Iphone_Photo_Backup` folders
- **Intelligent merging** with existing year-based directories
- **Duplicate detection** - skips files that already exist with identical content
- **Conflict resolution** - creates unique names for different files with same filename

### 📁 **Advanced File Handling**
- **Year-based organization** from DCIM folder names (e.g., 2023ABCD → 2023/)
- **Recursive file discovery** - finds photos in nested subdirectories
- **File integrity verification** using size comparison
- **Progress tracking** with files processed counter

### 🛡️ **Safety & Security Features**
- **Preview mode** - see exactly what will happen before starting
- **Double confirmation** before deleting original files
- **Comprehensive error handling** with graceful failure recovery
- **Backup verification** tools and detailed logs for peace of mind

## 🚀 Getting Started

### Option 1: Executable Version (Recommended)
**Download the pre-built executable** - No Python installation required!
- Windows: `iPhone_Photo_Sorter.exe`
- Simply double-click to run

### Option 2: Python Source Code
**Requirements:**
- Python 3.7 or higher
- Standard library modules (no additional installations needed)

**Run from source:**
```bash
python apple-pic-sorter.py
```

## 📖 How to Use

### Step 1: Launch the Application
- **Executable**: Double-click the `.exe` file
- **Python**: Run `python apple-pic-sorter.py`

### Step 2: Select Folders
1. **Source Folder**: Choose the folder containing your iPhone DCIM subfolders
   - Example: `iPhone_Import/` containing `2023ABCD/`, `2024EFGH/`, etc.
2. **Destination**: Choose where the organized backup should be created
   - The app will create `Iphone_Photo_Backup/` in this location

### Step 3: Analyze Before Processing
- Click **"Analyze Folders"** to preview the operation
- Review the analysis results showing:
  - Number of files to process
  - Years that will be created
  - Existing backup status
  - File breakdown by year

### Step 4: Start Sorting
- Click **"Start Sorting"** to begin the organization process
- Monitor real-time progress with the progress bar
- View live status updates in the status window

### Step 5: Review Results
- Check the comprehensive log file for detailed operation results
- Verify your photos are properly organized in year folders
- Optionally delete the original folder after verification

## 📂 Folder Structure

### Before Sorting:
```
iPhone_Import/
├── 2023ABCD/
│   ├── IMG_001.jpg
│   ├── IMG_002.mov
│   └── ...
├── 2023EFGH/
│   ├── IMG_100.jpg
│   └── ...
└── 2024IJKL/
    ├── IMG_200.jpg
    └── ...
```

### After Sorting:
```
Backup_Location/
└── Iphone_Photo_Backup/
    ├── 2023/
    │   ├── IMG_001.jpg
    │   ├── IMG_002.mov
    │   ├── IMG_100.jpg
    │   └── ...
    ├── 2024/
    │   ├── IMG_200.jpg
    │   └── ...
    └── photo_sort_log_20240624_143022.log
```

## 📋 Log File Information

Each operation creates a detailed log file with:
- **Operation timestamp and duration**
- **Source and destination paths**
- **File processing statistics**
- **Error reports and warnings**
- **Final folder structure summary**
- **Success rate calculations**

Example Log Entry:
```
2024-06-24 14:30:22,123 - INFO - === iPhone Photo Sorting Started ===
2024-06-24 14:30:22,124 - INFO - Source: C:\iPhone_Import
2024-06-24 14:30:22,125 - INFO - Destination: C:\Backup\Iphone_Photo_Backup
2024-06-24 14:30:22,126 - INFO - Found 1,245 files to process
2024-06-24 14:30:22,127 - INFO - Created/verified year folders: 2023, 2024
```

## ⚡ Technical Specifications

### System Requirements
- **Operating System**: Windows 7+, macOS 10.12+, or Linux
- **Memory**: 50MB RAM minimum
- **Storage**: Sufficient space for photo backup (2x source folder size recommended)
- **Python**: 3.7+ (if running from source)

### Performance
- **Processing Speed**: ~100-500 files per second (depending on file sizes and storage speed)
- **Memory Usage**: Low memory footprint, processes files one at a time
- **Storage Efficiency**: Only copies files, no unnecessary duplication

### Supported File Types
- **All file types** found in iPhone DCIM folders
- Common formats: `.jpg`, `.jpeg`, `.png`, `.mov`, `.mp4`, `.heic`, `.aae`
- **Preserves file metadata** including creation dates and EXIF data

## 🛠️ Troubleshooting

### Common Issues

**"No valid year-based folders found"**
- Ensure your DCIM folders start with 4-digit years (e.g., `2023ABCD`)
- Check that subfolders actually contain the expected format

**"Permission denied" errors**
- Run as administrator (Windows) or with `sudo` (macOS/Linux)
- Ensure you have write permissions to the destination folder

**Application won't start**
- **Executable**: Try running from command prompt to see error messages
- **Python**: Ensure Python 3.7+ is installed: `python --version`

**Slow performance**
- Close other applications to free up system resources
- Ensure adequate free disk space (2x source folder size)
- Use local drives rather than network locations for better speed

### Getting Help
1. Check the log file for detailed error information
2. Ensure all file paths are accessible and have proper permissions
3. Try running with a smaller test folder first
4. Verify that the source folder structure matches expected iPhone DCIM format

## 📝 File Versions

This package includes:

### 🔥 **Executable Version**
- **iPhone_Photo_Sorter.exe** - Standalone Windows executable
- No Python installation required
- Double-click to run immediately
- All dependencies included

### 📄 **Python Source Code**
- **apple-pic-sorter.py** - Complete Python source code
- Fully commented and documented
- Cross-platform compatibility
- Customizable and extensible

## 🔒 Privacy & Security

- **No internet connection required** - works completely offline
- **No data transmission** - all processing happens locally
- **File integrity preservation** - maintains original file properties
- **Safe operation** - creates copies, never modifies originals
- **Transparent logging** - complete operation audit trail

## 🤝 Contributing

This tool is designed to be reliable and user-friendly. If you encounter any issues or have suggestions for improvements:

1. Check the log files for detailed error information
2. Verify your folder structure matches the expected iPhone DCIM format
3. Ensure proper file permissions for both source and destination
4. Test with a small sample folder first

## 📄 License

This software is provided as-is for personal use. Feel free to modify the Python source code for your specific needs.

---

**Made with ❤️ for iPhone users who want organized photo libraries**

*Last updated: June 2024*