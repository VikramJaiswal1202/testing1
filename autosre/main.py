import time
import os
from autosre.agents.monitoring_agent import MonitoringAgent
from autosre.agents.incident_analysis_agent import IncidentAnalysisAgent
from autosre.agents.remediation_agent import RemediationAgent
from autosre.agents.risk_scoring_agent import RiskScoringAgent
from autosre.agents.execution_agent import ExecutionAgent

def run_autosre_pipeline():
    """Main orchestration loop for the Agentic DevOps System."""
    
    # 1. Initialize Agents
    # Pull config from Action Inputs
    services_env = os.getenv("SERVICES_CONFIG", "payment-service")
    services_to_monitor = [s.strip() for s in services_env.split(",") if s.strip()]
    
    monitoring_agent = MonitoringAgent(services_to_monitor)
    analysis_agent = IncidentAnalysisAgent()
    remediation_agent = RemediationAgent()
    scoring_agent = RiskScoringAgent()
    
    # Needs to know where the git repo is for running generic workspace commands
    # GITHUB_WORKSPACE is the default checked out cloned directory
    project_root = os.getenv("GITHUB_WORKSPACE", os.getcwd())
    execution_agent = ExecutionAgent(repo_path=project_root)

    print("="*50)
    print("AutoSRE Agentic Pipeline Started")
    print("="*50)

    # 2. Monitor & Detect
    incidents = monitoring_agent.run_check()
    
    if not incidents:
        print("\nPipeline Complete: No incidents detected. System healthy.")
        return

    # Process each incident sequentially
    for incident in incidents:
        print("\n" + "-"*40)
        print(f"Processing Incident: {incident['metric']} on {incident['service']}")
        print("-" * 40)
        
        # 3. Analyze & Explain Root Cause
        rca = analysis_agent.analyze(incident)
        
        # 4. Recommend Fixes
        remediations = remediation_agent.suggest_remediations(rca)
        
        if not remediations:
            print("No remediations could be identified.")
            continue
            
        # 5. Score Risk
        scored_remediations = scoring_agent.evaluate_risk(rca, remediations)
        
        # 6. Execute Fix
        execution_agent.execute_and_report(rca, scored_remediations)

if __name__ == "__main__":
    # Continuous loop or one-off depending on how it's called
    # GitHub Action runs it once. A daemon runs it forever.
    # We will simulate a one-off run.
    print("Starting AutoSRE in REAL Execution Mode:")
    os.environ["MOCK_PROMETHEUS"] = "false"
    os.environ["MOCK_GITHUB"] = "false"
    os.environ["MOCK_GRAFANA"] = "false"
    os.environ["MOCK_EXECUTE"] = "false"
    
    try:
        run_autosre_pipeline()
    except KeyboardInterrupt:
        print("\nAutoSRE shutting down.")
