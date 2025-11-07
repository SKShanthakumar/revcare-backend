from flask import Flask, render_template, request, redirect
import razorpay

app = Flask(__name__)

# Razorpay API Keys
RAZORPAY_KEY_ID = "rzp_test_jMpRm1HDX5ZT4x"
RAZORPAY_KEY_SECRET = "PERAVYmOCKh4ZygDuRzEJWzi"

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.route('/')
def home():
    return render_template("index.html", key_id=RAZORPAY_KEY_ID)

@app.route('/order', methods=['POST'])
def create_order():
    # Create an order with Razorpay
    amount = 500  # Amount in paise (e.g., ₹500)
    currency = "INR"

    order_data = {
        "amount": amount,
        "currency": currency
    }
    razorpay_order = razorpay_client.order.create(data=order_data)
    return {"order_id": razorpay_order['id'], "amount": amount}

@app.route('/success')
def payment_success():
    return render_template("success.html")  # Render success.html

@app.route('/verify', methods=['POST'])
def verify_signature():
    # Data from Razorpay Checkout
    payment_id = request.form.get("razorpay_payment_id")
    order_id = request.form.get("razorpay_order_id")
    signature = request.form.get("razorpay_signature")

    # Verify signature
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
        return redirect('/success')  # Redirect to success page
    except razorpay.errors.SignatureVerificationError:
        return "Signature verification failed", 400

if __name__ == '__main__':
    app.run(debug=True)
