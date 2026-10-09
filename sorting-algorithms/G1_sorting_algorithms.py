def bubble_sort(A):
    A = A[:]
    n = len(A)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swapped = True
        if not swapped:
            break
    return A


def insertion_sort(A):
    A = A[:]
    n = len(A)
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key
    return A


def merge(left, right):
    i = 0
    j = 0
    result = []
    while i < len(left) and j < len(right):
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


def merge_sort(A):
    if len(A) <= 1:
        return A[:]
    mid = len(A) // 2
    left = merge_sort(A[:mid])
    right = merge_sort(A[mid:])
    return merge(left, right)


if __name__ == "__main__":
    tests = [
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
    ]
    for A in tests:
        print(f"bubble_sort:    {A} -> {bubble_sort(A)}")
    for A in tests:
        print(f"insertion_sort: {A} -> {insertion_sort(A)}")
    for A in tests:
        print(f"merge_sort:     {A} -> {merge_sort(A)}")
