from typing import Dict, Any, Callable, Optional
from functools import wraps
from datetime import datetime
from backend.logging.structured import PerformanceLogger
from backend.logging.config import setup_logger

performance_logger = PerformanceLogger()
monitor_logger = setup_logger("monitor")

def monitor_memory_usage(func: Callable) -> Callable:
    """Decorator to monitor memory usage of a function."""
    import psutil
    
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        process = psutil.Process()
        start_memory = process.memory_info().rss
        
        try:
            result = func(*args, **kwargs)
            end_memory = process.memory_info().rss
            memory_used = end_memory - start_memory
            
            performance_logger.log(
                "memory",
                func.__name__,
                memory_used,
                f"Function {func.__name__} memory usage"
            )
            
            return result
        except Exception as e:
            end_memory = process.memory_info().rss
            memory_used = end_memory - start_memory
            
            performance_logger.log(
                "memory",
                func.__name__,
                memory_used,
                f"Function {func.__name__} failed: {str(e)}"
            )
            raise
    return wrapper

def monitor_cpu_usage(func: Callable) -> Callable:
    """Decorator to monitor CPU usage of a function."""
    import psutil
    
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        process = psutil.Process()
        start_cpu = process.cpu_percent()
        
        try:
            result = func(*args, **kwargs)
            end_cpu = process.cpu_percent()
            cpu_used = end_cpu - start_cpu
            
            performance_logger.log(
                "cpu",
                func.__name__,
                cpu_used,
                f"Function {func.__name__} CPU usage"
            )
            
            return result
        except Exception as e:
            end_cpu = process.cpu_percent()
            cpu_used = end_cpu - start_cpu
            
            performance_logger.log(
                "cpu",
                func.__name__,
                cpu_used,
                f"Function {func.__name__} failed: {str(e)}"
            )
            raise
    return wrapper

def monitor_rate_limit(
    rate: int,
    period: int = 60,
    key: Optional[str] = None
) -> Callable:
    """Decorator to implement rate limiting."""
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    rate_limits = defaultdict(list)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = datetime.now()
            identifier = key or func.__name__
            
            # Clean up old timestamps
            rate_limits[identifier] = [
                t for t in rate_limits[identifier]
                if t > now - timedelta(seconds=period)
            ]
            
            # Check rate limit
            if len(rate_limits[identifier]) >= rate:
                performance_logger.log(
                    "rate_limit",
                    func.__name__,
                    rate,
                    f"Rate limit exceeded for {func.__name__}"
                )
                raise RateLimitExceeded(
                    f"Rate limit exceeded for {func.__name__}: "
                    f"{rate} calls per {period} seconds"
                )
            
            # Add current timestamp
            rate_limits[identifier].append(now)
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                performance_logger.log(
                    "rate_limit",
                    func.__name__,
                    rate,
                    f"Rate limited function failed: {str(e)}"
                )
                raise
        return wrapper

class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    pass

def monitor_api_rate_limit(
    rate: int,
    period: int = 60,
    user_id: Optional[str] = None
) -> Callable:
    """Decorator to implement API rate limiting."""
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    api_limits = defaultdict(list)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = datetime.now()
            identifier = user_id or kwargs.get("user_id", "unknown")
            
            # Clean up old timestamps
            api_limits[identifier] = [
                t for t in api_limits[identifier]
                if t > now - timedelta(seconds=period)
            ]
            
            # Check rate limit
            if len(api_limits[identifier]) >= rate:
                performance_logger.log(
                    "api_rate_limit",
                    func.__name__,
                    rate,
                    f"API rate limit exceeded for user {identifier}"
                )
                raise RateLimitExceeded(
                    f"API rate limit exceeded for user {identifier}: "
                    f"{rate} calls per {period} seconds"
                )
            
            # Add current timestamp
            api_limits[identifier].append(now)
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                performance_logger.log(
                    "api_rate_limit",
                    func.__name__,
                    rate,
                    f"Rate limited API call failed: {str(e)}"
                )
                raise
        return wrapper
