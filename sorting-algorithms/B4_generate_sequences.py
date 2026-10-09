import random

from B3_descents_inversions import count_descents, count_inversions


def generate_with_k_descents(n, k, randomize=False):
    """Δημιουργεί ακολουθία μήκους n με ακριβώς k descents, 0 <= k <= n-1.

    Λογική: χωρίζουμε τις τιμές 1..n σε k+1 συνεχόμενα μπλοκ τιμών
    (το πρώτο μπλοκ παίρνει τις μεγαλύτερες τιμές, το τελευταίο τις
    μικρότερες), ταξινομούμε κάθε μπλοκ αύξουσα και τα ενώνουμε.
    Μέσα σε κάθε μπλοκ δεν υπάρχει descent, αλλά σε κάθε ένωση δύο
    διαδοχικών μπλοκ υπάρχει πάντα descent, άρα το σύνολο descents
    ισούται με τον αριθμό των ενώσεων, δηλαδή k.

    Με randomize=True τα μεγέθη των μπλοκ επιλέγονται τυχαία, ώστε
    διαδοχικές κλήσεις να δίνουν διαφορετικές ακολουθίες με το ίδιο k.
    """
    assert 0 <= k <= n - 1

    values = list(range(n, 0, -1))
    num_blocks = k + 1

    if randomize:
        cuts = sorted(random.sample(range(1, n), k))
        bounds = [0] + cuts + [n]
        sizes = [bounds[b + 1] - bounds[b] for b in range(num_blocks)]
    else:
        base_size, extra = divmod(n, num_blocks)
        sizes = [base_size + (1 if b < extra else 0) for b in range(num_blocks)]

    result = []
    idx = 0
    for size in sizes:
        result.extend(sorted(values[idx:idx + size]))
        idx += size
    return result


def generate_with_k_inversions(n, k):
    """Δημιουργεί ακολουθία μήκους n με ακριβώς k αντιστροφές,
    0 <= k <= n*(n-1)//2.

    Λογική: εισάγουμε τους αριθμούς 1, 2, ..., n έναν-έναν σε μια
    λίστα. Όταν εισάγεται ο αριθμός i, αν τοποθετηθεί a θέσεις πριν
    το τέλος της τρέχουσας λίστας, δημιουργούνται ακριβώς a νέες
    αντιστροφές (αφού το i είναι μεγαλύτερο από όλα τα ήδη
    τοποθετημένα στοιχεία). Η μέγιστη δυνατή προσθήκη στο βήμα i
    είναι i-1. Μοιράζουμε άπληστα το k ξεκινώντας από το βήμα με τη
    μεγαλύτερη χωρητικότητα (i = n) προς τα κάτω, μέχρι να
    εξαντληθεί.
    """
    max_k = n * (n - 1) // 2
    assert 0 <= k <= max_k

    add = [0] * (n + 1)
    remaining = k
    for i in range(n, 0, -1):
        capacity = i - 1
        add[i] = min(remaining, capacity)
        remaining -= add[i]

    result = []
    for i in range(1, n + 1):
        pos = len(result) - add[i]
        result.insert(pos, i)
    return result


if __name__ == "__main__":
    for n, k in [(8, 0), (8, 2), (8, 7)]:
        A = generate_with_k_descents(n, k)
        print(f"n={n}, k={k} -> {A}, descents={count_descents(A)}")

    print()
    for _ in range(3):
        A = generate_with_k_descents(8, 2, randomize=True)
        print(f"randomize=True -> {A}, descents={count_descents(A)}")

    print()
    for n, k in [(5, 0), (5, 4), (5, 10)]:
        A = generate_with_k_inversions(n, k)
        print(f"n={n}, k={k} -> {A}, inversions={count_inversions(A)}")
