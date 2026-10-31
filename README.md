# Razorpay Test Orders API

A backend-only practice project for creating and retrieving Razorpay **Test Mode** orders. It uses FastAPI, SQLAlchemy 2.x async ORM, PostgreSQL, and the Razorpay Python SDK. There is no frontend, login, webhook, or payment verification flow.

## Files

- `app/config/settings.py`: loads database and Razorpay credentials from environment using Pydantic Settings.
- `app/config/database.py`: creates the async SQLAlchemy engine, session factory, and FastAPI session dependency.
- `app/config/razorpay_config.py`: creates the SDK client from the test key pair.
- `app/models/`: SQLAlchemy mapped product and payment tables; payment amounts are stored as paise.
- `app/schemas/`: Pydantic v2 request and response schemas.
- `app/repositories/`: database queries for products and payments.
- `app/services/`: order and product business logic, separate from HTTP routing.
- `app/routers/`: Swagger-visible endpoints.
- `app/main.py`: application, lifespan table creation, and router registration.
- `sql/setup.sql`: database and sample-product SQL.

## Setup

1. Create a PostgreSQL database. Run `CREATE DATABASE payment_db;` as a PostgreSQL superuser, or use `sql/setup.sql`.
2. Copy `.env.example` to `.env`, then set `DATABASE_URL` and your Razorpay **Test Mode** key ID and secret. Never commit `.env`.
3. Install and run:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

   Or use `python` in place of `py` if that is your Python launcher. Tables are created at startup. To add sample products, connect to `payment_db` in `psql` and execute the `INSERT` portion of `sql/setup.sql` (or add rows with your SQL client).

4. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API workflow

1. `GET /products` and choose a product ID.
2. `POST /payments/create-order` with `{"product_id": 1}`. The API reads the price from PostgreSQL; clients cannot supply an amount.
3. The response includes the local payment ID, Razorpay order ID, amount in paise, and currency.
4. `GET /payments` or `GET /payments/{payment_id}` to inspect the local record.
5. `GET /payments/razorpay-order/{order_id}` to fetch the current order from Razorpay.
6. Inspect the order in your Razorpay Test Dashboard.

## SDK calls

- `razorpay.Client(auth=(key_id, key_secret))` builds the authenticated SDK client.
- `client.order.create(data={...})` creates an order. Razorpay expects `amount` as an integer in the smallest currency unit (paise for INR).
- `client.order.fetch(order_id)` retrieves an order by Razorpay order ID.

The SDK uses synchronous HTTP requests. Both operations run via `asyncio.to_thread` so they do not block the FastAPI event loop. The secret is used only for SDK authentication and is never part of an API response.
