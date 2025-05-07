import os
import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime, UTC

def select_files_and_folders():
    """Use tkinter to select files and folders"""
    root = tk.Tk()
    root.withdraw()
    
    files = list(filedialog.askopenfilenames(
        title="Select files to prefix",
        filetypes=[("Audio Files", "*.wav *.mp3 *.aif *.aiff"), ("All Files", "*.*")]
    ))
    
    folder = filedialog.askdirectory(title="Select folder (optional)")
    if folder:
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith(('.wav', '.mp3', '.aif', '.aiff')):
                    files.append(os.path.join(root, filename))
    
    return files

def prefix_files(files, prefix, dry_run=False):
    """Prefix files and return results"""
    results = []
    for file in files:
        directory, filename = os.path.split(file)
        new_filename = prefix + filename
        new_path = os.path.join(directory, new_filename)
        
        if not os.path.exists(new_path):  # Avoid overwriting
            if not dry_run:
                try:
                    os.rename(file, new_path)
                    results.append({"old": file, "new": new_path})
                    print(f"✅ {filename} ➜ {new_filename}")
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")
            else:
                print(f"🔸 Would rename: {filename} ➜ {new_filename}")
        else:
            print(f"⚠️  Skipped (already exists): {new_filename}")
    
    return results

def main(dry_run=False):
    try:
        # Get files
        files = select_files_and_folders()
        if not files:
            print("No files selected.")
            return False
        
        # Get prefix
        prefix = input("Enter prefix: ").strip()
        if not prefix:
            print("No prefix entered.")
            return False
        
        # Process files
        results = prefix_files(files, prefix, dry_run)
        
        # Log results if not dry run
        if results and not dry_run:
            operation = {
                'entries': results,
                'prefix': prefix,
                'timestamp': datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            try:
                with open("LOG_renamed.json", 'r') as f:
                    log = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                log = []
            
            log.append(operation)
            with open("LOG_renamed.json", 'w') as f:
                json.dump(log, f, indent=2)
        
        print("\nOperation complete!")
        return True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    main()