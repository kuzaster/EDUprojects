import types

from solution import fizzbuzz


def test_fizzbuzz_is_generator():
    actual_results = fizzbuzz(5)
    assert isinstance(actual_results, types.GeneratorType)


def test_fizzbuzz_is_fizz():
    N = 15
    actual_results = list(fizzbuzz(N))
    for i in range(3, N + 1, 3):
        assert actual_results[i - 1].startswith("fizz")


def test_fizzbuzz_is_buzz():
    N = 15
    actual_results = list(fizzbuzz(N))
    for i in range(5, N + 1, 5):
        assert actual_results[i - 1].endswith("buzz")


def test_fizzbuzz_is_fizzbuzz():
    N = 45
    actual_results = list(fizzbuzz(N))
    for i in range(15, N + 1, 15):
        assert actual_results[i - 1] == "fizzbuzz"
