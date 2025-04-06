import os
import datetime
from dotenv import load_dotenv
# from pytube import YouTube
from pytubefix import YouTube  # pytubefix is a patched version of pytube
from pytubefix.cli import on_progress
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Load environment variables from .env file
load_dotenv()
RUMBLE_EMAIL = os.getenv("RUMBLE_EMAIL")
RUMBLE_PASSWORD = os.getenv("RUMBLE_PASSWORD")
YT_SECRET = os.getenv("YT_SECRET")

# YouTube API scope to access your videos
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def accept_rumble_terms(driver):
    """
    Accepts the mandatory terms and conditions checkboxes on Rumble using JavaScript.
    """
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "crights")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cterms")))
    driver.execute_script("document.getElementById('crights').click();")
    driver.execute_script("document.getElementById('cterms').click();")

def select_primary_category(driver, category_name):
    """
    Selects a category from Rumble's custom searchable dropdown.
    """
    input_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "primary-category"))
    )
    input_field.click()
    input_field.send_keys(category_name)
    time.sleep(0.5)  # Allow dropdown options to load
    driver.find_element(By.CLASS_NAME, "select-options-container").click()

def get_authenticated_service():
    """
    Authenticates the YouTube API client using OAuth2.
    """
    flow = InstalledAppFlow.from_client_secrets_file(YT_SECRET, SCOPES)
    creds = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)

def fetch_shorts_by_date(youtube, date):
    """
    Retrieves all YouTube Shorts uploaded on the specified date.
    """
    request = youtube.channels().list(part="contentDetails", mine=True)
    response = request.execute()
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    shorts = []
    next_page_token = None
    target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    while True:
        # Get videos from uploads playlist
        playlist_items = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_items["items"]:
            video_id = item["contentDetails"]["videoId"]
            snippet = item["snippet"]
            published_at = snippet["publishedAt"]
            pub_date = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").date()

            if pub_date != target_date:
                continue

            # Get video metadata
            video_response = youtube.videos().list(
                part="contentDetails,snippet",
                id=video_id
            ).execute()

            video = video_response["items"][0]
            duration = video["contentDetails"]["duration"]
            title = video["snippet"]["title"]
            description = video["snippet"]["description"]
            # Extract hashtags from description
            tags = ", ".join([x for x in video["snippet"]["description"].split() if x.startswith("#")])

            # Filter for Shorts (videos under 60 seconds)
            if "PT" in duration and "M" not in duration and "H" not in duration:
                shorts.append({
                    "id": video_id,
                    "title": title,
                    "description": description,
                    "tags": tags
                })

        next_page_token = playlist_items.get("nextPageToken")
        if not next_page_token:
            break

    return shorts

def download_video(video_id):
    """
    Downloads a YouTube video given its video ID using pytubefix.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(file_extension="mp4", only_video=False, audio_codec='mp4a.40.2').order_by("resolution").desc().first()
    filepath = stream.download(filename=f"{video_id}.mp4")
    return filepath

def upload_to_rumble(driver, video_path, title, description, tags):
    """
    Automates the upload of a video to Rumble, filling in metadata and submitting the form.
    """
    driver.get("https://rumble.com/upload")

    # If login is required, do it
    if "login" in driver.current_url:
        driver.find_element(By.ID, "login-username").send_keys(RUMBLE_EMAIL)
        driver.find_element(By.ID, "login-password").send_keys(RUMBLE_PASSWORD)
        driver.find_element(By.CLASS_NAME, "login-button").click()
        time.sleep(3)

    # Upload the video file
    upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
    upload_input.send_keys(os.path.abspath(video_path))
    time.sleep(5)  # Wait for video to process/upload

    # Fill in metadata
    driver.find_element(By.ID, "title").send_keys(title)
    driver.find_element(By.ID, "description").send_keys(description)
    driver.find_element(By.ID, "tags").send_keys(tags)

    # Select a primary category
    select_primary_category(driver, "Entertainment")

    # Submit first form section
    submit_button = driver.find_element(By.ID, "submitForm")
    driver.execute_script("arguments[0].click();", submit_button)

    time.sleep(2)

    # Accept terms and conditions checkboxes
    accept_rumble_terms(driver)

    # Final submit to publish
    submit_button2 = driver.find_element(By.ID, "submitForm2")
    driver.execute_script("arguments[0].click();", submit_button2)
    time.sleep(10)

def main(date_str):
    """
    Main function to coordinate fetching, downloading, and uploading all shorts for a given date.
    """
    youtube = get_authenticated_service()
    shorts = fetch_shorts_by_date(youtube, date_str)
    print(f"Found {len(shorts)} shorts uploaded on {date_str}.")

    # Set up Chrome browser with default options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome()  # Or use: ChromeDriverManager().install()

    driver.get("https://www.google.com/")  # Load any page to warm up browser

    try:
        for short in shorts:
            print(f"Processing {short['title']}")
            filepath = download_video(short["id"])
            upload_to_rumble(driver, filepath, short["title"], short["description"], short["tags"])
            os.remove(filepath)  # Clean up the downloaded file
    finally:
        driver.quit()

# Entry point
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py YYYY-MM-DD")
    else:
        main(sys.argv[1])
