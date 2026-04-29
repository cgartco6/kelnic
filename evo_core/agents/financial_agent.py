import os
from datetime import datetime
from ..memory.state_manager import StateManager

class FinancialAgent:
    def __init__(self, bus, state):
        self.bus = bus
        self.state = state
        self.upgrade_fund_lower = 0.0
        self.upgrade_fund_upper = 0.0
        self._start_distribution()

    def _start_distribution(self):
        import threading
        import time
        def loop():
            while True:
                self.process_pending_revenue()
                time.sleep(3600)
        threading.Thread(target=loop, daemon=True).start()

    def process_pending_revenue(self):
        # In real implementation, fetch from payment gateways
        # For now, simulate
        pass

    def distribute_revenue(self, amount):
        lower = amount * 0.33
        upper = amount * 0.17
        fnb = amount * 0.30
        african = amount * 0.20

        self.upgrade_fund_lower += lower
        self.upgrade_fund_upper += upper

        # Notify bookkeeper
        self.bus.publish('record_revenue', {'amount': amount, 'provider': 'system'})

        # Store in state
        self.state.save_financial_split({
            'date': datetime.utcnow().isoformat(),
            'lower_upgrade': lower,
            'upper_upgrade': upper,
            'fnb': fnb,
            'african': african
        })

    def get_upgrade_funds(self):
        return {'lower': self.upgrade_fund_lower, 'upper': self.upgrade_fund_upper}
