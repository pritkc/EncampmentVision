# EncampmentVision

## API Key Setup

This project uses the Google Street View API to download street view images. To use this application, you need to:

1. Obtain a Google Street View API key from the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a `.env` file in the root directory of the project
3. Add your API key to the `.env` file in the following format:
   ```
   API_KEY=your_api_key_here
   ```

## Requirements

Install the required dependencies:

```bash
pip install google_streetview requests python-dotenv
```

## Available Scripts

### Multi-Location Street View Downloader

Process multiple locations and download street view images for each one:

```bash
python multi_location_downloader.py
```

This script will:
- Process 5 predefined locations with their coordinates
- Create properly named folders for each location (replacing spaces with hyphens)
- Download 75 street view images for each location
- Save images with coordinates and heading information

### Street View Downloader (Python Script)

Run the script to download street view images:

```bash
python copy_of_google_street_view_downloader_pc.py
```

### Google Maps Street View Downloader (Python Script)

Alternative script that uses direct Google Maps Street View API:

```bash
python gmap_street_view.py
```

Both scripts will download Google Street View images based on the specified coordinates and parameters, but with slightly different implementations.

### Original Jupyter Notebooks

The repository also contains the original Jupyter notebooks:
- `Copy_of_Google_Street_View_Downloader_PC.ipynb`
- `gmap_download_script.ipynb`

**Note:** The Python scripts are recommended over the notebooks as they incorporate proper API key security.
