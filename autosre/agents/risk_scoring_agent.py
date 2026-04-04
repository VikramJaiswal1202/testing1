
from typing import Dict, Any, List

class RiskScoringAgent:
    """Assigns a risk score (0-100) to each remediation step. Lower is safer."""
    
    def evaluate_risk(self, rca: Dict[str, Any], remediations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        print("RiskScoringAgent: Evaluating risk for remediation steps...")
        
        scored_remediations = []
        suspected_commit = rca.get("suspected_commit", {})
        files_modified = len(suspected_commit.get("files_changed", []))
        
        for rem in remediations:
            score = 50 # Base default risk
            
            action = rem.get("action")
            
            if action == "dispatch_workflow":
                # Triggering a generic workflow is standard, but check target
                if rem.get("target") == "restart":
                    score = 10
                elif rem.get("target") == "scale":
                    score = 20
                else:
                    score = 30
            elif action == "revert_commit":
                # Risk goes up if the commit touched many files
                # Base is 15. Add 5 per file changed.
                score = 15 + (files_modified * 5)
                # But cap it at 80 so we don't block everything wildly
                score = min(score, 80)
                
            rem_copy = rem.copy()
            rem_copy["risk_score"] = score
            scored_remediations.append(rem_copy)
            print(f"RiskScoringAgent: {rem['description']} -> Risk Score: {score}")
            
        # Return sorted by lowest risk
        scored_remediations.sort(key=lambda x: x["risk_score"])
        return scored_remediations
