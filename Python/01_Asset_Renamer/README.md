# Asset Renamer

A Python-based asset renaming tool designed for 3D artists and texture workflows.


## Features

- Detects texture-map names from filenames
- Supports BaseColor, Albedo, Normal, Roughness, AO, Metallic, Height and Opacity
- Converts texture names into standard abbreviations
- Detects UDIM numbers
- Generates standardized filenames
- Automatically handles version numbers
- Creates a CSV report for artist approval
- Revalidates original filenames before renaming
- Supports individual folders
- Supports recursive subfolder processing
- Includes a Tkinter GUI
- Can be packaged as a Windows `.exe`

## Example

### Original filenames

```text
wood_albedo.png
wood_normal.jpg
Metal_Floor_01_BaseColor_1001.png
```

## Renamed files
* wood_BC_v01.png
* wood_N_v01.jpg

## Workflow
* Enter or browse to the target folder.
* Click Run.
* Click Status to open the CSV report.
* Edit the Status column in the CSV file.
* Keep Approved for files to rename.
* Change unwanted files to Skipped.
* Click Rename.

## Folder Path Options
### Process one folder
- D:\Assets\sample_assets

### Process a folder and its subfolders
- D:\Assets\sample_assets\*

## Technologies
* Python
* Tkinter
* pathlib
* CSV
* PyInstaller