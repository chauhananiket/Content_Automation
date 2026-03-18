import streamlit as st
import os
from datetime import datetime

from utils.file_utils import load_metadata, save_metadata , clean_metadata
from utils.scheduler import generate_schedule
from utils.datetime_utils import utc_to_ist
from dotenv import load_dotenv

from services.instagram_service import (
    get_instagram_media,
    filter_by_date,
    download_media
)

from services.youtube_service import (
    get_authenticated_service,
    upload_video
)

DOWNLOAD_FOLDER = "instagram_downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

METADATA_PATH = os.path.join(DOWNLOAD_FOLDER, "metadata.json")

load_dotenv()
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")


# -----------------------------
# LOAD CSS
# -----------------------------

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# -----------------------------
# STREAMLIT CONFIG
# -----------------------------

st.set_page_config(
    page_title="Reels → Shorts Automation",
    layout="wide"
)

load_css()

# -----------------------------
# HEADER
# -----------------------------

st.title("🚀 Reels → Shorts Automation Platform")

st.write(
    "Download Instagram Reels and automatically schedule them as YouTube Shorts."
)

# -----------------------------
# LOAD METADATA
# -----------------------------

metadata = load_metadata(METADATA_PATH)
metadata = clean_metadata(metadata,DOWNLOAD_FOLDER)


# -----------------------------
# DASHBOARD METRICS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
        <h3>Videos Available</h3>
        <h2>{len(metadata)}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="metric-card">
        <h3>Status</h3>
        <h2>Ready</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="metric-card">
        <h3>Platform</h3>
        <h2>YouTube Shorts</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# TABS
# -----------------------------

# tab1, tab2 = st.tabs(["📥 Download Reels", "📤 Upload Shorts"])
tab1, tab2, tab3 = st.tabs([
    "📥 Download Reels",
    "📤 Upload Shorts",
    "🗑 Manage Videos"
])


# -----------------------------
# DOWNLOAD TAB
# -----------------------------

with tab1:

    st.subheader("Download Instagram Reels")

    access_token = INSTAGRAM_ACCESS_TOKEN

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")
        
    skip_existing = st.checkbox("Skip already downloaded videos", value=True)

    if st.button("Download Reels"):

        media = get_instagram_media(access_token)

        filtered = filter_by_date(
            media,
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.max.time())
        )

        metadata = load_metadata(METADATA_PATH)
        metadata = clean_metadata(metadata, DOWNLOAD_FOLDER)

        
        for item in filtered:
            download_media(item, DOWNLOAD_FOLDER, metadata, skip_existing)

        save_metadata(metadata, METADATA_PATH)
        
        st.success(f"{len(metadata)} videos downloaded")
        
        st.rerun()

# -----------------------------
# UPLOAD TAB
# -----------------------------

if "schedule" not in st.session_state:
    st.session_state["schedule"] = []

if "selected_videos" not in st.session_state:
    st.session_state["selected_videos"] = {}

