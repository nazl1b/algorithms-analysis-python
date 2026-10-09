import random

from B3_descents_inversions import count_descents, count_inversions
from B4_generate_sequences import generate_with_k_descents


def sorted_sequence(n):
    """Ήδη ταξινομημένη ακολουθία: 0 descents, 0 αντιστροφές."""
    return list(range(1, n + 1))


def reverse_sorted_sequence(n):
    """Αντίστροφα ταξινομημένη ακολουθία: μέγιστος αριθμός descents (n-1)
    και μέγιστος αριθμός αντιστροφών (n*(n-1)/2)."""
    return list(range(n, 0, -1))


def random_sequence(n):
    """Τυχαία ακολουθία (τυχαία μετάθεση των 1..n)."""
    A = list(range(1, n + 1))
    random.shuffle(A)
    return A


def few_descents_sequence(n, k=None):
    """Ακολουθία με μικρό αριθμό descents (περίπου 5% του μέγιστου n-1)."""
    if k is None:
        k = max(1, n // 20)
    k = min(k, n - 1)
    return generate_with_k_descents(n, k, randomize=True)


def many_descents_sequence(n, k=None):
    """Ακολουθία με μεγάλο αριθμό descents (περίπου 80% του μέγιστου n-1),
    χωρίς να φτάνει στο n-1 ώστε να διαφέρει από την πλήρως αντίστροφη."""
    if k is None:
        k = max(1, int(0.8 * (n - 1)))
    k = min(k, n - 1)
    return generate_with_k_descents(n, k, randomize=True)


def generate_all_inputs(n):
    """Επιστρέφει dict {όνομα_κατηγορίας: ακολουθία} με τις 5 κατηγορίες εισόδου
    που ζητά η Δραστηριότητα Γ.3, για δεδομένο μέγεθος n."""
    return {
        "sorted": sorted_sequence(n),
        "reverse_sorted": reverse_sorted_sequence(n),
        "random": random_sequence(n),
        "few_descents": few_descents_sequence(n),
        "many_descents": many_descents_sequence(n),
    }


if __name__ == "__main__":
    n = 20
    inputs = generate_all_inputs(n)
    for name, A in inputs.items():
        print(f"{name:15s} descents={count_descents(A):3d}  inversions={count_inversions(A):4d}  {A}")
