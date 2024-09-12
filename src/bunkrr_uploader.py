from bunkrr_uploader import main
import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        main()
        exit(0)
    except KeyboardInterrupt:
        logger.warning("Script stopped by user")
        exit(0)
    except Exception:
        logger.exception("Fatal error. Exiting...")
        exit(1)
