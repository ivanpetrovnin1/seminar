import requests


def get_requests_session() -> requests.Session:
    return requests.Session()


def register(api_url: str, username: str, password: str, email: str = None) -> dict:
    url = f"{api_url}/api/auth/register"
    payload = {"username": username, "password": password, "email": email}
    response = requests.post(url, json=payload)
    try:
        return response.json()
    except Exception:
        return {"detail": f"Ошибка регистрации: {response.status_code}"}


def login(api_url: str, username: str, password: str, session: requests.Session) -> dict:
    url = f"{api_url}/api/auth/login"
    payload = {"username": username, "password": password}
    response = session.post(url, json=payload)
    try:
        return response.json()
    except Exception:
        return {"detail": f"Ошибка входа: {response.status_code}"}


def logout(api_url: str, session: requests.Session) -> dict:
    url = f"{api_url}/api/auth/logout"
    response = session.post(url)
    try:
        return response.json()
    except Exception:
        return {"detail": f"Ошибка выхода: {response.status_code}"}


def get_links(api_url: str, session: requests.Session):
    url = f"{api_url}/api/links/list"
    response = session.get(url)

    try:
        data = response.json()
    except Exception:
        return {"detail": "Ошибка получения ссылок"}

    if response.status_code != 200:
        return data

    return data


def create_link(api_url: str, payload: dict, session: requests.Session) -> dict:
    url = f"{api_url}/api/links/create"
    response = session.post(url, json=payload)
    try:
        return response.json()
    except Exception:
        return {"detail": f"Ошибка создания ссылки: {response.status_code}"}

def delete_link(api_url: str, short_code: str, session: requests.Session) -> dict:
    url = f"{api_url}/api/links/delete/{short_code}"
    response = session.delete(url)

    try:
        return response.json() if response.text else {}
    except Exception:
        return {"detail": "Ошибка удаления ссылки"}


def delete_user(api_url: str, session: requests.Session) -> dict:
    url = f"{api_url}/api/auth/user"
    response = session.delete(url)
    try:
        return response.json()
    except Exception:
        return {"detail": f"Ошибка удаления пользователя: {response.status_code}"}