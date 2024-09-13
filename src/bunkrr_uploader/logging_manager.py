import logging, __main__
from pathlib import Path
from datetime import datetime
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

CONSOLE_THEME = Theme({
    "logging.level.warning": "yellow",
    "logging.level.debug": "blue",
    "logging.level.info": "white",
    "logging.level.error": "red"})

RICH_CONSOLE = Console (theme = CONSOLE_THEME)

RICH_HANDLER_CONFIG = {
    'show_time': False, 
    'rich_tracebacks': True, 
    'tracebacks_show_locals': False
}

class LogFileConfig(int):
    def __init__(self, value):
        self.value = value
    
NO_LOG_FILE = LogFileConfig(0)
USE_PROJECT_NAME = LogFileConfig(1)
USE_MAIN_NAME = LogFileConfig(2)

def setup_logger(*,
        log_file: LogFileConfig | Path | str = NO_LOG_FILE ,
        log_level: int = logging.DEBUG, 
        logs_folder_overrride: Path | str = None,
        datetime_as_suffix : bool = True,
        rich_console_handler: bool = True
        ) -> None:
    
    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.CRITICAL)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if rich_console_handler:
        console_handler = RichHandler(**RICH_HANDLER_CONFIG, level = log_level, console = RICH_CONSOLE )
        logger.addHandler(console_handler)

    main = Path(__main__.__file__)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    log_file_path = None
    default_log_folder = main.parent / "logs"
    log_folder = Path(logs_folder_overrride) if logs_folder_overrride else default_log_folder

    if log_file:
        
        if log_file == USE_PROJECT_NAME:
            log_file_path = log_folder / main.parent.with_suffix('.log').name 

        elif log_file == USE_MAIN_NAME:
            log_file_path = log_folder / main.with_suffix('.log').name 

        else:
            log_file_path = Path (log_file)

    if log_file_path:
        if datetime_as_suffix:
            log_file_path = log_file_path.parent / f'{log_file_path.stem}_{current_time}.log' 

        log_file_path.parent.mkdir(exist_ok=True)
        file_handler = RichHandler(**RICH_HANDLER_CONFIG, level = logging.DEBUG, 
                                   console = Console(file = log_file_path.open("a", encoding = "utf8")) )
        logger.addHandler(file_handler)   

if __name__ == '__main__':
    raise NotImplementedError