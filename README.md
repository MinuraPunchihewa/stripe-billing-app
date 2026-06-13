# Stripe Billing App

A minimal Flask app for learning Stripe Checkout. It displays a product price from Stripe, redirects users to Stripe-hosted Checkout on purchase, and shows success or cancel pages when they return.

## Prerequisites

- Python 3.12+
- A [Stripe](https://stripe.com) account (test mode is fine)
- A Stripe **Price** ID for the product you want to sell

## Setup

1. Clone the repo and install dependencies:

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install flask python-dotenv stripe
   ```

2. Create a `.env` file in the project root:

   ```
   STRIPE_SECRET_KEY=sk_test_...
   ```

   Find your test secret key in the [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys).

3. Set your price ID in `main.py`:

   ```python
   PRICE_ID = "price_..."
   ```

   Create a product and price in the Stripe Dashboard under **Products**, then copy the price ID (starts with `price_`).

## Running

```bash
uv run python main.py
```

Or with Python directly:

```bash
python main.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Routes

| Route     | Description                                      |
| --------- | ------------------------------------------------ |
| `/`       | Product page with live price from Stripe         |
| `/success`| Shown after a successful Checkout payment          |
| `/cancel` | Shown when payment fails or is not completed       |

## Testing payments

Use Stripe test card numbers in Checkout, for example:

- **Success:** `4242 4242 4242 4242`
- **Decline:** `4000 0000 0000 0002`

Use any future expiry date and any 3-digit CVC. See [Stripe test cards](https://docs.stripe.com/testing#cards) for more options.

## Project structure

```
main.py              # Flask app and Stripe Checkout logic
templates/
  base.html          # Shared layout and styles
  index.html         # Product / checkout page
  success.html       # Payment success page
  cancel.html        # Payment cancelled page
```
