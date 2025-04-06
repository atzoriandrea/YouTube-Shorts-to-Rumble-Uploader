# 🎬 YouTube Shorts to Rumble Uploader

This project downloads all **YouTube Shorts uploaded on a specific date** from **your YouTube channel**, and **automatically reuploads them to your Rumble account**, preserving titles, descriptions, and hashtags.

> ✅ Perfect if you want to cross-post your content to reach a wider audience.

---

## ⭐ Support This Project

If you found this project useful or interesting, please consider giving it a **star** ⭐ on GitHub! It helps others discover it and keeps the project going.

👉 Just click the ⭐ button at the top-right of the [repository page](https://github.com/atzoriandrea/YouTube-Shorts-to-Rumble-Uploader)!

Thanks for your support! 🙏


---

## 📸 What It Does

- Authenticates with your **YouTube account** using OAuth.
- Filters for **Shorts (videos under 60 seconds)** uploaded on a specific day.
- Downloads them using a patched version of `pytube`.
- Logs into **Rumble**, uploads the videos, fills out titles, descriptions, tags, categories, and agrees to terms.
- All done automatically via browser automation (`Selenium`).

---

## 🧠 Who Is This For?

- Creators with a YouTube channel and Rumble account  
- People with **no coding experience**  
- Users who can follow instructions step-by-step 🙌

---

## 🛠 Requirements

You'll need:

- A **Google Cloud account** for YouTube API access  
- A **Rumble account**  
- Python 3.9 or newer installed  

---

## 🧪 Step-by-Step Setup Guide

### 1. 🔽 Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-shorts-to-rumble.git
cd youtube-shorts-to-rumble
```

### 2. 🐍 Set Up Python & Install Dependencies

First, make sure you have **Python 3.9 or newer** installed. You can check this by running:

```bash
python --version
```

### ✅ (Optional) Create a Virtual Environment
This helps keep your dependencies clean and isolated.

```
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows
```

### 📦 Install Required Python Packages
Use the provided requirements.txt file:


```
pip install -r requirements.txt
```
If you don’t have requirements.txt, you can install everything manually:

```
pip install pytubefix python-dotenv selenium google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client webdriver-manager
```
## 🧰 Installing ChromeDriver (Windows & Linux)

This script uses **Google Chrome + ChromeDriver** for browser automation. You must have:

- ✅ Google Chrome installed
- ✅ ChromeDriver that matches your Chrome version

---

### ⚡ Easiest Method: Let the Script Install ChromeDriver Automatically

The script uses `webdriver-manager`, which downloads and sets up ChromeDriver for you.

Just make sure it's installed:

```bash
pip install webdriver-manager
```

Then in your Python code, Chrome will launch like this:

```python
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
```

No need to manually download anything if this works for you!

---

### 🧱 Manual Installation (Windows)

1. Open Google Chrome and go to `chrome://settings/help`  
   Note your **Chrome version** (e.g., `114.0.5735.90`)

2. Go to: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)  
   Download the version that matches your Chrome version.

3. Extract the ZIP file

4. Move `chromedriver.exe` into a known folder, like:

```
C:\tools\chromedriver\
```

