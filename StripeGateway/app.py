from flask import Flask, redirect, render_template, url_for, request, jsonify
import stripe
from dotenv import load_dotenv
import os

app = Flask(__name__) # Initialize

def configure():
  load_dotenv()

app.config['STRIPE_PUBLIC_KEY'] = os.getenv('api_pub')
app.config['STRIPE_SECRET_KEY'] = os.getenv('api_secret')

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
  configure()
  app.run(debug=True)
