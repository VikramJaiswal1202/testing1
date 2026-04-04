from typing import Dict, Any, List

class RemediationAgent:
    """Proposes configuration-agnostic fixes based on RCA to be executed by GitHub Actions."""
    
    def suggest_remediations(self, rca: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return a list of generic remediation step definitions."""
        service = rca.get("service")
        suspected_commit = rca.get("suspected_commit")
        
        print(f"RemediationAgent: Brainstorming fixes for {service}...")
        
        remediations = []
        
        # Action 1: Generic Rollback
        if suspected_commit:
            remediations.append({
                "action": "revert_commit",
                "target": suspected_commit.get('commit_id'),
                "description": f"Revert commit {suspected_commit.get('commit_id')}"
            })
            
        # Action 2: Trigger Deployment/Restart Workflow
        remediations.append({
             "action": "dispatch_workflow",
             "target": "restart",
             "service": service,
             "description": f"Trigger restart/redeploy workflow for {service}"
        })
        
        # Action 3: Scale
        if "latency" in str(rca.get("reason", "")).lower() or "resource" in str(rca.get("reason", "")).lower():
             remediations.append({
                 "action": "dispatch_workflow",
                 "target": "scale",
                 "service": service,
                 "description": f"Trigger scale workflow for {service}"
             })
             
        print(f"RemediationAgent: Proposed {len(remediations)} remediation steps.")
        return remediations
