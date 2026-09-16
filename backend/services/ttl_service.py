import asyncio
import logging
from backend.services.order_services import cleanup_expired_orders

logger = logging.getLogger("ttl_service")
logging.basicConfig(level=logging.INFO)

CLEANUP_INTERVAL_SECONDS = 86400
TTL_DAYS = 30


async def ttl_cleanup_worker(
    interval_seconds: int = CLEANUP_INTERVAL_SECONDS,
    days: int = TTL_DAYS
):
   
    logger.info(
        f"TTL Worker started: Scheduled to run every {interval_seconds}s for orders > {days} days."
    )

    while True:
        try:
            logger.info("TTL Worker: Running scheduled order cleanup...")
            result = cleanup_expired_orders(days=days)
            logger.info(
                f"TTL Worker cleanup complete: {result.get('deletedCount', 0)} order(s) deleted. IDs: {result.get('deletedOrderIds', [])}"
            )
        except asyncio.CancelledError:
            logger.info("TTL Worker received stop/cancel signal. Exiting.")
            break
        except Exception as e:
            logger.error(f"TTL Worker encountered an error: {str(e)}")

        try:
            await asyncio.sleep(interval_seconds)
        except asyncio.CancelledError:
            logger.info("TTL Worker sleep interrupted. Exiting.")
            break
