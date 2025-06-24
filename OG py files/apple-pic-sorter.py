import os
import shutil
import datetime
import logging
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from collections import defaultdict

class PhotoSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("iPhone Photo Sorter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.backup_root = None
        self.logger = None
        self.log_file_path = None
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'copied_files': 0,
            'failed_files': 0,
            'existing_files': 0,
            'years_processed': set()
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="iPhone Photo Sorter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Source folder selection
        ttk.Label(main_frame, text="Source Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.source_folder, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=1, column=2, padx=5)
        
        # Destination folder selection
        ttk.Label(main_frame, text="Destination:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.destination_folder, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_destination).grid(row=2, column=2, padx=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        preview_frame.columnconfigure(0, weight=1)
        
        # Preview text
        self.preview_text = tk.Text(preview_frame, height=8, wrap=tk.WORD)
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(1, weight=1)
        
        # Progress bar
        ttk.Label(progress_frame, text="Progress:").grid(row=0, column=0, sticky=tk.W)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready")
        self.progress_label.grid(row=0, column=2, padx=5)
        
        # Status text
        self.status_text = tk.Text(progress_frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
        status_scrollbar = ttk.Scrollbar(progress_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        status_scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.analyze_button = ttk.Button(button_frame, text="Analyze Folders", command=self.analyze_folders)
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        self.start_button = ttk.Button(button_frame, text="Start Sorting", command=self.start_sorting, state=tk.DISABLED)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(button_frame, text="Delete Original", command=self.delete_original, state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Open Log File", command=self.open_log_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(3, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
    def browse_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder with iPhone DCIM Subfolders")
        if folder:
            self.source_folder.set(folder)
            
    def browse_destination(self):
        folder = filedialog.askdirectory(title="Select Destination for Backup Folder")
        if folder:
            self.destination_folder.set(folder)
            
    def log_message(self, message, level=logging.INFO):
        """Add message to both log file and status display"""
        if self.logger:
            self.logger.log(level, message)
            
        # Update status display
        self.status_text.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
        
    def setup_logging(self):
        """Setup logging to file in the backup directory"""
        if not self.backup_root:
            return
            
        # Create log file path
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file_path = os.path.join(self.backup_root, f"photo_sort_log_{timestamp}.log")
        
        # Setup logger
        self.logger = logging.getLogger('PhotoSorter')
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def extract_unique_years(self, folder_names):
        """Extract years from folder names"""
        years = {name[:4] for name in folder_names if len(name) >= 4 and name[:4].isdigit()}
        return sorted(years)
        
    def analyze_folders(self):
        """Analyze source folder and show preview"""
        if not self.source_folder.get():
            messagebox.showerror("Error", "Please select a source folder first.")
            return
            
        if not self.destination_folder.get():
            messagebox.showerror("Error", "Please select a destination folder first.")
            return
            
        try:
            source_path = self.source_folder.get()
            dest_path = self.destination_folder.get()
            
            # Check if source folder exists
            if not os.path.exists(source_path):
                messagebox.showerror("Error", "Source folder does not exist.")
                return
                
            # Get subfolders
            subfolders = [name for name in os.listdir(source_path) 
                         if os.path.isdir(os.path.join(source_path, name))]
            
            if not subfolders:
                messagebox.showerror("Error", "No subfolders found in source directory.")
                return
                
            # Extract years
            years = self.extract_unique_years(subfolders)
            
            if not years:
                messagebox.showerror("Error", "No valid year-based folders found.")
                return
                
            # Check for existing backup folder
            potential_backup = os.path.join(dest_path, "Iphone_Photo_Backup")
            existing_backup = os.path.exists(potential_backup)
            
            # Count files
            total_files = 0
            file_breakdown = defaultdict(int)
            
            for subfolder in subfolders:
                year = subfolder[:4] if len(subfolder) >= 4 and subfolder[:4].isdigit() else "Unknown"
                subfolder_path = os.path.join(source_path, subfolder)
                for root, dirs, files in os.walk(subfolder_path):
                    file_count = len(files)
                    total_files += file_count
                    file_breakdown[year] += file_count
                    
            # Update preview
            preview_text = f"Analysis Results:\n"
            preview_text += f"{'='*50}\n\n"
            preview_text += f"Source Folder: {source_path}\n"
            preview_text += f"Destination: {dest_path}\n\n"
            preview_text += f"Found {len(subfolders)} subfolders\n"
            preview_text += f"Years identified: {', '.join(years)}\n"
            preview_text += f"Total files to process: {total_files:,}\n\n"
            
            preview_text += f"Files by year:\n"
            for year in sorted(file_breakdown.keys()):
                preview_text += f"  {year}: {file_breakdown[year]:,} files\n"
                
            preview_text += f"\nBackup folder status:\n"
            if existing_backup:
                preview_text += f"  ✓ Existing backup folder found: {potential_backup}\n"
                existing_years = []
                for item in os.listdir(potential_backup):
                    item_path = os.path.join(potential_backup, item)
                    if os.path.isdir(item_path) and len(item) == 4 and item.isdigit():
                        existing_years.append(item)
                if existing_years:
                    preview_text += f"  ✓ Existing year folders: {', '.join(sorted(existing_years))}\n"
                    preview_text += f"  → Files will be added to existing year folders\n"
                else:
                    preview_text += f"  → New year folders will be created\n"
            else:
                preview_text += f"  → New backup folder will be created: {potential_backup}\n"
                
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
            
            # Store backup root for later use
            self.backup_root = potential_backup
            
            # Enable start button
            self.start_button.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing folders: {str(e)}")
            
    def collect_all_files(self, source_path):
        """Collect all files from subfolders"""
        all_files = []
        for subfolder in os.listdir(source_path):
            subfolder_path = os.path.join(source_path, subfolder)
            if os.path.isdir(subfolder_path):
                year = subfolder[:4] if len(subfolder) >= 4 and subfolder[:4].isdigit() else "Unknown"
                for root, dirs, files in os.walk(subfolder_path):
                    for file in files:
                        all_files.append((os.path.join(root, file), year))
        return all_files
        
    def create_year_folders(self, years):
        """Create or use existing year folders"""
        # Create backup root if it doesn't exist
        os.makedirs(self.backup_root, exist_ok=True)
        
        year_paths = {}
        for year in years:
            year_path = os.path.join(self.backup_root, year)
            os.makedirs(year_path, exist_ok=True)
            year_paths[year] = year_path
            
        return year_paths
        
    def copy_files_with_progress(self, files, year_paths):
        """Copy files with progress tracking"""
        total_files = len(files)
        
        for i, (src_file, year) in enumerate(files):
            try:
                dst_dir = year_paths.get(year)
                if not dst_dir:
                    self.log_message(f"No destination folder for year {year}, skipping {src_file}", logging.WARNING)
                    self.stats['failed_files'] += 1
                    continue
                    
                # Get filename and destination path
                filename = os.path.basename(src_file)
                dst_file = os.path.join(dst_dir, filename)
                
                # Check if file already exists
                if os.path.exists(dst_file):
                    # Compare file sizes to determine if it's the same file
                    if os.path.getsize(src_file) == os.path.getsize(dst_file):
                        self.stats['existing_files'] += 1
                        continue
                    else:
                        # File exists but different size, create unique name
                        base, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(dst_file):
                            new_filename = f"{base}_{counter}{ext}"
                            dst_file = os.path.join(dst_dir, new_filename)
                            counter += 1
                
                # Copy file
                shutil.copy2(src_file, dst_file)
                self.stats['copied_files'] += 1
                self.stats['years_processed'].add(year)
                
                # Update progress
                progress = (i + 1) / total_files * 100
                self.progress_var.set(progress)
                self.progress_label.config(text=f"{i + 1}/{total_files}")
                
                if i % 100 == 0:  # Log every 100 files
                    self.log_message(f"Copied {i + 1}/{total_files} files...")
                    
            except Exception as e:
                error_msg = f"Error copying {src_file}: {str(e)}"
                self.log_message(error_msg, logging.ERROR)
                self.stats['failed_files'] += 1
                
            # Update GUI
            self.root.update()
            
    def start_sorting(self):
        """Start the file sorting process"""
        def sorting_thread():
            try:
                self.start_button.config(state=tk.DISABLED)
                self.analyze_button.config(state=tk.DISABLED)
                
                # Reset stats
                self.stats = {
                    'total_files': 0,
                    'copied_files': 0,
                    'failed_files': 0,
                    'existing_files': 0,
                    'years_processed': set()
                }
                
                # Setup logging
                self.setup_logging()
                
                # Log start
                self.log_message("=== iPhone Photo Sorting Started ===")
                self.log_message(f"Source: {self.source_folder.get()}")
                self.log_message(f"Destination: {self.backup_root}")
                
                # Get all files
                source_path = self.source_folder.get()
                all_files = self.collect_all_files(source_path)
                self.stats['total_files'] = len(all_files)
                
                self.log_message(f"Found {len(all_files):,} files to process")
                
                # Extract years and create folders
                subfolders = [name for name in os.listdir(source_path) 
                             if os.path.isdir(os.path.join(source_path, name))]
                years = self.extract_unique_years(subfolders)
                
                year_paths = self.create_year_folders(years)
                self.log_message(f"Created/verified year folders: {', '.join(years)}")
                
                # Copy files
                self.log_message("Starting file copy process...")
                self.copy_files_with_progress(all_files, year_paths)
                
                # Final statistics
                self.log_message("=== Sorting Complete ===")
                self.log_message(f"Total files processed: {self.stats['total_files']:,}")
                self.log_message(f"Files copied: {self.stats['copied_files']:,}")
                self.log_message(f"Files skipped (already exist): {self.stats['existing_files']:,}")
                self.log_message(f"Failed copies: {self.stats['failed_files']:,}")
                self.log_message(f"Years processed: {', '.join(sorted(self.stats['years_processed']))}")
                
                # Write summary to log
                self.write_summary_log()
                
                # Update progress
                self.progress_var.set(100)
                self.progress_label.config(text="Complete!")
                
                # Enable delete button
                self.delete_button.config(state=tk.NORMAL)
                
                messagebox.showinfo("Success", 
                    f"Sorting complete!\n\n"
                    f"Files copied: {self.stats['copied_files']:,}\n"
                    f"Files skipped: {self.stats['existing_files']:,}\n"
                    f"Failed: {self.stats['failed_files']:,}\n\n"
                    f"Log saved to: {os.path.basename(self.log_file_path)}")
                
            except Exception as e:
                error_msg = f"Error during sorting: {str(e)}"
                self.log_message(error_msg, logging.ERROR)
                messagebox.showerror("Error", error_msg)
            finally:
                self.start_button.config(state=tk.NORMAL)
                self.analyze_button.config(state=tk.NORMAL)
                
        # Start sorting in separate thread
        thread = threading.Thread(target=sorting_thread, daemon=True)
        thread.start()
        
    def write_summary_log(self):
        """Write detailed summary to log file"""
        if not self.logger:
            return
            
        self.logger.info("="*60)
        self.logger.info("DETAILED SUMMARY")
        self.logger.info("="*60)
        self.logger.info(f"Operation completed at: {datetime.datetime.now()}")
        self.logger.info(f"Source folder: {self.source_folder.get()}")
        self.logger.info(f"Backup folder: {self.backup_root}")
        self.logger.info(f"Total files found: {self.stats['total_files']:,}")
        self.logger.info(f"Files successfully copied: {self.stats['copied_files']:,}")
        self.logger.info(f"Files skipped (duplicates): {self.stats['existing_files']:,}")
        self.logger.info(f"Failed file copies: {self.stats['failed_files']:,}")
        self.logger.info(f"Success rate: {(self.stats['copied_files'] / max(1, self.stats['total_files']) * 100):.1f}%")
        self.logger.info(f"Years processed: {', '.join(sorted(self.stats['years_processed']))}")
        
        # Log folder structure
        self.logger.info("\nFINAL FOLDER STRUCTURE:")
        try:
            for year_folder in sorted(os.listdir(self.backup_root)):
                year_path = os.path.join(self.backup_root, year_folder)
                if os.path.isdir(year_path) and len(year_folder) == 4 and year_folder.isdigit():
                    file_count = sum(len(files) for _, _, files in os.walk(year_path))
                    self.logger.info(f"  {year_folder}/: {file_count:,} files")
        except Exception as e:
            self.logger.error(f"Error logging folder structure: {e}")
            
    def delete_original(self):
        """Delete original source folder after confirmation"""
        source_path = self.source_folder.get()
        
        if not source_path or not os.path.exists(source_path):
            messagebox.showerror("Error", "Source folder not found.")
            return
            
        # Double confirmation
        response = messagebox.askyesno("Confirm Deletion", 
            f"Are you sure you want to delete the original folder?\n\n"
            f"This will permanently delete:\n{source_path}\n\n"
            f"Make sure you have verified that all files were copied correctly!")
            
        if not response:
            return
            
        # Final confirmation
        response = messagebox.askyesno("Final Confirmation", 
            "This is your last chance to cancel.\n\n"
            "Are you absolutely sure you want to delete the original folder?")
            
        if not response:
            return
            
        try:
            self.log_message(f"Deleting original folder: {source_path}")
            shutil.rmtree(source_path)
            self.log_message("Original folder deleted successfully")
            messagebox.showinfo("Success", "Original folder deleted successfully.")
            self.delete_button.config(state=tk.DISABLED)
        except Exception as e:
            error_msg = f"Error deleting original folder: {str(e)}"
            self.log_message(error_msg, logging.ERROR)
            messagebox.showerror("Error", error_msg)
            
    def open_log_file(self):
        """Open the log file in default text editor"""
        if self.log_file_path and os.path.exists(self.log_file_path):
            try:
                os.startfile(self.log_file_path)  # Windows
            except AttributeError:
                try:
                    os.system(f'open "{self.log_file_path}"')  # macOS
                except:
                    os.system(f'xdg-open "{self.log_file_path}"')  # Linux
        else:
            messagebox.showinfo("Info", "No log file available yet. Run the sorting process first.")

def main():
    root = tk.Tk()
    app = PhotoSorterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()