5. Add that folder to your **System PATH**:
   - Open Start > search "Environment Variables"
   - Edit the `PATH` variable
   - Add the folder path (e.g., `C:\tools\chromedriver\`)

6. Restart your terminal and test it:

```bash
chromedriver --version
```

---

### 🧱 Manual Installation (Linux)

1. Check your Chrome version:

```bash
google-chrome --version
```

2. Download the matching ChromeDriver from:  
   [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

3. Extract the archive:

```bash
unzip chromedriver_linux64.zip
```

4. Move it to `/usr/local/bin`:

```bash
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

5. Verify it's installed:

```bash
chromedriver --version
```

---

✅ Once ChromeDriver is installed and accessible from your `PATH`, you're good to go!


### 3. 🔐 Get Your YouTube API OAuth Credentials

In order to access your own YouTube videos, you need to create an OAuth 2.0 Client ID from Google Cloud. Follow these steps **exactly**, even if you've never used Google Cloud before.

---

#### ✅ Step-by-Step Instructions

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. At the top-left, click the **project dropdown** and select **"New Project"**.
3. Name your project something like `YT Shorts API` and click **Create**.
4. After it's created, make sure the project is selected.

---

#### 🧠 Enable the YouTube Data API

5. In the left sidebar, go to:  
   **APIs & Services > Library**
6. Search for **YouTube Data API v3** and click it.
7. Click the blue **Enable** button.

---

#### 🔑 Create OAuth Credentials

8. In the sidebar, go to:  
   **APIs & Services > Credentials**
9. Click the **+ CREATE CREDENTIALS** button.
10. Choose **OAuth client ID**.
11. When asked to set up a screen, click **Configure Consent Screen**:
    - Choose **External**
    - App name: `YT Shorts Tool` (or anything)
    - Add your email as the user support email
    - Add your email as a test user under "Test Users"
    - Save and continue until you can click **Back to Dashboard**
12. Now continue creating the OAuth client:
    - Choose **Desktop App**
    - Name it something like `YouTube API Access`
    - Click **Create**

---

#### 💾 Download the Credentials

13. After creation, click the **Download JSON** button.
14. Rename the file to: client_secret.json

15. Move this file to the **same folder** as your `main.py` script.

---

✅ You're now ready to authenticate with your YouTube account in the next step!

## 🚀 Running the Script

Once everything is set up, run the script with a specific date:

```bash
python main.py YYYY-MM-DD
```

Replace `YYYY-MM-DD` with the date you want to fetch YouTube Shorts from. For example:

```bash
python main.py 2025-04-05
```

---

## ✅ Example Output

```text
Found 2 shorts uploaded on 2025-04-05.
Processing My Funny Short #1
Processing Cat Does Backflip #2
```

---

## 🧼 What It Does Behind the Scenes

- Authenticates to YouTube
- Downloads Shorts uploaded on a given date
- Logs into Rumble using your `.env` credentials
- Uploads the video file
- Fills in:
  - ✅ Title  
  - ✅ Description  
  - ✅ Tags (from hashtags in the description)  
  - ✅ Primary Category (`Entertainment`)  
  - ✅ Required checkboxes (terms and rights)
- Publishes the video

---

## 🛑 Troubleshooting

### ❌ Chrome doesn’t open

- Make sure you have **Google Chrome** installed
- The script uses `webdriver-manager` to download the right driver

---

### ❌ YouTube OAuth not working

- Make sure your file is named `client_secret.json`
- You must use **OAuth Desktop App**, not Web or Service Account

---

### ❌ Rumble upload fails

- Double-check your credentials in the `.env` file
- Solve any CAPTCHA manually if it pops up the first time

## 🔐 Creating the `.env` File (Windows & Linux)

The `.env` file is where you securely store your **Rumble login credentials** so the script can log in automatically.

---

### 🪟 Windows

1. Open **Notepad**
2. Paste the following lines (replace with your actual credentials):

```env
RUMBLE_EMAIL=your-email@example.com
RUMBLE_PASSWORD=yourrumblepassword
YT_SECRET=client_secret.json
```

3. Click **File > Save As**
4. In the **"Save as type"** dropdown, select **"All Files"**
5. Save the file as:

```
.env
```

in the **same folder** as `main.py`.

✅ Done!

---

### 🐧 Linux / macOS

1. Open your terminal
2. Navigate to the folder where `main.py` is located
3. Run:

```bash
nano .env
```

4. Paste the following (replace with your actual credentials):

```env
RUMBLE_EMAIL=your-email@example.com
RUMBLE_PASSWORD=yourrumblepassword
```

5. Press `CTRL + O` to save, then `ENTER`  
6. Press `CTRL + X` to exit

✅ Your `.env` file is now ready!

---

⚠️ **Important:**  
- The `.env` file should be kept **private** and never shared.
- Do **not** upload it to GitHub. Add `.env` to your `.gitignore` file.


---

## 📁 Example Project Structure

```text
youtube-shorts-to-rumble/
├── main.py
├── client_secret.json
├── .env
├── README.md
```

---

## 🧑‍💻 Contributing

Pull requests welcome! If you run into issues, feel free to open an issue.

---

## 📜 License

MIT — Free for personal or commercial use.

