"""
Circuit breaker for external API calls.
Prevents cascading failures when external services (like Gemini API) fail.
"""
import time
from typing import Optional


class CircuitBreaker:
    """
    Simple circuit breaker implementation.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Service is failing, requests fail fast
    - HALF_OPEN: Testing if service recovered
    """

    def __init__(self, failure_threshold: int = 3, timeout: int = 60):
        """
        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting recovery
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"

    def call(self, func, *args, **kwargs):
        """
        Execute function through circuit breaker.

        Returns:
            Function result if successful

        Raises:
            Exception: If circuit is open or function fails
        """
        if self.state == "OPEN":
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = "HALF_OPEN"
            else:
                wait_time = int(
                    self.timeout - (time.time() - self.last_failure_time))
                raise Exception(
                    f"Circuit breaker is OPEN. Service unavailable. "
                    f"Retry in {wait_time} seconds."
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def get_state(self) -> dict:
        """Get current circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
        }


# THIS LINE IS CRITICAL - Make sure it's at the bottom
gemini_circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=60)
