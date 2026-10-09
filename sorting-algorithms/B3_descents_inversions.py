def count_descents(A):
    """Επιστρέφει τον αριθμό descents της λίστας A,
    δηλαδή το πλήθος των δεικτών i με A[i] > A[i+1]."""
    count = 0
    for i in range(len(A) - 1):
        if A[i] > A[i + 1]:
            count += 1
    return count


def count_inversions(A):
    """Επιστρέφει τον αριθμό αντιστροφών της λίστας A,
    δηλαδή το πλήθος των ζευγών (i, j) με i < j και A[i] > A[j]."""
    count = 0
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i] > A[j]:
                count += 1
    return count


if __name__ == "__main__":
    print(count_descents([1, 2, 3, 4, 5, 6, 7, 8]))   # 0
    print(count_descents([1, 2, 5, 3, 4, 8, 6, 7]))   # 2
    print(count_descents([8, 7, 6, 5, 4, 3, 2, 1]))   # 7

    print(count_inversions([1, 2, 3, 4, 5]))          # 0
    print(count_inversions([2, 1, 3, 5, 4]))          # 2
    print(count_inversions([5, 4, 3, 2, 1]))          # 10

