import stripe
import paypalrestsdk
import os
import hashlib
import urllib.parse
from datetime import datetime
from ..memory.state_manager import StateManager

class PaymentAgent:
    def __init__(self, bus, state):
        self.bus = bus
        self.state = state
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        paypalrestsdk.configure({
            "mode": os.getenv("PAYPAL_MODE", "sandbox"),
            "client_id": os.getenv("PAYPAL_CLIENT_ID"),
            "client_secret": os.getenv("PAYPAL_SECRET")
        })
        self.payfast_merchant_id = os.getenv("PAYFAST_MERCHANT_ID")
        self.payfast_merchant_key = os.getenv("PAYFAST_MERCHANT_KEY")
        self.payfast_passphrase = os.getenv("PAYFAST_PASSPHRASE")
        self.payfast_mode = os.getenv("PAYFAST_MODE", "sandbox")
        self.payfast_url = "https://sandbox.payfast.co.za/eng/process" if self.payfast_mode == "sandbox" else "https://www.payfast.co.za/eng/process"

    def run(self):
        self.bus.subscribe('payment_request', self.handle)

    def handle(self, params):
        provider = params.get('provider')
        if provider == 'stripe':
            return self.create_stripe_checkout(params)
        elif provider == 'paypal':
            return self.create_paypal_payment(params)
        elif provider == 'payfast':
            return self.create_payfast_form(params)
        return {'error': 'Unknown provider'}

    def create_stripe_checkout(self, params):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f"Kelnic {params['tier']} Pack"},
                    'unit_amount': int(params['price'] * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://kelnic.com/success',
            cancel_url='https://kelnic.com/cancel',
            customer_email=params.get('email'),
            metadata={'tier': params['tier']}
        )
        return {'url': session.url}

    def create_paypal_payment(self, params):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": params.get('return_url', 'https://kelnic.com/success'),
                "cancel_url": params.get('cancel_url', 'https://kelnic.com/cancel')
            },
            "transactions": [{
                "amount": {"total": str(params['price']), "currency": "USD"},
                "description": f"Kelnic {params['tier']} Pack"
            }]
        })
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return {'url': link.href, 'payment_id': payment.id}
        return {'error': payment.error}

    def create_payfast_form(self, params):
        data = {
            'merchant_id': self.payfast_merchant_id,
            'merchant_key': self.payfast_merchant_key,
            'return_url': 'https://kelnic.com/payfast/success',
            'cancel_url': 'https://kelnic.com/payfast/cancel',
            'notify_url': 'https://api.kelnic.com/webhooks/payfast',
            'name_first': params.get('name', '').split()[0],
            'name_last': params.get('name', '').split()[-1] if len(params.get('name', '').split()) > 1 else '',
            'email_address': params.get('email'),
            'm_payment_id': f"kelnic_{params['tier']}_{int(datetime.utcnow().timestamp())}",
            'amount': f"{params['price']:.2f}",
            'item_name': f"Kelnic {params['tier']} Pack",
            'item_description': "Digital download"
        }
        signature_string = '&'.join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted(data.items()) if v)
        if self.payfast_passphrase:
            signature_string += f"&passphrase={urllib.parse.quote_plus(self.payfast_passphrase)}"
        data['signature'] = hashlib.md5(signature_string.encode()).hexdigest()
        form_html = f'''
        <form id="payfast_form" action="{self.payfast_url}" method="post">
            {''.join(f'<input type="hidden" name="{k}" value="{v}">' for k, v in data.items())}
        </form>
        <script>document.getElementById("payfast_form").submit();</script>
        '''
        return {'html': form_html}

    def handle_webhook(self, provider, payload, sig_header=None):
        if provider == 'stripe':
            return self._handle_stripe_webhook(payload, sig_header)
        return {'error': 'not implemented'}

    def _handle_stripe_webhook(self, payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET"))
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                self._grant_access(session['customer_email'], session['metadata']['tier'])
                self.bus.publish('payment_success', {'email': session['customer_email'], 'tier': session['metadata']['tier'], 'amount': session['amount_total']/100})
            return {'status': 'processed'}
        except Exception as e:
            return {'error': str(e)}

    def _grant_access(self, email, tier):
        # Store in DB and trigger fulfillment
        self.bus.publish('fulfill_order', {'email': email, 'tier': tier})
