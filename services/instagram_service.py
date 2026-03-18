import requests
import os
from dateutil import parser


def get_instagram_media(access_token):

    url = "https://graph.instagram.com/me/media"

    params = {
        "fields": "id,caption,media_type,media_url,timestamp,permalink",
        "access_token": access_token
    }

    media_list = []

    while url:

        response = requests.get(url, params=params)
        data = response.json()

        media_list.extend(data.get("data", []))

        url = data.get("paging", {}).get("next")
        params = None

    return media_list


def filter_by_date(media_list, start_date, end_date):

    filtered = []

    for media in media_list:

        post_time = parser.parse(media["timestamp"]).replace(tzinfo=None)

        if start_date <= post_time <= end_date:
            filtered.append(media)

    return filtered

def download_media(media, folder, metadata, skip_existing=True):

    if media["media_type"] != "VIDEO":
        return

    media_url = media["media_url"]
    media_id = media["id"]

    file_name = f"{media_id}.mp4"
    file_path = os.path.join(folder, file_name)

    # -------------------------------------
    # Skip already downloaded videos
    # -------------------------------------

    if skip_existing and os.path.exists(file_path):
        return

    r = requests.get(media_url)

    with open(file_path, "wb") as f:
        f.write(r.content)

    metadata[file_name] = {
        "caption": media.get("caption", ""),
        "timestamp": media["timestamp"],
        "permalink": media["permalink"]
    }