import os
import shutil
from tqdm import tqdm
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def get_folder_location(prompt_title):
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=prompt_title)
    return folder

def extract_unique_years(folder_names):
    years = {name[:4] for name in folder_names if name[:4].isdigit()}
    return sorted(years)

def collect_all_files(subfolders_path):
    all_files = []
    for subfolder in os.listdir(subfolders_path):
        full_path = os.path.join(subfolders_path, subfolder)
        if os.path.isdir(full_path):
            for dirpath, _, filenames in os.walk(full_path):
                for file in filenames:
                    all_files.append((os.path.join(dirpath, file), subfolder[:4]))
    return all_files

def create_year_folders(base_path, years):
    backup_root = os.path.join(base_path, "Iphone_Photo_Backup")
    os.makedirs(backup_root, exist_ok=True)
    year_paths = {}
    for year in years:
        year_path = os.path.join(backup_root, year)
        os.makedirs(year_path, exist_ok=True)
        year_paths[year] = year_path
    return backup_root, year_paths

def copy_files_with_progress(files, year_paths):
    for src_file, year in tqdm(files, desc="Copying Files", unit="file"):
        dst_dir = year_paths.get(year)
        if dst_dir:
            try:
                shutil.copy2(src_file, dst_dir)
            except Exception as e:
                print(f"Error copying {src_file}: {e}")

def confirm_and_delete(source_folder):
    print("\nPlease manually check the 'Iphone_Photo_Backup' folder to ensure everything copied correctly.")
    confirm = input("Type 'YES' to confirm deletion of the original folder: ").strip()
    if confirm.upper() == "YES":
        shutil.rmtree(source_folder)
        print("Original folder deleted.")
    else:
        print("Deletion cancelled.")

def main():
    print("Step 1: Select the folder where all iPhone DCIM subfolders were copied.")
    source_folder = get_folder_location("Select Source Folder with iPhone DCIM Subfolders")
    if not source_folder:
        print("No folder selected. Exiting.")
        return

    subfolders = [name for name in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, name))]
    years = extract_unique_years(subfolders)
    
    if not years:
        print("No valid year-based folders found.")
        return

    print(f"Identified years: {', '.join(years)}")
    print("\nStep 2: Select the location where 'Iphone_Photo_Backup' should be created.")
    target_base = get_folder_location("Select Destination for Backup Folder")
    if not target_base:
        print("No destination selected. Exiting.")
        return

    backup_root, year_paths = create_year_folders(target_base, years)

    print("\nStep 3: Copying files to year-based folders...")
    all_files = collect_all_files(source_folder)
    copy_files_with_progress(all_files, year_paths)

    print(f"\n✅ Backup complete. All photos copied to '{backup_root}'.")
    
    confirm_and_delete(source_folder)

if __name__ == "__main__":
    main()
