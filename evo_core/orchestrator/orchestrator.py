import threading
from .message_bus import MessageBus
from ..agents import *
from ..memory.state_manager import StateManager

class Orchestrator:
    def __init__(self):
        self.bus = MessageBus()
        self.state = StateManager()
        self.agents = {
            'strategist': StrategistAgent(self.bus, self.state),
            'designer': DesignerAgent(self.bus, self.state),
            'scriptwriter': ScriptwriterAgent(self.bus, self.state),
            'voice_artist': VoiceArtistAgent(self.bus, self.state),
            'funnel_builder': FunnelBuilderAgent(self.bus, self.state),
            'optimizer': OptimizerAgent(self.bus, self.state),
            'feedback_analyzer': FeedbackAnalyzerAgent(self.bus, self.state),
            'meta': MetaAgent(self.bus, self.state),
            'code_verifier': CodeVerifierAgent(self.bus, self.state),
            'compliance': ComplianceAgent(self.bus, self.state),
            'payment': PaymentAgent(self.bus, self.state),
            'marketplace': MarketplaceAgent(self.bus, self.state),
            'support': SupportAgent(self.bus, self.state),
            'legal': LegalAgent(self.bus, self.state),
            'monitoring': MonitoringAgent(self.bus, self.state),
            'chatbot': ChatbotAgent(self.bus, self.state),
            'customization': CustomizationAgent(self.bus, self.state),
            'analytics': AnalyticsAgent(self.bus, self.state),
            'affiliate': AffiliateAgent(self.bus, self.state),
            'social': SocialAgent(self.bus, self.state),
            'white_label': WhiteLabelAgent(self.bus, self.state),
            'community': CommunityAgent(self.bus, self.state),
            'personalization': PersonalizationAgent(self.bus, self.state),
            'blockchain': BlockchainAgent(self.bus, self.state),
            'predictive': PredictiveAgent(self.bus, self.state),
            'voice_control': VoiceControlAgent(self.bus, self.state),
            'ar_preview': ARPreviewAgent(self.bus, self.state),
            'gap_detector': GapDetectorAgent(self.bus, self.state),
            'marketing_engine': MarketingEngineAgent(self.bus, self.state),
            'revenue_tracker': RevenueTrackerAgent(self.bus, self.state),
            'content_creator': ContentCreatorAgent(self.bus, self.state),
            'landing_page': LandingPageAgent(self.bus, self.state),
            'promotion': PromotionAgent(self.bus, self.state),
            'quality_assurance': QualityAssuranceAgent(self.bus, self.state),
            'alex': AlexMonitoringAgent(self.bus, self.state),
            'financial': FinancialAgent(self.bus, self.state),
            'self_healing': SelfHealingAgent(self.bus, self.state),
            'reporting': ReportingAgent(self.bus, self.state),
            'upgrade': UpgradeAgent(self.bus, self.state),
            'bookkeeper': BookkeeperAgent(self.bus, self.state),
            'invoicing': InvoicingAgent(self.bus, self.state),
            'payout': PayoutAgent(self.bus, self.state),
        }
        self._setup_routes()

    def _setup_routes(self):
        self.routes = {
            'create_new_template': self.agents['designer'].handle,
            'modify_funnel': self.agents['funnel_builder'].handle,
            'generate_script': self.agents['scriptwriter'].handle,
            'generate_voice': self.agents['voice_artist'].handle,
            'optimize': self.agents['optimizer'].handle,
            'analyze_feedback': self.agents['feedback_analyzer'].handle,
            'evolve': self.agents['meta'].handle,
            'verify_code': self.agents['code_verifier'].handle,
            'check_compliance': self.agents['compliance'].handle,
            'payment_webhook': self.agents['payment'].handle_webhook,
            'publish_marketplace': self.agents['marketplace'].publish,
            'customer_support': self.agents['support'].handle_query,
            'update_legal': self.agents['legal'].update_rules,
            'monitor_usage': self.agents['monitoring']._collect_all_metrics,
            'chat_message': self.agents['chatbot'].handle_message,
            'user_activity': self.agents['chatbot'].handle_activity,
            'social_reply_posted': self.agents['alex'].handle_reply,
            'qa_alert': self.agents['quality_assurance'].run_all_checks,
            'launch_campaign': self.agents['marketing_engine'].launch_campaign,
            'track_campaign': self.agents['marketing_engine'].track_campaign,
            'generate_marketing_content': self.agents['content_creator'].handle,
            'build_landing_page': self.agents['landing_page'].handle,
            'create_promotion': self.agents['promotion'].create_discount_code,
            'record_revenue': self.agents['bookkeeper'].record_revenue,
            'record_payout': self.agents['bookkeeper'].record_payout,
            'check_upgrade': self.agents['upgrade'].check_and_upgrade,
        }

    def start(self):
        self.bus.subscribe('orchestrator', self._dispatch)
        for agent in self.agents.values():
            threading.Thread(target=agent.run, daemon=True).start()
        while True:
            pass

    def _dispatch(self, event):
        action = event.get('action')
        if action in self.routes:
            self.routes[action](event.get('params', {}))
        else:
            print(f"Unknown action: {action}")

def main():
    orch = Orchestrator()
    orch.start()

if __name__ == "__main__":
    main()
