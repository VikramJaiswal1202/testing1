import os
import time
from datetime import datetime
from typing import Dict, Any, List
from autosre.integrations.github_api import GitHubAPI

class ExecutionAgent:
    """Evaluates risk and automatically reports action to the GitHub Actions context."""
    
    def __init__(self, repo_path: str = ".", report_dir: str = "autosre/reports/incident_reports"):
        self.repo_path = repo_path
        self.report_dir = report_dir

    def set_action_output(self, key: str, value: str):
        """Append output variables to the $GITHUB_OUTPUT file so subsequent workflow steps can use them."""
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output and os.path.exists(github_output):
            with open(github_output, "a") as f:
                f.write(f"{key}={value}\n")

    def execute_and_report(self, rca: Dict[str, Any], scored_remediations: List[Dict[str, Any]]):
        """Run the best remediation using remote APIs, and set action outputs."""
        best_fix = scored_remediations[0]
        risk = best_fix.get("risk_score", 100)
        
        action_taken = "None"
        system_status = "Unresolved"
        
        print("\nExecutionAgent: Deciding whether to execute...")
        
        if risk < 30:
            print(f"ExecutionAgent: Risk ({risk}) is below 30. Executing automatically via API: {best_fix['description']}")
            
            action_type = best_fix.get("action")
            target = best_fix.get("target")

            # 1. Take action using GitHub API
            if action_type == "revert_commit":
                GitHubAPI.revert_commit(target)
            elif action_type == "dispatch_workflow":
                service = best_fix.get("service", "unknown-service")
                GitHubAPI.dispatch_workflow("autosre-remediate.yml", {"action": target, "service": service})

            # 2. Output to GitHub Actions environment
            self.set_action_output("executed_action", action_type)
            self.set_action_output("system_status", "Stable")
            
            action_taken = f"{best_fix['description']} executed successfully via Actions API"
            system_status = "Stable (Pending subsequent verification)"
            
        elif risk <= 60:
            print(f"ExecutionAgent: Risk ({risk}) requires manual approval.")
            action_taken = "Pending Manual Approval"
            system_status = "Waiting for human"
        else:
            print(f"ExecutionAgent: Risk ({risk}) is too high. Generating report only.")
            action_taken = "No action taken - Risk too high"
            system_status = "Degraded"
            
        # Generate the report
        self.generate_report(rca, best_fix, action_taken, system_status)

    def generate_report(self, rca: Dict[str, Any], remediation: Dict[str, Any], action_taken: str, system_status: str):
        incident = rca.get("incident_details", {})
        
        report_content = f"""# Incident Report

**Service**: {rca.get('service')}

**Detected Issue**:
{incident.get('description', 'Unknown anomaly')}

**Detection Time**:
{datetime.utcnow().isoformat()}

**Root Cause**:
{rca.get('reason')}

**Remediation**:
{remediation.get('description')}

**Risk Score**:
{remediation.get('risk_score')}

**Action Taken**:
{action_taken}

**System Status**:
{system_status}
"""
        
        os.makedirs(self.report_dir, exist_ok=True)
        filename = f"incident_{int(time.time())}.md"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, "w") as f:
            f.write(report_content)
            
        print(f"\nExecutionAgent: Incident report saved to {filepath}")
