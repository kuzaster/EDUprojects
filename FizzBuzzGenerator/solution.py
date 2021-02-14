
from typing import Generator


def fizzbuzz(n: int) -> Generator[str, None, None]:
    for i in range(1, n + 1):
        first_if = not bool(i % 15) and "fizzbuzz"
        second_if = not bool(i % 3) and "fizz"
        third_if = not bool(i % 5) and "buzz"
        yield first_if or second_if or third_if or i


# def old_fizzbuzz(n: int) -> Generator[str, None, None]:
#     d = defaultdict(str)
#     for i in range(3, n + 1, 3):
#         d[i] = "fizz"
#     for i in range(5, n + 1, 5):
#         d[i] += "buzz"
#     for i in range(1, n + 1):
#         yield d[i] or str(i)
