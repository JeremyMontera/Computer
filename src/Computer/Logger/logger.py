import logging

MAPPING = {0: "LogicCircuit", 1: "Bit"}
# This makes it so we don't have to continously type in where the message is being
# printed from. Later on, this will be replaced with a more robust logging level.

class Logger:

    """
    This class will allow for a basic custom logging method. Later on, when this
    package is more complete (i.e., able to run on the command-line), then this will be
    filled in more.
    """
    
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%I:%M:%S",
        level=logging.INFO,
    )

    @staticmethod
    def info(*, message: str, level: int) -> None:
        """
        This method will forward the message and the level to [`info()`][logging.info].
        This will format the message based on where the message originated from.

        Args:
            message:
                The message to display.
            level:
                Where the message came from.
        """

        logging.info(f"{MAPPING[level]} :: {message}")
