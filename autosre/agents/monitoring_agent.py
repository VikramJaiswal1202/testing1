from autosre.integrations.prometheus_api import PrometheusAPI
from autosre.services.anomaly_detector import AnomalyDetector
from typing import List, Dict, Any

class MonitoringAgent:
    """Continuously monitors services for anomalies based on metrics."""

    def __init__(self, services_to_monitor: List[str]):
        self.services = services_to_monitor

    def run_check(self) -> List[Dict[str, Any]]:
        """Run a point-in-time check across all services."""
        detected_incidents = []
        
        for service in self.services:
            print(f"MonitoringAgent: Checking {service}...")
            latency = PrometheusAPI.get_service_latency(service)
            error_rate = PrometheusAPI.get_error_rate(service)
            
            metrics = {
                "service": service,
                "latency": latency,
                "error_rate": error_rate
            }
            
            incidents = AnomalyDetector.analyze_metrics(metrics)
            if incidents:
                print(f"MonitoringAgent: Detected {len(incidents)} anomalies for {service}!")
                detected_incidents.extend(incidents)
            
        return detected_incidents
