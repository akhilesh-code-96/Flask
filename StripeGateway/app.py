from flask import Flask, redirect, render_template, url_for, request, jsonify
import stripe

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51PPqNSJbkURFzj1KHohUlaHfnkftHqY3xuM0LLuW3mpg4sdkYfzGBqTL0J5phBpnb9lkqET9HRbVrgbM18MX4EB200UAV0kGza'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51PPqNSJbkURFzj1KO9Xan2BhMGGv449xmqMZh2mBPeS2IWUzw5NtNjSeA4vQ65gscUiDHDjLAjAmMkrwXhmAXcOa004oF48q1T'

stripe.api_key = app.config['STRIPE_SECRET_KEY']
YOUR_DOMAIN = 'http://localhost:5000'

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/checkout")
def checkout():
  return render_template("checkout.html", stripe_public_key=app.config['STRIPE_PUBLIC_KEY'])

@app.route("/create-checkout-session", methods=['POST'])
def checkout_session():
  data = request.get_json()
  product_id = data.get('product_id')

  try:
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': product_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/thanks',
        cancel_url=YOUR_DOMAIN + '/cancel',
    )
    return jsonify(id=checkout_session.id)
  except Exception as e:
    return jsonify(error=str(e)), 403

@app.route("/thanks")
def thanks():
  return render_template("success.html")

@app.route("/cancel")
def cancel():
  return render_template("cancel.html")

if __name__ == "__main__":
  app.run(debug=True)
