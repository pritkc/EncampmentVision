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

## Usage

Run the script to download street view images:

```bash
python copy_of_google_street_view_downloader_pc.py
```

The script will download Google Street View images based on the specified coordinates and parameters.
