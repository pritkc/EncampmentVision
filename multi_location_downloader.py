import google_streetview.api
import os
import time
import requests
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Street View API key
API_KEY = os.getenv("API_KEY")

# Check if API key is available
if not API_KEY:
    raise ValueError("API key not found. Please set the API_KEY in the .env file.")

# List of locations with their coordinates
locations = [
    # {
    #     "name": "Central Fwy 2",
    #     "top_left": (37.7695034, -122.4113093),
    #     "bottom_right": (37.769882, -122.4215653)
    # },
    # {
    #     "name": "1938 Evans Ave",
    #     "top_left": (37.7462877, -122.3942652),
    #     "bottom_right": (37.7479154, -122.396425)
    # },
    # {
    #     "name": "2098 Marin St",
    #     "top_left": (37.7485767, -122.3938247),
    #     "bottom_right": (37.7483964, -122.3964596)
    # },
    # {
    #     "name": "255 Barneveld Ave",
    #     "top_left": (37.7442872, -122.4031137),
    #     "bottom_right": (37.7463507, -122.4025866)
    # },
    # {
    #     "name": "1938 Evans Ave(2)",
    #     "top_left": (37.7463403, -122.3943565),
    #     "bottom_right": (37.7441226, -122.390377)
    # },
    # {
    #     "name": "19th Street",
    #     "top_left": (37.7667, -122.4167),
    #     "bottom_right": (37.7667, -122.4100)
    # },
    {
        "name": "2010 Cesar Chavez St",
        "top_left": (37.7496673, -122.3972457),
        "bottom_right": (37.7495168, -122.4028567)
    }
]

# Function to determine the major axis and step size automatically
def calculate_grid_steps(top_left, bottom_right, num_points_major):
    lat1, lon1 = top_left
    lat2, lon2 = bottom_right

    lat_diff = abs(lat1 - lat2)
    lon_diff = abs(lon1 - lon2)

    if lat_diff > lon_diff:
        # Street runs north-south
        latitude_step = lat_diff / (num_points_major - 1)
        longitude_step = 0  # Keep longitude constant
        major_axis = "latitude"
    else:
        # Street runs east-west
        latitude_step = 0  # Keep latitude constant
        longitude_step = lon_diff / (num_points_major - 1)
        major_axis = "longitude"

    # Ensure steps respect the direction of travel (positive/negative values)
    latitude_step = -latitude_step if lat1 > lat2 else latitude_step
    longitude_step = -longitude_step if lon1 > lon2 else longitude_step

    return latitude_step, longitude_step, major_axis

# Function to generate grid points based on the detected direction with a sampling rate
def generate_grid(top_left, num_points_major, latitude_step, longitude_step, major_axis, sample_interval=1):
    lat1, lon1 = top_left
    
    # Calculate total steps needed to cover the distance
    total_steps = num_points_major * sample_interval
    
    # Generate all points
    all_points = [(lat1 + i * latitude_step, lon1 + i * longitude_step) for i in range(total_steps)]
    
    # Sample points at the specified interval
    sampled_points = [all_points[i] for i in range(0, len(all_points), sample_interval)]
    
    # Make sure we have at least num_points_major points or as many as possible
    return sampled_points[:num_points_major]

# Function to create a folder-friendly name
def create_folder_name(name):
    # Replace spaces with hyphens and remove any invalid characters
    folder_name = name.replace(" ", "-")
    # Replace any other characters that might be problematic
    folder_name = re.sub(r'[\\/*?:"<>|]', "", folder_name)
    return folder_name

# Number of images to download for each location
num_points_major = 75

# Sample interval - how far apart the points should be (higher = more diverse images)
# A value of 1 means use every point, 2 means every other point, 3 means every third point, etc.
sample_interval = 2  # Increase this value to get more diverse images

# Process each location
for location in locations:
    name = location["name"]
    top_left = location["top_left"]
    bottom_right = location["bottom_right"]
    
    # Create folder name
    folder_name = create_folder_name(name)
    output_dir = f"images/{folder_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n===== Processing {name} =====")
    print(f"Coordinates: {top_left} to {bottom_right}")
    print(f"Output directory: {output_dir}")
    print(f"Using sample interval: {sample_interval} (higher = more distance between images)")
    
    # Auto-calculate grid step sizes
    latitude_step, longitude_step, major_axis = calculate_grid_steps(top_left, bottom_right, num_points_major)
    
    # Generate grid of points with sampling
    grid_points = generate_grid(top_left, num_points_major, latitude_step, longitude_step, major_axis, sample_interval)
    print(f"Generated {len(grid_points)} grid points along the {major_axis} axis.")
    
    # Check if there are any grid points
    if not grid_points:
        print("No grid points generated. Please check coordinates.")
        continue
    
    # Download Google Street View images for each point in the grid at angles 90 and 270
    for idx, (lat, lon) in enumerate(grid_points):
        headings = [90, 270]  # Capture street view images from two angles
        for heading in headings:
            # Define parameters for the Google Street View API request
            params = [{
                'size': '640x640',     # Maximum resolution allowed by API
                'location': f'{lat},{lon}',
                'heading': str(heading),  # Set heading to 90 and 270
                'pitch': '0',          # Adjust pitch as desired (0 = horizon)
                'source': 'outdoor',   # ensures official Google images only
                'key': API_KEY
            }]

            # Use Google Street View API to get image and metadata
            results = google_streetview.api.results(params)

            try:
                # Extract metadata
                metadata = results.metadata[0]  # Get metadata for the first result
                pano_id = metadata.get('pano_id', 'unknown')
                date = metadata.get('date', 'unknown')

                # Define a filename based on coordinates, heading, and capture date
                filename = f"streetview_{pano_id}_{date}_{lat}_{lon}_heading{heading}.jpg"
                filepath = os.path.join(output_dir, filename)

                # Download the image directly to the specified path
                if results.links:
                    response = requests.get(results.links[0])
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded to {output_dir}: image for location {lat}, {lon} at heading {heading} as {filename}")
                else:
                    print(f"No image available for location {lat}, {lon} at heading {heading}")

                time.sleep(1)  # Sleep to avoid hitting rate limits (adjust as needed)
            except Exception as e:
                print(f"Failed to download image for location {lat}, {lon} at heading {heading}: {e}")
    
    print(f"===== Completed {name} =====")

print("\nAll locations processed successfully!") 