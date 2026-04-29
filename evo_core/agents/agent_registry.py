# evo_core/agents/agent_registry.py
from evo_core.orchestrator.orchestrator import KelnicOrchestrator
from .marketing_engine_agent import MarketingEngineAgent
from .financial_agent import FinancialAgent
from .invoicing_agent import InvoicingAgent
from .payout_agent import PayoutAgent
from .content_creator_agent import ContentCreatorAgent
from .self_healing_agent import SelfHealingAgent
from .quality_assurance_agent import QualityAssuranceAgent
from .support_agent import SupportAgent
from .payment_agent import PaymentAgent
from .analytics_agent import AnalyticsAgent
from .legal_agent import LegalAgent
from .designer_agent import DesignerAgent
from .monitoring_agent import MonitoringAgent

def register_all_agents(orchestrator: KelnicOrchestrator):
    """Register all agents with the orchestrator"""
    
    agents = [
        MarketingEngineAgent(orchestrator),
        FinancialAgent(orchestrator),
        InvoicingAgent(orchestrator),
        PayoutAgent(orchestrator),
        ContentCreatorAgent(orchestrator),
        SelfHealingAgent(orchestrator),
        QualityAssuranceAgent(orchestrator),
        SupportAgent(orchestrator),
        PaymentAgent(orchestrator),
        AnalyticsAgent(orchestrator),
        LegalAgent(orchestrator),
        DesignerAgent(orchestrator),
        MonitoringAgent(orchestrator),
    ]

    for agent in agents:
        orchestrator.register_agent(agent.name, agent)
    
    # Register MetaAgent separately
    from .meta_agent import MetaAgent
    meta = MetaAgent(orchestrator)
    orchestrator.register_agent("MetaAgent", meta)
    
    orchestrator.logger.info(f"✅ Successfully registered {len(agents) + 1} agents")
