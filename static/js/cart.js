// Shopping cart functionality
class ShoppingCart {
    constructor() {
        this.items = JSON.parse(localStorage.getItem('cart')) || [];
        this.updateCartDisplay();
    }
    
    addItem(item) {
        const existingItem = this.items.find(i => i.id === item.id && i.type === item.type);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({...item, quantity: 1});
        }
        
        this.saveCart();
        this.updateCartDisplay();
    }
    
    removeItem(itemId, itemType) {
        this.items = this.items.filter(item => !(item.id === itemId && item.type === itemType));
        this.saveCart();
        this.updateCartDisplay();
    }
    
    updateQuantity(itemId, itemType, quantity) {
        const item = this.items.find(i => i.id === itemId && i.type === itemType);
        
        if (item) {
            item.quantity = quantity;
            if (item.quantity <= 0) {
                this.removeItem(itemId, itemType);
            } else {
                this.saveCart();
                this.updateCartDisplay();
            }
        }
    }
    
    clearCart() {
        this.items = [];
        this.saveCart();
        this.updateCartDisplay();
    }
    
    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }
    
    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.items));
    }
    
    updateCartDisplay() {
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = this.items.reduce((total, item) => total + item.quantity, 0);
        }
        
        // Update cart sidebar if open
        const cartSidebar = document.getElementById('cart-sidebar');
        if (cartSidebar && cartSidebar.classList.contains('active')) {
            this.renderCartItems();
        }
    }
    
    renderCartItems() {
        const cartItems = document.querySelector('.cart-items');
        if (!cartItems) return;
        
        cartItems.innerHTML = '';
        
        if (this.items.length === 0) {
            cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
            return;
        }
        
        this.items.forEach(item => {
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <div class="cart-item-price">R ${item.price.toLocaleString()} x ${item.quantity}</div>
                </div>
                <div class="cart-item-actions">
                    <button class="quantity-btn minus" data-id="${item.id}" data-type="${item.type}">-</button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="quantity-btn plus" data-id="${item.id}" data-type="${item.type}">+</button>
                    <button class="remove-btn" data-id="${item.id}" data-type="${item.type}">&times;</button>
                </div>
            `;
            cartItems.appendChild(cartItem);
        });
        
        // Add event listeners
        cartItems.querySelectorAll('.quantity-btn.minus').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-id');
                const type = btn.getAttribute('data-type');
                const item = this.items.find(i => i.id === id && i.type === type);
                if (item) {
                    this.updateQuantity(id, type, item.quantity - 1);
                }
            });
        });
        
        cartItems.querySelectorAll('.quantity-btn.plus').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-id');
                const type = btn.getAttribute('data-type');
                const item = this.items.find(i => i.id === id && i.type === type);
                if (item) {
                    this.updateQuantity(id, type, item.quantity + 1);
                }
            });
        });
        
        cartItems.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-id');
                const type = btn.getAttribute('data-type');
                this.removeItem(id, type);
            });
        });
        
        // Update total
        const cartTotal = document.querySelector('.cart-total .currency');
        if (cartTotal) {
            cartTotal.textContent = `R ${this.getTotal().toLocaleString()}`;
        }
    }
}

// Initialize cart
const cart = new ShoppingCart();

// Export for use in other modules
window.ShoppingCart = ShoppingCart;
