from urllib.parse import urlsplit, parse_qs


def query_to_dict(text: str, url=True) -> dict:
    if url:
        query = urlsplit(text).query
    else:
        query = text
    params = parse_qs(query)
    return {k: v[0] for k, v in params.items()}
