import re


def clean(text):
    text_ = text.replace("\n", " ").replace("\r", " ")
    text_no_pmarks = re.sub(r'[^\w\s]', '', text_)
    text_no_unicode = re.sub(r'[\u1000-\u3000\x00-\x1f\x7f-\x9f]', '', text_no_pmarks)
    clean_text = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        " ",
        text_no_unicode,
    )
    return clean_text
