#!/usr/bin/env python3
# ==============================================================================
# Script Name: file_organizer.py
# Description: Organizes loose files into subfolders based on extension.
# Author:      Muhammad Rayyan
# ==============================================================================

import os
import shutil

def organize_directory(target_dir="."):
    extension_map = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Docs": [".pdf", ".docx", ".txt", ".md", ".xlsx"],
        "Scripts": [".py", ".sh", ".js", ".json", ".yml", ".yaml"],
        "Archives": [".zip", ".tar", ".gz", ".7z"]
    }
    
    print(f"[*] Auditing directory: {os.path.abspath(target_dir)}")
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower()
            for category, exts in extension_map.items():
                if ext in exts:
                    category_folder = os.path.join(target_dir, category)
                    os.makedirs(category_folder, exist_ok=True)
                    print(f"  [+] Moving '{item}' -> '{category}/'")
                    # shutil.move(item_path, os.path.join(category_folder, item))
                    break

if __name__ == "__main__":
    print("============================================================")
    print("                 PYTHON FILE ORGANIZER                      ")
    print("============================================================")
    organize_directory(".")
    print("============================================================")
