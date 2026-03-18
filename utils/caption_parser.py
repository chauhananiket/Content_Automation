import re

def parse_caption(caption):

    caption = caption.strip()

    title = caption.split("\n")[0].strip()

    keyword_match = re.search(r"\[(.*?)\]", caption)

    keywords = []
    if keyword_match:
        keywords = [k.strip() for k in keyword_match.group(1).split(",")]

    hashtags = re.findall(r"#\w+", caption)

    return title, caption, keywords, hashtags