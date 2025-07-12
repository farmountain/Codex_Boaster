from typing import Dict, Any, Callable
import time
from functools import wraps
from backend.logging.structured import PerformanceLogger

performance_logger = PerformanceLogger()

def monitor_performance(component: str, metric: str) -> Callable:
    """Decorator to monitor function performance."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                
                performance_logger.log(
                    component,
                    metric,
                    duration,
                    f"Function {func.__name__} completed successfully"
                )
                return result
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                
                performance_logger.log(
                    component,
                    metric,
                    duration,
                    f"Function {func.__name__} failed: {str(e)}"
                )
                raise
        return wrapper

def monitor_api_endpoint(endpoint: str) -> Callable:
    """Decorator to monitor API endpoint performance."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                
                performance_logger.log(
                    "api",
                    endpoint,
                    duration,
                    f"Endpoint {endpoint} completed successfully"
                )
                return result
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                
                performance_logger.log(
                    "api",
                    endpoint,
                    duration,
                    f"Endpoint {endpoint} failed: {str(e)}"
                )
                raise
        return wrapper

def monitor_database_query(query_type: str) -> Callable:
    """Decorator to monitor database query performance."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                
                performance_logger.log(
                    "database",
                    query_type,
                    duration,
                    f"Query {query_type} completed successfully"
                )
                return result
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                
                performance_logger.log(
                    "database",
                    query_type,
                    duration,
                    f"Query {query_type} failed: {str(e)}"
                )
                raise
        return wrapper
