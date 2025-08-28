// Payment functionality
class PaymentProcessor {
    constructor() {
        this.initializePaymentForm();
    }
    
    initializePaymentForm() {
        const paymentForm = document.getElementById('payment-form');
        if (!paymentForm) return;
        
        paymentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.processPayment();
        });
        
        // Format card number
        const cardNumberInput = document.getElementById('card-number');
        if (cardNumberInput) {
            cardNumberInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 16) value = value.slice(0, 16);
                
                // Add spaces every 4 digits
                value = value.replace(/(\d{4})/g, '$1 ').trim();
                e.target.value = value;
            });
        }
        
        // Format expiry date
        const expiryInput = document.getElementById('card-expiry');
        if (expiryInput) {
            expiryInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 4) value = value.slice(0, 4);
                
                if (value.length > 2) {
                    value = value.slice(0, 2) + '/' + value.slice(2);
                }
                
                e.target.value = value;
            });
        }
    }
    
    async processPayment() {
        const paymentForm = document.getElementById('payment-form');
        const payButton = document.getElementById('pay-now');
        const loadingText = 'Processing...';
        
        if (payButton.textContent === loadingText) return;
        
        const originalText = payButton.textContent;
        payButton.textContent = loadingText;
        payButton.disabled = true;
        
        try {
            // Get form data
            const cardNumber = document.getElementById('card-number').value.replace(/\s/g, '');
            const cardName = document.getElementById('card-name').value;
            const cardExpiry = document.getElementById('card-expiry').value.split('/');
            const cardCvv = document.getElementById('card-cvv').value;
            
            const cardDetails = {
                number: cardNumber,
                name: cardName,
                exp_month: cardExpiry[0] || '',
                exp_year: cardExpiry[1] || '',
                cvv: cardCvv
            };
            
            // Get cart items
            const cart = window.ShoppingCart ? window.ShoppingCart.items : [];
            const total = window.ShoppingCart ? window.ShoppingCart.getTotal() : 0;
            
            // Send payment request
            const response = await fetch('/api/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    amount: total,
                    card_details: cardDetails,
                    items: cart
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Payment successful
                alert('Payment processed successfully! Your order ID is: ' + data.order_id);
                
                // Clear cart
                if (window.ShoppingCart) {
                    window.ShoppingCart.clearCart();
                }
                
                // Redirect to dashboard
                window.location.href = '/dashboard';
            } else {
                // Payment failed
                alert('Payment failed: ' + data.error);
            }
        } catch (error) {
            console.error('Payment error:', error);
            alert('An error occurred during payment processing. Please try again.');
        } finally {
            payButton.textContent = originalText;
            payButton.disabled = false;
        }
    }
}

// Initialize payment processor
document.addEventListener('DOMContentLoaded', () => {
    new PaymentProcessor();
});
