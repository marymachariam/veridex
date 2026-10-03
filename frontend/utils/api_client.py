import requests
import streamlit as st

from config import settings


class APIError(Exception):
    """Raised when the API rejects a request; the message is safe to show to the user."""


class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.timeout = settings.API_TIMEOUT

    def _headers(self):
        token = st.session_state.get("token")
        return {"Authorization": f"Bearer {token}"} if token else {}

    @staticmethod
    def _detail(response):
        try:
            detail = response.json().get("detail")
        except Exception:
            return f"Request failed ({response.status_code})"
        if isinstance(detail, list):  # validation errors: include which field failed
            parts = []
            for item in detail:
                loc = item.get("loc", [])
                field = loc[-1] if loc else "field"
                parts.append(f"{field}: {item.get('msg', 'Invalid input')}")
            return "; ".join(parts)
        return str(detail or f"Request failed ({response.status_code})")

    def _request(self, method, path, *, raise_on_error=False, default=None, **kwargs):
        try:
            response = requests.request(
                method, f"{self.base_url}{path}", headers=self._headers(), timeout=self.timeout, **kwargs
            )
        except requests.RequestException as exc:
            if raise_on_error:
                raise APIError("Cannot reach the server. Please try again.") from exc
            return default

        if response.status_code == 401:
            st.session_state.pop("token", None)  # expired token: next page load sends the user to login
        if response.status_code >= 400:
            if raise_on_error:
                raise APIError(self._detail(response))
            return default
        return response.json() if response.content else default

    def health_check(self):
        try:
            return requests.get(f"{self.base_url}/health", timeout=self.timeout).status_code == 200
        except requests.RequestException:
            return False

    # ---- reads (return [] / {} on failure so pages never crash) ----
    def get_all_competitors(self, limit=500):
        return self._request("GET", "/api/v1/competitors", params={"limit": min(limit, 500)}, default=[])

    def get_all_pricing(self, limit=500):
        return self._request("GET", "/api/v1/pricing", params={"limit": min(limit, 500)}, default=[])

    def get_all_reviews(self, limit=500):
        return self._request("GET", "/api/v1/reviews", params={"limit": min(limit, 500)}, default=[])

    def get_all_price_history(self, limit=500):
        return self._request("GET", "/api/v1/price-history", params={"limit": min(limit, 500)}, default=[])

    def get_dashboard_summary(self):
        return self._request("GET", "/api/v1/dashboard/summary", default={})

    def get_research_history(self, search=None, limit=100, offset=0):
        params = {"limit": limit, "offset": offset}
        if search:
            params["search"] = search
        return self._request("GET", "/api/v1/history", params=params, default=[])

    def get_research_history_item(self, history_id):
        return self._request("GET", f"/api/v1/history/{history_id}", default=None)

    # ---- writes (raise APIError with a readable message) ----
    def create_competitor(self, data):
        return self._request("POST", "/api/v1/competitors", json=data, raise_on_error=True)

    def create_pricing(self, data):
        return self._request("POST", "/api/v1/pricing", json=data, raise_on_error=True)

    def create_review(self, data):
        return self._request("POST", "/api/v1/reviews", json=data, raise_on_error=True)

    def create_price_change(self, data):
        return self._request("POST", "/api/v1/price-history", json=data, raise_on_error=True)

    def delete_research_history_item(self, history_id):
        return self._request("DELETE", f"/api/v1/history/{history_id}", raise_on_error=True)

    def register_user(self, data):
        return self._request("POST", "/api/v1/auth/register", json=data, raise_on_error=True)

    def login_user(self, username, password):
        result = self._request(
            "POST", "/api/v1/auth/login", json={"username": username, "password": password}, raise_on_error=True
        )
        if result and "access_token" in result:
            st.session_state["token"] = result["access_token"]
        return result


api_client = APIClient()