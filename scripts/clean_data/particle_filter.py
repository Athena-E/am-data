import numpy as np
from numpy.random import normal

class ParticleFilter:
    def __init__(self, num_particles, process_variance_rate, measurement_variance, initial_value=0):
        """
        Initialize particle filter
        
        Args:
            num_particles: Number of particles to use
            process_variance_rate: Variance rate in the process model (per unit time)
            measurement_variance: Variance in the measurement model
        """
        self.num_particles = num_particles
        self.process_variance_rate = process_variance_rate  # Variance per unit time
        self.measurement_variance = measurement_variance
        
        # Initialize particles and weights
        self.particles = np.ones(num_particles) * initial_value
        self.weights = np.ones(num_particles) / num_particles
    
    def predict(self, dt):
        """
        Predict step: Move particles according to process model
        
        Args:
            dt: Time step size (time elapsed since last update)
        """
        # Scale process noise by time step
        scaled_variance = self.process_variance_rate * dt
        self.particles += normal(0, np.sqrt(scaled_variance), self.num_particles)


    def update(self, value, dt):
        """
        Update step: Update weights based on measurement
        
        Args:
            measurement: Measurement object containing timestamp and value
        """
        # First predict up to the measurement time
        if dt > 0:
            self.predict(dt)
        
        # Calculate likelihood of measurement given each particle
        likelihoods = np.exp(-0.5 * ((value - self.particles)**2) / 
                            self.measurement_variance) / np.sqrt(2 * np.pi * self.measurement_variance)
        
        # Update weights
        self.weights *= likelihoods
        self.weights += 1e-300  # Avoid numerical underflow
        self.weights /= sum(self.weights)  # Normalize weights
        
        # Resample if effective sample size is too low
        if self.effective_sample_size() < self.num_particles / 2:
            self.resample()
    
    def effective_sample_size(self):
        """Calculate the effective sample size to determine when to resample"""
        return 1.0 / np.sum(self.weights ** 2)
    
    def resample(self):
        """
        Resample particles based on their weights
        """
        cumsum = np.cumsum(self.weights)
        cumsum[-1] = 1.0  # Handle numerical errors
        
        # Generate random numbers for resampling
        indices = np.searchsorted(cumsum, np.random.random(self.num_particles))
        
        # Resample particles and reset weights
        self.particles = self.particles[indices]
        self.weights = np.ones(self.num_particles) / self.num_particles
    
    def estimate(self):
        """
        Return weighted average of particles as state estimate
        """
        return np.sum(self.particles * self.weights)