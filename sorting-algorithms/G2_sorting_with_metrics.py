import time


def bubble_sort_metrics(A):
    """Bubble sort που επιστρέφει (ταξινομημένη λίστα, αριθμός συγκρίσεων, χρόνος σε δευτερόλεπτα)."""
    A = A[:]
    n = len(A)
    comparisons = 0
    start = time.perf_counter()
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            comparisons += 1
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swapped = True
        if not swapped:
            break
    elapsed = time.perf_counter() - start
    return A, comparisons, elapsed


def insertion_sort_metrics(A):
    """Insertion sort που επιστρέφει (ταξινομημένη λίστα, αριθμός συγκρίσεων, χρόνος σε δευτερόλεπτα)."""
    A = A[:]
    n = len(A)
    comparisons = 0
    start = time.perf_counter()
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if A[j] > key:
                A[j + 1] = A[j]
                j -= 1
            else:
                break
        A[j + 1] = key
    elapsed = time.perf_counter() - start
    return A, comparisons, elapsed


def _merge_metrics(left, right, counter):
    i = j = 0
    result = []
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def _merge_sort_helper(A, counter):
    if len(A) <= 1:
        return A[:]
    mid = len(A) // 2
    left = _merge_sort_helper(A[:mid], counter)
    right = _merge_sort_helper(A[mid:], counter)
    return _merge_metrics(left, right, counter)


def merge_sort_metrics(A):
    """Merge sort που επιστρέφει (ταξινομημένη λίστα, αριθμός συγκρίσεων, χρόνος σε δευτερόλεπτα)."""
    counter = [0]
    start = time.perf_counter()
    result = _merge_sort_helper(A, counter)
    elapsed = time.perf_counter() - start
    return result, counter[0], elapsed


if __name__ == "__main__":
    import random

    tests = [
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
    ]

    for A in tests:
        for name, func in [
            ("bubble_sort_metrics", bubble_sort_metrics),
            ("insertion_sort_metrics", insertion_sort_metrics),
            ("merge_sort_metrics", merge_sort_metrics),
        ]:
            result, comparisons, elapsed = func(A)
            assert result == sorted(A), f"{name} failed on {A}"
            print(f"{name:22s} {A} -> {result}, comparisons={comparisons}, time={elapsed:.8f}s")

    print()
    print("Test with larger random list (n=2000):")
    big = [random.randint(0, 10000) for _ in range(2000)]
    for name, func in [
        ("bubble_sort_metrics", bubble_sort_metrics),
        ("insertion_sort_metrics", insertion_sort_metrics),
        ("merge_sort_metrics", merge_sort_metrics),
    ]:
        result, comparisons, elapsed = func(big)
        assert result == sorted(big), f"{name} failed on big list"
        print(f"{name:22s} comparisons={comparisons}, time={elapsed:.6f}s")
