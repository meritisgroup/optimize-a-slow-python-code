import time


def process_ml_batch(name):
    """
    Every time a user requested a name we process an ML batch.

    The user won't need the result of the ML batch, the result of the batch
    will be saved into business tables and will be useful for us
    to know if he is a potential client.
    """
    time.sleep(0.2)
    pass
