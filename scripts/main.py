import os
import hashlib
import json
from pathlib import Path
from typing import List, Dict

def calculate_sha1(file_path: str) -> str:
    """Calculate SHA1 hash of a file"""
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def scan_assets_directory(
    assets_dir: str,
    base_url: str,
    output_file: str = "assets_manifest.json",
    special_files: Dict[str, str] = None
) -> List[Dict[str, any]]:
    """
    Scan assets directory and create manifest with file info
    
    Args:
        assets_dir: Path to assets directory
        base_url: Base URL where files will be hosted
        output_file: Output JSON file name
        special_files: Dictionary of filenames with custom base URLs
    
    Returns:
        List of file info dictionaries
    """
    
    if special_files is None:
        special_files = {}
    
    if not os.path.exists(assets_dir):
        print(f"Error: Directory '{assets_dir}' does not exist")
        return []
    
    files_info = []
    assets_path = Path(assets_dir)
    
    print(f"Scanning directory: {assets_dir}")
    print(f"Base URL: {base_url}")
    if special_files:
        print(f"Special files with custom URLs: {len(special_files)}")
    print()
    
    # Walk through all files in assets directory
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Calculate relative path from assets directory
            rel_path = os.path.relpath(file_path, assets_dir)
            
            # Convert Windows path separators to forward slashes for URLs
            url_path = rel_path.replace('\\', '/')
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Calculate hash
            print(f"Processing: {rel_path}")
            file_hash = calculate_sha1(file_path)
            
            # Check if this file has a special URL
            current_base_url = base_url
            for special_filename, special_url in special_files.items():
                if special_filename in file:
                    current_base_url = special_url
                    print(f"  ⚡ Using special URL for this file")
                    break
            
            # Construct URL
            file_url = f"{current_base_url}/{url_path}"
            
            # Create file info object
            file_info = {
                "path": url_path,
                "hash": file_hash,
                "size": file_size,
                "url": file_url
            }
            
            files_info.append(file_info)
            print(f"  Size: {file_size:,} bytes")
            print(f"  SHA1: {file_hash}")
            print(f"  URL: {file_url}\n")
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(files_info, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*60}")
    print(f"Summary:")
    print(f"  Total files processed: {len(files_info)}")
    print(f"  Manifest saved to: {output_file}")
    print(f"{'='*60}")
    
    return files_info


# Использование с кастомными URL для больших файлов
if __name__ == "__main__":
    # Определяем файлы, которые будут использовать R2 CDN
    special_files = {
        "Kaminari Motor Work 2.6.1 16-20.jar": "https://pub-667cb3e69b324e049e8d10959a1d5bb9.r2.dev",
        "MTS Official Pack-1.20.1-V28.2": "https://pub-667cb3e69b324e049e8d10959a1d5bb9.r2.dev"
    }
    
    files = scan_assets_directory(
        assets_dir='../assets',
        base_url='https://raw.githubusercontent.com/Homanti/wacorp-assets/main/assets',
        output_file='assets_manifest.json',
        special_files=special_files
    )