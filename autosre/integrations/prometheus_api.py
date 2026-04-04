import requests
import os
from typing import Dict, Any, Optional

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

class PrometheusAPI:
    """Interacts with Prometheus to fetch telemetry metrics."""

    @staticmethod
    def query(promql: str) -> Optional[Dict[str, Any]]:
        """Execute a PromQL query."""
        try:
            response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': promql})
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('result', [])
        except Exception as e:
            print(f"Prometheus API Error: {e}")
            return None

    @classmethod
    def get_service_latency(cls, service_name: str) -> Optional[float]:
        """Fetch the p95 API latency for a service."""
        # Simple simulated query or actual PromQL depending on metrics exported
        # Assuming a basic metric exposed by chaos_engine or similar
        # For this prototype we'll fetch basic up status or request dummy metrics
        # If testing with mock frontend/backend, adjust query accordingly
        # Map to the new metric we added in FastAPI
        query = f'histogram_quantile(0.95, rate(http_request_latency_seconds_bucket{{job="{service_name}"}}[5m]))'
        result = cls.query(query)
        
        # Mock logic if empty for testing
        if not result:
            # If no real data, we can mock it for the sake of the AutoSRE testing
            if os.getenv("MOCK_PROMETHEUS") == "true":
                return 900.0 if service_name == "payment-service" else 150.0
            return None
            
        try:
            val_in_seconds = float(result[0]['value'][1])
            if str(val_in_seconds) == "nan": return None
            return val_in_seconds * 1000.0 # Convert to ms for AnomalyDetector
        except (IndexError, KeyError, ValueError, TypeError):
            return None

    @classmethod
    def get_error_rate(cls, service_name: str) -> Optional[float]:
        """Fetch the error rate for a service."""
        query = f'rate(http_requests_errors_total{{job="{service_name}"}}[5m]) / rate(http_requests_total{{job="{service_name}"}}[5m])'
        result = cls.query(query)
        if not result:
            if os.getenv("MOCK_PROMETHEUS") == "true":
                return 0.10 if service_name == "payment-service" else 0.01
            return None
            
        try:
            return float(result[0]['value'][1])
        except (IndexError, KeyError, ValueError):
            return None
