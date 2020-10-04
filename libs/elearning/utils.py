import requests


def is_valid_token(
    token: str, url="https://elearning.ut.ac.id/webservice/rest/server.php"
) -> bool:
    if len(token) != 32:
        return False
    params = {"wstoken": token, "wsfunction": "core_webservice_get_site_info"}
    res = requests.get(url, params=params)
    return "invalidtoken" not in res.text if res.ok else False
