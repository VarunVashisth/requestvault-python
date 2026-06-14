import random

from ..config import Config


def should_sample():

    try:

        return (
            random.random()
            <= Config.sample_rate
        )

    except Exception:

        return True