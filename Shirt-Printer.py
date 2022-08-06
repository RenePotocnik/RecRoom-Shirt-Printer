import logging

import Encoding
import Importing
from common import setup_logger


def main():
    img, img_data = Encoding.main(list_size=50)

    # Insert beginning and end. Required when using my Image Printer Bot
    img_data.insert(0, "BEGIN")
    img_data.append("END")
    Importing.copy_into_rr_variable(img_data, delay=0.4, pause_at_50=False, stop_at_500=False)


log: logging.Logger = setup_logger()

try:
    main()
    input("Press enter to exit")
except (KeyboardInterrupt, Exception):
    log.exception("ERROR", exc_info=True)
