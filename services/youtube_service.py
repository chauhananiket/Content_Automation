import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http

from utils.caption_parser import parse_caption
import streamlit as st


def get_authenticated_service(client_secret):

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret,
        ["https://www.googleapis.com/auth/youtube.upload"]
    )

    credentials = flow.run_local_server(port=8080)

    youtube = googleapiclient.discovery.build(
        "youtube",
        "v3",
        credentials=credentials
    )

    return youtube


def upload_video(youtube, video_path, caption, publish_time):

    title, description, keywords, hashtags = parse_caption(caption)

    # ---------------------------------------
    # Instagram specific words to remove
    # ---------------------------------------

    insta_terms = {
        "reels",
        "reel",
        "reelsinstagram",
        "reelitfeelit",
        "reelkarofeelkaro",
        "reelsvideo",
        "reelsviral",
        "reelstrending",
        "fyp"
    }

    # ---------------------------------------
    # Remove Instagram hashtags
    # ---------------------------------------

    filtered_hashtags = [
        h for h in hashtags
        if h.lower().replace("#", "") not in insta_terms
    ]

    # ---------------------------------------
    # Remove Instagram keywords
    # ---------------------------------------

    filtered_keywords = [
        k for k in keywords
        if k.lower() not in insta_terms
    ]

    # ---------------------------------------
    # YouTube Shorts hashtags
    # ---------------------------------------

    yt_shorts_hashtags = [
        "#shorts",
        "#ytshorts",
        "#youtubeshorts",
        "#lgbtq"
    ]

    # ---------------------------------------
    # Merge hashtags
    # ---------------------------------------

    all_hashtags = list(dict.fromkeys(filtered_hashtags + yt_shorts_hashtags))

    # ---------------------------------------
    # Build tags
    # ---------------------------------------

    tags = filtered_keywords + [h.replace("#", "") for h in all_hashtags]

    tags = list(dict.fromkeys(tags))

    # ---------------------------------------
    # New Description
    # ---------------------------------------

    new_description = title + "\n\n\n" + " ".join(all_hashtags)
    
    # ---------------------------------------
    # Upload request
    # ---------------------------------------

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title[:90],
                "description": new_description,
                "tags": tags,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_time
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True
        )
    )

    response = None

    while response is None:
        status, response = request.next_chunk()

    return publish_time