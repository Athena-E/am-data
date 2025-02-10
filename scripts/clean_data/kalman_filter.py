import numpy as np

class SingleValueKalmanFilter:
    """
    A Kalman filter implementation that estimates a value and its rate of change over time using sensor measurements.

    The filter estimates the value based on noisy measurements and updates its estimate over time by taking into account
    the rate of change (velocity) of the value. It uses a state vector that includes both the value and its rate of change
    and applies the Kalman filter's prediction and update steps.

    Attributes:
        x (numpy.ndarray): State vector containing the value and its rate of change (velocity).
        P (numpy.ndarray): Covariance matrix representing the uncertainty in the state vector.
        R (numpy.ndarray): Measurement noise covariance matrix.
        H (numpy.ndarray): Measurement matrix that defines how the state vector relates to the measurements.

    Methods:
        __init__(initial=0, variance=0.1): Initializes the Kalman filter with an initial value and measurement variance.
        update(measured_value, dt): Updates the filter with a new value measurement and the time step since the last update.
    """

    def __init__(self, initial=0, variance=0.1):
        """
        Initializes the Kalman filter with the given initial value and measurement variance.

        Args:
            initial (float): The initial estimate of the value to be tracked. Default is 0.
            variance (float): The variance (uncertainty) in the measurements. Default is 0.1.
        """
        # State vector [value,value_rate_of_change]
        self.x = np.array([[initial],
                          [0.0]])  # assume initial rate of change is 0
        
        # Initial uncertainty covariance matrix
        self.P = np.array([[1000.0, 0],
                          [0, 1000.0]])  # start with high uncertainty
        
        # Measurement noise (R)
        self.R = np.array([[variance * 100]])
        
        # Measurement matrix (H)
        self.H = np.array([[1.0, 0]])  # we only measure value
        
    def update(self, measured_value, dt):
        """
        Updates the filter's estimate based on a new measurement and time step.

        This method performs the prediction and update steps of the Kalman filter algorithm:
        1. Predict the new state based on the previous state.
        2. Update the state estimate using the new measurement.

        Args:
            measured_value (float): The raw measurement of the value (e.g., from a sensor).
            dt (float): The time step in seconds since the last update (delta time).

        Returns:
            float: The filtered estimate of the value after applying the Kalman filter.
        """
        # State transition matrix
        F = np.array([[1, dt],
                     [0, 1]])
        
        # Process noise covariance matrix
        # Using a simplified continuous white noise model
        q = 30  # process noise parameter (can be tuned)
        Q = np.array([[q * dt**3 / 3, q * dt**2 / 2],
                     [q * dt**2 / 2, q * dt]])
        
        # Predict
        self.x = np.dot(F, self.x)
        self.P = np.dot(np.dot(F, self.P), F.T) + Q
        
        # Update
        z = np.array([[measured_value]])
        y = z - np.dot(self.H, self.x)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        
        self.x = self.x + np.dot(K, y)
        I = np.eye(2)
        self.P = np.dot((I - np.dot(K, self.H)), self.P)
        
        return float(self.x[0])  # return the filtered value