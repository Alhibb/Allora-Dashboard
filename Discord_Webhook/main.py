import asyncio
import os
import logging
from typing import Dict, Any

import aiohttp

# Import from your agentipy tools
from agentipy.tools.use_pyth import PythManager
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_allora import (
    AlloraManager,
    PriceInferenceToken,
    PriceInferenceTimeframe,
    ChainSlug
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration variables
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 300))
ALLORA_ENV = os.getenv("ALLORA_ENV", "MAINNET")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  

CHAIN = ChainSlug.MAINNET if ALLORA_ENV.upper() == "MAINNET" else ChainSlug.TESTNET

# Pyth feed addresses for tokens
PYTH_FEEDS: Dict[str, str] = {
    "SOL/USD": "H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG",
    "BTC/USD": "GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU",
    "ETH/USD": "JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB",
    "TRUMP/USD": "A8G6XyA6fSrsavG63ssAGU3Hnt2oDZARxefREzAY5axH",
}


async def send_discord_notification(message: str):
    """
    Send a message to a Discord channel using a webhook.
    """
    if not DISCORD_WEBHOOK_URL:
        logging.warning("Discord webhook URL not set. Skipping Discord notification.")
        return

    async with aiohttp.ClientSession() as session:
        payload = {"content": message}
        try:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                if resp.status not in (200, 204):
                    logging.error(f"Failed to send Discord webhook: HTTP {resp.status}")
                else:
                    logging.info("Discord webhook sent successfully.")
        except Exception as e:
            logging.error(f"Error sending Discord webhook: {str(e)}")


async def get_pyth_data(symbol: str, mint_address: str) -> Dict[str, Any]:
    """
    Fetch Pyth price data and return a dictionary with price and confidence.
    """
    try:
        result = await PythManager.get_price(mint_address)
        if result["status"] == "TRADING":
            return {
                "symbol": symbol,
                "price": result["price"],
                "confidence": result["confidence_interval"]
            }
        else:
            return {"symbol": symbol, "error": f"Status: {result['status']} - {result.get('message', 'No details')}"}
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


async def get_allora_predictions(agent: SolanaAgentKit) -> Dict[str, Dict[str, Any]]:
    """
    Fetch Allora predictions for BTC and ETH and return structured data.
    Returns a dictionary like:
    {
       "BTC": {"5min": {...}, "8hour": {...}},
       "ETH": {"5min": {...}, "8hour": {...}}
    }
    """
    allora = AlloraManager(agent=agent, chain=CHAIN)
    predictions = {}
    try:
        btc_pred_5min = await allora.get_price_prediction(
            PriceInferenceToken.BTC,
            PriceInferenceTimeframe.FIVE_MIN
        )
        eth_pred_5min = await allora.get_price_prediction(
            PriceInferenceToken.ETH,
            PriceInferenceTimeframe.FIVE_MIN
        )
        btc_pred_8hour = await allora.get_price_prediction(
            PriceInferenceToken.BTC,
            PriceInferenceTimeframe.EIGHT_HOURS
        )
        eth_pred_8hour = await allora.get_price_prediction(
            PriceInferenceToken.ETH,
            PriceInferenceTimeframe.EIGHT_HOURS
        )
        predictions["BTC"] = {
            "5min": btc_pred_5min,
            "8hour": btc_pred_8hour,
        }
        predictions["ETH"] = {
            "5min": eth_pred_5min,
            "8hour": eth_pred_8hour,
        }
    except Exception as e:
        predictions["error"] = str(e)
    return predictions


def format_prediction(prediction: Dict[str, Any]) -> str:
    """
    Format prediction data to show predicted price and its confidence.
    Uses the first element of the confidence interval list.
    """
    try:
        pred_price = float(prediction.get("price_prediction", 0))
        confidence_list = prediction.get("confidence_interval", [])
        pred_conf = float(confidence_list[0]) if confidence_list else 0.0
        return f"$ {pred_price:.4f} (Confidence: ±$ {pred_conf:.4f})"
    except Exception:
        return "N/A"


async def main():
    # Create an agent instance for Allora; ensure ALLORA_API_KEY is set in your environment
    api_key = os.getenv('ALLORA_API_KEY', 'UP-20c3607b1068463f884e3796')
    agent = SolanaAgentKit(allora_api_key=api_key)

    while True:
        try:
            # Fetch Pyth data concurrently for each token
            pyth_tasks = [get_pyth_data(symbol, address) for symbol, address in PYTH_FEEDS.items()]
            pyth_results = await asyncio.gather(*pyth_tasks)
            pyth_data = {item["symbol"]: item for item in pyth_results}

            # Fetch Allora predictions for BTC and ETH
            allora_predictions = await get_allora_predictions(agent)

            # Build the combined message
            message_lines = ["Market Update:\n"]
            for symbol in PYTH_FEEDS:
                data = pyth_data.get(symbol, {})
                if "error" in data:
                    message_lines.append(f"{symbol}:\nError fetching data: {data['error']}\n")
                else:
                    current_price = data["price"]
                    current_conf = data["confidence"]
                    line = f"{symbol}:\nCurrent Price: $ {current_price:.4f}\nConfidence: ±$ {current_conf:.4f}"
                    # For BTC/USD and ETH/USD, add predictions if available
                    if symbol in ("BTC/USD", "ETH/USD"):
                        asset = symbol.split("/")[0]  # 'BTC' or 'ETH'
                        pred_5min = allora_predictions.get(asset, {}).get("5min", {})
                        pred_8hour = allora_predictions.get(asset, {}).get("8hour", {})
                        line += (
                            f"\nPredicted Price (5min): {format_prediction(pred_5min)}"
                            f"\nPredicted Price (8hour): {format_prediction(pred_8hour)}"
                        )
                    message_lines.append(line + "\n")
            
            combined_message = "\n".join(message_lines)

            logging.info("Sending combined market update to Discord...")
            await send_discord_notification(combined_message)

            logging.info(f"Sleeping for {SLEEP_INTERVAL} seconds before next cycle...")
            await asyncio.sleep(SLEEP_INTERVAL)
        except Exception as e:
            logging.error(f"Main loop error: {str(e)}")
            await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopped by user")
