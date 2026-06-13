import os

import stripe
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

app = Flask(__name__)

PRICE_ID = "price_1ThkmlAe3ux7fBdcJzJNtXy7"

CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
}


def format_price(price_obj):
    amount = price_obj.unit_amount / 100
    currency = price_obj.currency.upper()
    symbol = CURRENCY_SYMBOLS.get(currency, '')
    if symbol:
        return f"{symbol}{amount:.2f}"
    return f"{amount:.2f} {currency}"


def price_note(price_obj):
    if price_obj.type == 'recurring':
        interval = price_obj.recurring.interval
        return f"Recurring · billed every {interval}"
    return "One-time payment · No subscription"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': PRICE_ID,
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('index', _external=True),
        )

        return redirect(checkout_session.url, code=303)

    price_obj = stripe.Price.retrieve(PRICE_ID)
    return render_template(
        'index.html',
        formatted_price=format_price(price_obj),
        price_note=price_note(price_obj),
    )    


@app.route('/success')
def success():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    
    if session.payment_status == 'paid':
        return render_template('success.html')
    else:
        return redirect(url_for('cancel'))


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


if __name__ == '__main__':
    app.run(debug=True)