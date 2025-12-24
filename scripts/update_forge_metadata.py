import hashlib
import json

def calculate_md5(file_path: str) -> str:
    """Calculate MD5 hash of a file"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            md5.update(chunk)
    return md5.hexdigest()

def update_forge_json_hash(
    json_path: str,
    forge_file_path: str,
    output_json_path: str = None,
    classifier: str = "installer",
    extension: str = "jar"
):
    """
    Update MD5 hash for a specific forge file in the JSON
    
    Args:
        json_path: Path to forge JSON file
        forge_file_path: Path to the actual forge file
        output_json_path: Path to save updated JSON (default: same as input)
        classifier: Classifier name (e.g., "installer", "universal")
        extension: File extension (e.g., "jar")
    """
    
    if output_json_path is None:
        output_json_path = json_path
    
    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Calculate MD5
    print(f"Calculating MD5 hash for: {forge_file_path}\n")
    md5_hash = calculate_md5(forge_file_path)
    
    print(f"MD5: {md5_hash}\n")
    
    # Check if classifier exists
    if "classifiers" not in data:
        data["classifiers"] = {}
    
    if classifier not in data["classifiers"]:
        data["classifiers"][classifier] = {}
    
    # Update hash
    old_hash = data["classifiers"][classifier].get(extension, "N/A")
    data["classifiers"][classifier][extension] = md5_hash
    
    # Save updated JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*60}")
    print(f"Updated: classifiers.{classifier}.{extension}")
    print(f"Old hash: {old_hash}")
    print(f"New hash: {md5_hash}")
    print(f"Saved to: {output_json_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    update_forge_json_hash(
        json_path='./1.20.1-47.4.13/meta.json',
        forge_file_path='./forge-1.20.1-47.4.13-installer.jar',
        classifier='installer',
        extension='jar'
    )