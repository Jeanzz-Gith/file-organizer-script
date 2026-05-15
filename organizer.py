"""
File Organizer by Extension

This script moves files from a source folder (default: "./files") into subfolders
based on file type (Images, Documents, Videos, Music, Archives, Others).

How to use:
1. Place this script in the directory containing the "files" folder (or change SOURCE_FOLDER).
2. Run: python file_organizer.py
3. Files will be moved into subfolders like "./files/Images", "./files/Documents", etc.

Notes:
- Files without extension or with unknown extensions go to "Others".
- Subfolders inside the source folder are ignored (only files are moved).
- If the source folder does not exist, an error message is shown.
"""

import os
import shutil
from pathlib import Path

# ============================================================================
# CONFIGURATION (easy to modify)
# ============================================================================

# Folder to organize (relative or absolute path)
SOURCE_FOLDER = "./files"   # Example: "./downloads" or r"C:\Users\Name\Desktop\messy"

# Mapping: destination folder name -> list of file extensions (case-insensitive)
FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".odt"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
    # Add or remove extensions as needed
}

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def organize_files(source_folder: str) -> None:
    """
    Organizes files from source_folder into subfolders based on extension.

    Args:
        source_folder (str): Path to the folder containing files to organize.
    """
    source_path = Path(source_folder)

    # --- Check if source folder exists and is a directory ---
    if not source_path.exists():
        print(f"ERROR: Folder '{source_folder}' not found.")
        print("Tip: Verify the path and ensure the script is in the correct directory.")
        return

    if not source_path.is_dir():
        print(f"ERROR: '{source_folder}' is not a directory.")
        return

    # --- Iterate over each item in the source folder ---
    for item in source_path.iterdir():
        if not item.is_file():
            continue  # Skip subdirectories

        file_name = item.name
        file_path = item
        moved = False

        # --- Try to match the file extension with a category ---
        for folder_name, extensions in FILE_TYPES.items():
            if file_name.lower().endswith(tuple(extensions)):
                target_folder = source_path / folder_name
                target_folder.mkdir(exist_ok=True)  # Create folder if it doesn't exist

                destination = target_folder / file_name
                shutil.move(str(file_path), str(destination))
                print(f"Moved: {file_name} -> {folder_name}/")
                moved = True
                break  # Stop searching once a match is found

        # --- If no category matches, move to "Others" ---
        if not moved:
            others_folder = source_path / "Others"
            others_folder.mkdir(exist_ok=True)
            destination = others_folder / file_name
            shutil.move(str(file_path), str(destination))
            print(f"Moved: {file_name} -> Others/")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("=== File Organizer by Extension ===\n")
    print(f"Source folder: {SOURCE_FOLDER}")
    print("Configured categories:")
    for cat, exts in FILE_TYPES.items():
        print(f"  - {cat}: {', '.join(exts)}")
    print("\nStarting organization...\n")

    organize_files(SOURCE_FOLDER)

    print("\nOrganization complete.")
