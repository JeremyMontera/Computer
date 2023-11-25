import time
from typing import Optional

MAPPING = {
    0: "LogicGate",
    1: "Compound Factory",
    2: "Compound Gate",
    3: "Connection",
    4: "Branch",
    5: "Switch",
    6: "Loop",
    7: "Standard Input",
    8: "Standard Output",
}
# This makes it so we don't have to continously type in where the message is being
# printed from. Later on, this will be replaced with a more robust logging level.


class Logger:

    """
    This class will allow for a basic custom logging method. Later on, when this
    package is more complete (i.e., able to run on the command-line), then this will be
    filled in more.
    """

    @staticmethod
    def info(message: str, level: Optional[int] = None) -> None:
        """
        This method will forward the message and the level to [`info()`][logging.info].
        This will format the message based on where the message originated from.

        TODO: actually do this when we are ready to do so...

        Args:
            message:
                The message to display.
            level:
                Where the message came from.
        """
        if level is None:
            raise ValueError("You need to provide a valid logging level!")

        current_time: str = time.strftime("%H:%M:%S")
        print(f"[{current_time}] {MAPPING[level]} :: {message}")
