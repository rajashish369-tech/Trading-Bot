import argparse
import os
from dotenv import load_dotenv
from bot.client import BinanceFuturesClient
from bot.orders import create_order
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("API keys missing in .env file")
        return

    client = BinanceFuturesClient(api_key, api_secret)

    print("\n=== ORDER SUMMARY ===")
    print(f"Symbol: {args.symbol}")
    print(f"Side: {args.side}")
    print(f"Type: {args.type}")
    print(f"Quantity: {args.quantity}")
    if args.type.upper() == "LIMIT":
        print(f"Price: {args.price}")

    try:
        res = create_order(
            client,
            logger,
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        print("\n✅ Order Placed Successfully!")
        print("Order ID:", res.get("orderId"))
        print("Status:", res.get("status"))
        print("Executed Qty:", res.get("executedQty"))
        print("Avg Price:", res.get("avgPrice"))

    except Exception as e:
        print("❌ Order Failed:", str(e))

if __name__ == "__main__":
    main()
