import requests
import os
from typing import Dict, Any, Optional

GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3001")
# For production use API keys. Using Anonymous/Admin for local docker-compose setup
GRAFANA_AUTH = (os.getenv("GRAFANA_USER", "admin"), os.getenv("GRAFANA_PASSWORD", "admin"))

class GrafanaAPI:
    """Interacts with Grafana to pull dashboards, alerts, or datasource proxies."""

    @staticmethod
    def get_dashboard(uid: str) -> Optional[Dict[str, Any]]:
        """Fetch dashboard definition by UID."""
        try:
            response = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/{uid}", auth=GRAFANA_AUTH)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Grafana API Error: {e}")
            return None
            
    @staticmethod
    def check_alerts() -> list:
        """Fetch firing alerts from Grafana."""
        try:
            response = requests.get(f"{GRAFANA_URL}/api/v1/alerts", auth=GRAFANA_AUTH)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Grafana API Alert Error: {e}")
            # Mock
            if os.getenv("MOCK_GRAFANA") == "true":
                return [{"labels": {"alertname": "HighLatency", "service": "payment-service"}, "state": "firing"}]
            return []
