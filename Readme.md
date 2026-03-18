# 🚀 Reels → Shorts Automation Platform

A **Streamlit-based content automation tool** that allows you to:

- 📥 Download Instagram Reels
- 🧹 Manage & delete downloaded videos
- 📅 Schedule videos intelligently
- 📤 Upload & schedule them as YouTube Shorts

This project acts like a **mini content management system (CMS)** for creators.

---

# 📌 Table of Contents

1. Project Overview
2. Features
3. Tech Stack
4. Project Structure
5. Setup Instructions
6. Instagram Access Token Setup
7. YouTube API Setup
8. Running the App
9. Workflow
10. Key Components
11. Common Errors & Fixes
12. Future Improvements

---

# 1️⃣ Project Overview

This tool automates:

```

Instagram → Download → Preview → Filter → Schedule → Upload → YouTube Shorts

```

Useful for:

- Content creators
- Social media managers
- Automation enthusiasts

---

# 2️⃣ ✨ Features

## 📥 Download Tab

- Fetch Instagram Reels using API
- Filter by date range
- Skip already downloaded videos
- Auto-save metadata

## 📤 Upload Tab

- Preview videos in grid format
- Select/deselect videos
- Schedule based on:
  - videos per day
  - upload time
  - start & end date
- Upload & schedule to YouTube

## 🗑 Manage Videos Tab

- View all downloaded videos
- Delete selected videos
- Sync with metadata automatically

---

# 3️⃣ 🛠 Tech Stack

| Tool                | Purpose               |
| ------------------- | --------------------- |
| Python              | Core logic            |
| Streamlit           | UI                    |
| Instagram Graph API | Fetch media           |
| YouTube Data API    | Upload videos         |
| python-dotenv       | Environment variables |
| JSON                | Metadata storage      |

---

# 4️⃣ 📁 Project Structure

```

project/
│
├── app.py
├── style.css
├── .env
│
├── services/
│   ├── instagram_service.py
│   └── youtube_service.py
│
├── utils/
│   ├── file_utils.py
│   ├── scheduler.py
│   ├── datetime_utils.py
│   └── caption_parser.py
│
├── instagram_downloads/
│   ├── metadata.json
│   └── *.mp4

```

---

# 5️⃣ ⚙️ Setup Instructions

## ⚙️ Prerequisites

Before running this project, make sure you have:

## 🧰 System Requirements

- Python **3.12+**

## 📦 Package Manager

This project uses:

- **uv** (fast Python package manager)

Install uv: check out https://docs.astral.sh/uv/getting-started/installation/

---

## Step 1: Create Virtual Environment

```bash
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

---

## Step 2: Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## Step 3: Create `.env`

```env
INSTAGRAM_ACCESS_TOKEN=your_token_here
```

---

# 6️⃣ 📥 Instagram Access Token Setup

1. Go to Facebook Developer Portal
2. Create an app
3. Enable Instagram Basic Display API
4. Generate access token

⚠️ Ensure permissions to read media.

---

# 7️⃣ 📤 YouTube API Setup

1. Go to Google Cloud Console
2. Enable **YouTube Data API v3**
3. Create OAuth credentials
4. Download `client_secret.json`
5. Place it in project root

---

# 8️⃣ ▶️ Run the App

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

# 9️⃣ 🔄 Workflow

## Step 1: Download Reels

- Select date range
- Click "Download Reels"
- Videos saved in `instagram_downloads/`

---

## Step 2: Preview & Schedule

- Go to Upload tab
- Click "Preview Schedule"
- Select/deselect videos
- Update schedule

---

## Step 3: Upload

- Provide `client_secret.json`
- Click "Upload & Schedule"

---

## Step 4: Manage Videos

- Delete unwanted videos
- Metadata auto-updates

---

# 🔟 🧠 Key Components

## metadata.json

```json
{
  "video1.mp4": {
    "caption": "Example caption",
    "timestamp": "2025-07-20T10:00:00Z",
    "permalink": "https://..."
  }
}
```

---

## Scheduler

Controls:

- videos per day
- upload time
- start/end date

---

## Session State

Used for:

- schedule
- selected videos
- delete state

---

# 1️⃣1️⃣ ❌ Common Errors & Fixes

## MediaFileStorageError

**Cause:** Missing/corrupt video

**Fix:**

```python
if os.path.exists(video_path):
    st.video(video_path)
```

---

## JSONDecodeError

**Cause:** Empty metadata

**Fix:** Safe JSON loader

---

## KeyError: selected_videos

**Fix:**

```python
if "selected_videos" not in st.session_state:
    st.session_state["selected_videos"] = {}
```

---

## YouTube Upload Issues

Check:

- client_secret.json path
- API enabled
- OAuth configured

---

# 1️⃣2️⃣ 🚀 Future Improvements

## High Impact Features

- Video thumbnails instead of full video loading
- Caption editing before upload
- Drag-and-drop scheduling
- Upload status tracking
- Retry failed uploads

---

# 🏁 Final Thoughts

This project evolves from:

```
Script → Automation Tool → Content Management System
```

You now have:

- Download pipeline
- Scheduling engine
- Upload automation
- Video management

---

# Happy Building 🚀
