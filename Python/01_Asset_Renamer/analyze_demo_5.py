from pathlib import Path
import csv
script_dir=Path(__file__).parent

def analyze_filename(file):
    TEXTURE_CODES={"basecolor":"BC","albedo":"BC","normal":"N","roughness": "R","ao": "AO",
                    "metallic": "M","height": "H","opacity": "OP","ambientocclusion": "AO","base":'BC'}
    asset_name=file.stem 
    parts=asset_name.split("_")
    parts_trim=[i.lower() for i in parts]
    texture = None
    asset_index=None
    for index,word in enumerate(parts):
        word=word.lower()
        if word in TEXTURE_CODES:
            texture=TEXTURE_CODES[word]
            asset_index=index
            break
        for j in parts_trim:
           temp_word=str(word+j)
           if temp_word in TEXTURE_CODES:
                texture=TEXTURE_CODES[temp_word]
                asset_index=index
                break
    if asset_index is None:
        new_name=asset_name
    else:
        new_name="_".join(parts[:asset_index])

    udim=None
    for word in parts:
        if word.isdigit() and word.startswith('1') and len(word)==4:
            udim=word
            break
    
    valid=texture is not None 
    return{
        "File_name":file.name,"asset_name":new_name,"Texture":texture,"UDIM":udim,"Is_valid":valid,"extension":file.suffix
    }


def get_next_version(folder, info, current_file, used_versions):

    asset_name = info["asset_name"]
    texture = info["Texture"]

    highest_version = 0

    for file in folder.iterdir():

        if file == current_file:
            continue

        parts = file.stem.split("_")

        if len(parts) < 3:
            continue

        if parts[0] != asset_name:
            continue

        if parts[1] != texture:
            continue

        version_part = parts[2]

        if not version_part.startswith("v"):
            continue

        version_text = version_part[1:]

        if not version_text.isdigit():
            continue

        version = int(version_text)

        if version > highest_version:
            highest_version = version

    key = (asset_name, texture)

    if key in used_versions:
        if used_versions[key] > highest_version:
            highest_version = used_versions[key]

    next_version = highest_version + 1

    used_versions[key] = next_version

    return next_version

def gen_new_filename(info, next_version):

    if not info["Is_valid"]:
        return None

    asset_name = info["asset_name"]
    texture = info["Texture"]
    udim = info["UDIM"]
    extension = info["extension"]

    if udim is None:
        return f"{asset_name}_{texture}_v{next_version:02d}{extension}"

    return f"{asset_name}_{texture}_v{next_version:02d}_{udim}{extension}"


def generate_preview(folder):

    used_versions = {}

    report_file = folder / "report.csv"

    with open(report_file, "w", newline="") as report_file_handle:

        writer = csv.writer(report_file_handle)

        writer.writerow([
            "# INSTRUCTIONS: Keep Status as Approved to rename or Skipped to ignore."
        ])

        writer.writerow([])

        writer.writerow([
            "Original",
            "New",
            "Texture",
            "UDIM",
            "Is_valid",
            "Status"
        ])

        for file in folder.iterdir():

            info = analyze_filename(file)

            next_version = get_next_version(
                folder,
                info,
                file,
                used_versions
            )

            new_filename = gen_new_filename(
                info,
                next_version
            )

            if not info["Is_valid"]:
                status = "Skipped"
            else:
                status = "Approved"

            print(f"Old_name : {file.name}")
            print(f"New_name : {new_filename}")
            print(f"Status   : {status}")
            print("------------------------------")

            writer.writerow([
                file.name,
                new_filename,
                info["Texture"],
                info["UDIM"],
                info["Is_valid"],
                status
            ])

def read_artist_decisions(report_file):

    decisions = {}

    with open(report_file, newline="") as file:

        reader = csv.reader(file)

        next(reader)  # Skip instruction row
        next(reader)  # Skip blank row

        headers = next(reader)

        for row in reader:

            original = row[0]
            status = row[5]

            decisions[original] = status

    return decisions


def execute_renaming(folder, decisions):
    used_versions = {}

    stats = {
        "renamed": 0,
        "skipped": 0,
        "conflicts": 0
    }

    for file in folder.iterdir():

        # Get the artist's decision for this file
        status = decisions.get(file.name)

        # Only Approved files are considered
        if status != "Approved":
            stats["skipped"] += 1
            continue

        # Analyze the ORIGINAL file again
        info = analyze_filename(file)

        # Do not trust the CSV Is_valid value
        if not info["Is_valid"]:
            print(f"SKIPPED - Invalid filename: {file.name}")
            stats["skipped"] += 1
            continue

        # Find the next available version
        next_version = get_next_version(
            folder,
            info,
            file,
            used_versions
        )

        # Generate the new filename
        new_filename = gen_new_filename(
            info,
            next_version
        )

        new_path = folder / new_filename

        # Safety check
        if new_path.exists():

            print(f"WARNING - Already exists: {new_filename}")
            stats["conflicts"] += 1
            continue

        # Rename
        file.rename(new_path)

        print(f"RENAMED: {file.name} -> {new_filename}")
        stats["renamed"] += 1

    return stats
    

# if __name__ == "__main__": 
#     generate_preview()
if __name__ == "__main__":
    pass