with tab2:

    st.subheader("Schedule & Upload YouTube Shorts")

    st.info(f"Videos ready: {len(metadata)}")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        videos_per_day = st.number_input("Videos per Day", 1, 20, 5)

    with col2:
        upload_time = st.time_input("Upload Time (IST)")

    with col3:
        start_schedule_date = st.date_input("Start Scheduling Date", min_value="today")

    end_schedule_date = st.date_input("End Scheduling Date (Optional)", value=start_schedule_date, min_value=start_schedule_date)

    client_secret = "client_secret.json"
    
    # ------------------------------------
    # PREVIEW SCHEDULE
    # ------------------------------------

    if st.button("Preview Schedule"):

        sorted_videos = sorted(
            metadata.items(),
            key=lambda x: x[1]["timestamp"]
        )

        videos = [v[0] for v in sorted_videos]

        # schedule = generate_schedule(videos, videos_per_day, upload_time)
        if end_schedule_date < start_schedule_date:
            st.error("End date cannot be before start date.")
            st.stop()
            
        if end_schedule_date == start_schedule_date:
            st.warning("End date is same as start date. End date is freed up to allow scheduling all videos from the start date.")
            schedule = generate_schedule(
                                    videos,
                                    videos_per_day,
                                    upload_time,
                                    start_schedule_date,
                                    None
                                )
        else :        
            schedule = generate_schedule(
                                        videos,
                                        videos_per_day,
                                        upload_time,
                                        start_schedule_date,
                                        end_schedule_date
                                    )
                                            
        st.session_state["schedule"] = schedule

        st.session_state["selected_videos"] = {
            video: True for video, _ in schedule
        }

        st.success("Schedule generated")

    # ------------------------------------
    # SHOW VIDEO GRID PREVIEW
    # ------------------------------------

    if "schedule" in st.session_state:

        schedule = st.session_state["schedule"]

        st.markdown("### 📅 Scheduled Videos Preview")

        cols_per_row = 7

        for i in range(0, len(schedule), cols_per_row):

            cols = st.columns(cols_per_row)

            row_videos = schedule[i:i + cols_per_row]

            for col, (video, publish_time) in zip(cols, row_videos):

                video_path = os.path.join(DOWNLOAD_FOLDER, video)

                with col:

                    st.markdown(
                        '<div class="video-card">',
                        unsafe_allow_html=True
                    )

                    st.video(video_path)

                    st.caption(video)

                    st.markdown(
                        f"**Scheduled:** {utc_to_ist(publish_time)}"
                    )

                    checked = st.checkbox(
                        "Include",
                        value=st.session_state["selected_videos"].get(video, True),
                        key=f"checkbox_{video}"
                    )

                    st.session_state["selected_videos"][video] = checked

                    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------
    # UPDATE SCHEDULE AFTER REMOVAL
    # ------------------------------------

    if "schedule" in st.session_state:

        if st.button("Update Schedule After Selection"):

            selected_videos = [
                video
                for video, selected in st.session_state["selected_videos"].items()
                if selected
            ]

            if len(selected_videos) == 0:
                st.warning("No videos selected.")
                st.stop()

            # regenerate schedule
            new_schedule = generate_schedule(
                selected_videos,
                videos_per_day,
                upload_time
            )

            # update session state
            st.session_state["schedule"] = new_schedule

            # rebuild selected_videos so removed videos disappear
            st.session_state["selected_videos"] = {
                video: True for video, _ in new_schedule
            }

            st.success(
                f"Schedule updated with {len(selected_videos)} videos"
            )
            
            st.rerun()

    # ------------------------------------
    # UPLOAD VIDEOS
    # ------------------------------------

    if "schedule" in st.session_state:

        if st.button("Upload & Schedule Videos"):

            youtube = get_authenticated_service(client_secret)

            schedule = st.session_state["schedule"]

            progress = st.progress(0)

            for i, (video, publish_time) in enumerate(schedule):

                video_path = os.path.join(DOWNLOAD_FOLDER, video)

                caption = metadata[video]["caption"]

                upload_video(
                    youtube,
                    video_path,
                    caption,
                    publish_time
                )

                st.write(
                    f"✅ {video} scheduled → {utc_to_ist(publish_time)}"
                )

                progress.progress((i + 1) / len(schedule))

            st.success("All videos uploaded & scheduled 🚀")
            
# -----------------------------
# TAB 3 — MANAGE VIDEOS
# -----------------------------

with tab3:

    st.subheader("🗑 Manage Downloaded Videos")

    metadata = load_metadata(METADATA_PATH)
    metadata = clean_metadata(metadata, DOWNLOAD_FOLDER)


    if len(metadata) == 0:
        st.info("No videos available")
        st.stop()

    # session state init
    if "delete_videos" not in st.session_state:
        st.session_state["delete_videos"] = {}

    st.markdown("### Select videos to delete")

    cols_per_row = 7

    videos_list = [
                    video for video, _ in sorted(
                        metadata.items(),
                        key=lambda x: x[1]["timestamp"]
                    )
                ]
    

    for i in range(0, len(videos_list), cols_per_row):

        cols = st.columns(cols_per_row)

        row_videos = videos_list[i:i + cols_per_row]

        for col, video in zip(cols, row_videos):

            video_path = os.path.join(DOWNLOAD_FOLDER, video)

            with col:

                st.markdown('<div class="video-card">', unsafe_allow_html=True)

                # if os.path.exists(video_path):
                #     st.video(video_path)
                if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                    st.video(video_path)
                else:
                    st.warning(f"Missing or corrupted file: {video}")

                st.caption(video)

                if video not in st.session_state["delete_videos"]:
                    st.session_state["delete_videos"][video] = False

                delete_checked = st.checkbox(
                    "Delete",
                    value=st.session_state["delete_videos"][video],
                    key=f"delete_{video}"
                )

                st.session_state["delete_videos"][video] = delete_checked

                st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # DELETE BUTTON
    # -----------------------------

    if st.button("Delete Selected Videos"):

        delete_list = [
            video for video, flag in st.session_state["delete_videos"].items()
            if flag
        ]

        if not delete_list:
            st.warning("No videos selected")
            st.stop()

        metadata = load_metadata(METADATA_PATH)
        metadata = clean_metadata(metadata, DOWNLOAD_FOLDER)


        for video in delete_list:

            file_path = os.path.join(DOWNLOAD_FOLDER, video)

            # delete file
            if os.path.exists(file_path):
                os.remove(file_path)

            # remove metadata
            if video in metadata:
                del metadata[video]

        save_metadata(metadata, METADATA_PATH)

        # reset state
        st.session_state["delete_videos"] = {}
        
        st.success(f"Deleted {len(delete_list)} videos")
        
        st.rerun()