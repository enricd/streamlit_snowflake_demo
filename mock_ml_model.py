import numpy as np
from time import sleep

class MockModel:

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Mock prediction function that returns the last value of the input Series with 5 rows of noise.
        """
        # Generate random predictions
        noise = np.random.normal(X[-1], 0.8, size=(20,))
        preds = noise.astype(np.int8)
        preds[preds < 0] = 0
        sleep(3)  # Simulate a delay for the prediction process

        return preds