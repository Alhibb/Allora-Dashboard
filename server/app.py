import asyncio
import os
import logging
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_allora import (
    AlloraManager,
    PriceInferenceToken,
    PriceInferenceTimeframe,
    ChainSlug
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 300))
API_ENV = os.getenv("ALLORA_ENV", "MAINNET")
CHAIN = ChainSlug.MAINNET if API_ENV.upper() == "MAINNET" else ChainSlug.TESTNET

async def main():
    """Main async function to run Allora integration"""
    try:
        api_key = os.getenv('ALLORA_API_KEY', 'UP-20c3607b1068463f884e3796')
        agent = SolanaAgentKit(allora_api_key=api_key)

        allora = AlloraManager(agent=agent, chain=CHAIN)

        while True:
            try:
                # 1. Get price predictions
                btc_prediction_5min = await allora.get_price_prediction(
                    PriceInferenceToken.BTC,
                    PriceInferenceTimeframe.FIVE_MIN
                )
                eth_prediction_5min = await allora.get_price_prediction(
                    PriceInferenceToken.ETH,
                    PriceInferenceTimeframe.FIVE_MIN
                )

                btc_prediction_8hour = await allora.get_price_prediction(
                    PriceInferenceToken.BTC,
                    PriceInferenceTimeframe.EIGHT_HOURS
                )
                eth_prediction_8hour = await allora.get_price_prediction(
                    PriceInferenceToken.ETH,
                    PriceInferenceTimeframe.EIGHT_HOURS
                )

                logging.info(f"BTC (5min) Prediction: {btc_prediction_5min}")
                logging.info(f"ETH (5min) Prediction: {eth_prediction_5min}")
                logging.info(f"BTC (8hour) Prediction: {btc_prediction_8hour}")
                logging.info(f"ETH (8hour) Prediction: {eth_prediction_8hour}")


                logging.info(f"Sleeping for {SLEEP_INTERVAL} seconds before next cycle...")
                await asyncio.sleep(SLEEP_INTERVAL)

            except Exception as e:
                logging.error(f"Main loop error: {str(e)}")
                await asyncio.sleep(60)

    except KeyboardInterrupt:
        logging.info("Stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())