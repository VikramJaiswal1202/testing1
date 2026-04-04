import re
import subprocess
from typing import List, Dict

class LogParser:
    """Parses application logs to identify errors, stack traces, and dependency failures."""

    ERROR_PATTERNS = [
        re.compile(r"(?i)exception"),
        re.compile(r"(?i)error"),
        re.compile(r"(?i)failed"),
        re.compile(r"(?i)fatal"),
        re.compile(r"(?i)timeout"),
        re.compile(r"(?i)connection refused"),
        re.compile(r"(?i)out of memory"),
    ]

    @staticmethod
    def get_docker_logs(service_name: str, tail: int = 100) -> str:
        """Fetch logs from a local docker-compose service for analysis."""
        try:
            # Assumes running in the root directory where docker-compose.yml lives
            result = subprocess.run(
                ["docker-compose", "logs", "--tail", str(tail), service_name],
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            return f"Error fetching logs: {str(e)}"

    @classmethod
    def analyze_logs(cls, logs: str) -> List[Dict[str, str]]:
        """Find matching error patterns in a log string and return context."""
        findings = []
        lines = logs.split("\n")
        
        for i, line in enumerate(lines):
            for pattern in cls.ERROR_PATTERNS:
                if pattern.search(line):
                    # Gather some context lines around the error
                    start_idx = max(0, i - 2)
                    end_idx = min(len(lines), i + 3)
                    context = "\n".join(lines[start_idx:end_idx])
                    
                    findings.append({
                        "pattern": pattern.pattern,
                        "line": line.strip(),
                        "context": context.strip()
                    })
                    break # Avoid multiple patterns matching the same line
                    
        return findings

    @classmethod
    def analyze_service(cls, service_name: str) -> List[Dict[str, str]]:
        """Convenience method to fetch and analyze logs for a service."""
        logs = cls.get_docker_logs(service_name)
        return cls.analyze_logs(logs)

# Example usage
# if __name__ == "__main__":
#     findings = LogParser.analyze_service("payment-service")
#     print(findings)
