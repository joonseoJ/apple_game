import time

def timer(func):
    """함수 실행 시간을 측정하는 데코레이터"""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 시작 시간
        result = func(*args, **kwargs)
        end_time = time.perf_counter()  # 종료 시간
        print(f"⏱ [TIME] {func.__name__} 실행 시간: {end_time - start_time:.6f}초")
        return result
    return wrapper

class TimerContext:
    """with 문을 사용하여 실행 시간을 측정하는 클래스"""
    def __init__(self, name="Block"):
        self.name = name

    def __enter__(self):
        self.start_time = time.perf_counter()

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.perf_counter()
        print(f"⏱ [TIME] {self.name} 실행 시간: {end_time - self.start_time:.6f}초")