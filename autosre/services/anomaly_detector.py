from typing import Dict, Any, List

class AnomalyDetector:
    """Detects anomalies such as API latency spikes, error rates, and memory leaks."""

    # Configurable thresholds
    THRESHOLDS = {
        "api_latency_ms": 300.0,       # P95 threshold
        "error_rate": 0.05,            # 5% error rate
        "memory_growth_bytes": 50 * 1024 * 1024, # 50MB growth over window
    }

    @classmethod
    def detect_latency_spike(cls, current_latency: float) -> bool:
        """Returns True if current latency exceeds threshold."""
        return current_latency > cls.THRESHOLDS["api_latency_ms"]

    @classmethod
    def detect_error_rate_spike(cls, error_rate: float) -> bool:
        """Returns True if error rate exceeds threshold."""
        return error_rate > cls.THRESHOLDS["error_rate"]

    @classmethod
    def analyze_metrics(cls, metrics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyzes a batch of metrics and returns a list of detected incidents.
        metrics_data example format:
        {
            "service": "payment-service",
            "latency": 900,
            "error_rate": 0.01,
            "memory_usage": 1024000
        }
        """
        incidents = []
        service = metrics_data.get("service", "unknown-service")
        
        latency = metrics_data.get("latency")
        if latency is not None and cls.detect_latency_spike(latency):
            incidents.append({
                "service": service,
                "metric": "API latency",
                "current_value": latency,
                "expected_value": cls.THRESHOLDS["api_latency_ms"],
                "description": f"Latency spike: {latency}ms exceeds {cls.THRESHOLDS['api_latency_ms']}ms",
                "severity": "HIGH"
            })
            
        error_rate = metrics_data.get("error_rate")
        if error_rate is not None and cls.detect_error_rate_spike(error_rate):
            incidents.append({
                "service": service,
                "metric": "Error Rate",
                "current_value": error_rate,
                "expected_value": cls.THRESHOLDS["error_rate"],
                "description": f"Error rate spike: {error_rate} exceeds {cls.THRESHOLDS['error_rate']}",
                "severity": "CRITICAL"
            })
            
        # Add basic memory growth checks here if historical data is passed
        # For a simple stateless check, we might just look at absolute threshold 
        # (e.g. > 1GB) rather than growth unless state is maintained.
        
        return incidents
