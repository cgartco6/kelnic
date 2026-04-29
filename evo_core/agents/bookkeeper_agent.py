from datetime import datetime
from ..memory.state_manager import StateManager

class BookkeeperAgent:
    def __init__(self, bus, state):
        self.bus = bus
        self.state = state
        self._subscribe()

    def _subscribe(self):
        self.bus.subscribe('payment_success', self.record_revenue)
        self.bus.subscribe('payout_executed', self.record_payout)
        self.bus.subscribe('upgrade_spent', self.record_upgrade_cost)

    def record_revenue(self, event):
        transaction = {
            'date': datetime.utcnow().isoformat(),
            'type': 'revenue',
            'amount': event['amount'],
            'source': event.get('provider', 'unknown'),
            'customer_email': event.get('email')
        }
        self._double_entry(transaction, 'cash', 'revenue')

    def record_payout(self, event):
        transaction = {
            'date': datetime.utcnow().isoformat(),
            'type': 'payout',
            'amount': event['amount'],
            'bank': event['bank']
        }
        self._double_entry(transaction, 'owner_equity', 'cash')

    def record_upgrade_cost(self, event):
        transaction = {
            'date': datetime.utcnow().isoformat(),
            'type': 'infrastructure',
            'amount': event['cost'],
            'resource': event['resource']
        }
        self._double_entry(transaction, 'cash', 'operating_expense')

    def _double_entry(self, transaction, debit_account, credit_account):
        self.state.save_journal_entry({
            'transaction': transaction,
            'debit': debit_account,
            'credit': credit_account,
            'amount': transaction['amount']
        })
