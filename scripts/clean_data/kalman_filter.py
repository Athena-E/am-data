import numpy as np


class KalmanFilter:
    """
    A generic Kalman filter implementation that can track any type of continuous value.
    This filter estimates both the value and its rate of change, adapting to different
    measurement types through customizable initialization parameters.

    Attributes:
        x (numpy.ndarray): State vector containing [value, rate_of_change].
        P (numpy.ndarray): Covariance matrix representing the uncertainty in the state vector.
        R (numpy.ndarray): Measurement noise covariance matrix.
        H (numpy.ndarray): Measurement matrix that defines how the state vector relates to measurements.
        q (float): Process noise parameter that can be tuned for different applications.
    """

    def __init__(self, initial_value=0, measurement_variance=0.1):
        """
        Initialize the Kalman filter with customizable parameters.

        Args:
            initial_value (float): Starting estimate for the value being tracked.
            measurement_variance (float): Expected variance in the measurements.
            initial_value_uncertainty (float): Initial uncertainty in the value estimate.
                If None, defaults to measurement_variance * 100.
            initial_velocity_uncertainty (float): Initial uncertainty in the rate of change.
            process_noise (float): Process noise parameter (q) for the system dynamics.
        """
        # State vector [value, rate_of_change]
        self.x = np.array(
            [[initial_value], [0.0]]
        )  # assume initial rate of change is 0

        self.P = np.array([[1000.0, 0], [0, 1000.0]])

        # Measurement noise (R)
        self.R = np.array([[measurement_variance]])

        # Measurement matrix (H)
        self.H = np.array([[1.0, 0]])  # we only measure the value

        # Process noise parameter
        self.q = 0.001

    def update(self, measured_value, dt):
        """
        Update the filter's estimate based on a new measurement and time step.

        Args:
            measured_value (float): The raw measurement value from the sensor.
            dt (float): Time step in seconds since the last update.

        Returns:
            dict: Dictionary containing:
                - 'value': filtered estimate of the value
                - 'velocity': estimated rate of change
                - 'value_uncertainty': uncertainty in the value estimate
                - 'velocity_uncertainty': uncertainty in the velocity estimate
        """
        # State transition matrix
        F = np.array([[1, dt], [0, 1]])

        # Process noise covariance matrix
        Q = np.array(
            [
                [self.q * dt**3 / 3, self.q * dt**2 / 2],
                [self.q * dt**2 / 2, self.q * dt],
            ]
        )

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

        # Return current state and uncertainties
        return {
            "value": float(self.x[0]),
            "velocity": float(self.x[1]),
            "value_uncertainty": float(self.P[0, 0]),
            "velocity_uncertainty": float(self.P[1, 1]),
        }

    def get_state(self):
        """
        Get the current state estimate and uncertainties.

        Returns:
            dict: Current state and uncertainty values
        """
        return {
            "value": float(self.x[0]),
            "velocity": float(self.x[1]),
            "value_uncertainty": float(self.P[0, 0]),
            "velocity_uncertainty": float(self.P[1, 1]),
        }
