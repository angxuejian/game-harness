import logging
from pathlib import Path
from datetime import datetime


def setup_loagging() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_path = Path("logs") / f"{timestamp}.txt"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    handlers = [
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(),
    ]
    for handler in handlers:
        handler.addFilter(logging.Filter("game_harness"))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
        force=True,
    )
