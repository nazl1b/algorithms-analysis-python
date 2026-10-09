import csv
import statistics

from G2_sorting_with_metrics import (
    bubble_sort_metrics,
    insertion_sort_metrics,
    merge_sort_metrics,
)
from G3_input_generators import (
    sorted_sequence,
    reverse_sorted_sequence,
    random_sequence,
    few_descents_sequence,
    many_descents_sequence,
)

SIZES = [100, 500, 1000, 2000, 5000]
REPETITIONS = 10

ALGORITHMS = {
    "BubbleSort": bubble_sort_metrics,
    "InsertionSort": insertion_sort_metrics,
    "MergeSort": merge_sort_metrics,
}

CATEGORIES = {
    "sorted": sorted_sequence,
    "reverse_sorted": reverse_sorted_sequence,
    "random": random_sequence,
    "few_descents": few_descents_sequence,
    "many_descents": many_descents_sequence,
}


def run_experiments(sizes=SIZES, repetitions=REPETITIONS, verbose=True):
    """Τρέχει κάθε αλγόριθμο πάνω σε κάθε κατηγορία εισόδου, για κάθε
    μέγεθος n. Σε κάθε επανάληψη δημιουργείται ΜΙΑ ΝΕΑ ακολουθία και οι
    ΤΡΕΙΣ αλγόριθμοι τρέχουν πάνω στην ΙΔΙΑ ακολουθία (paired comparison),
    ώστε η σύγκριση μεταξύ αλγορίθμων να γίνεται πάνω στα ίδια δεδομένα
    σε κάθε επανάληψη. Καταγράφονται ο μέσος χρόνος και ο μέσος αριθμός
    συγκρίσεων ανά αλγόριθμο.
    """
    results = []
    for n in sizes:
        for category_name, generator in CATEGORIES.items():
            times = {algo_name: [] for algo_name in ALGORITHMS}
            comparisons_list = {algo_name: [] for algo_name in ALGORITHMS}
            for _ in range(repetitions):
                A = generator(n)
                for algo_name, algo_func in ALGORITHMS.items():
                    _, comparisons, elapsed = algo_func(A)
                    times[algo_name].append(elapsed)
                    comparisons_list[algo_name].append(comparisons)
            for algo_name in ALGORITHMS:
                avg_time = statistics.mean(times[algo_name])
                avg_comparisons = statistics.mean(comparisons_list[algo_name])
                results.append({
                    "n": n,
                    "category": category_name,
                    "algorithm": algo_name,
                    "avg_time_sec": avg_time,
                    "avg_comparisons": avg_comparisons,
                })
                if verbose:
                    print(f"n={n:5d} {category_name:15s} {algo_name:14s} "
                          f"avg_time={avg_time:.6f}s avg_comparisons={avg_comparisons:.0f}")
    return results


def save_to_csv(results, filename="experiment_results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "category", "algorithm", "avg_time_sec", "avg_comparisons"])
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    results = run_experiments()
    save_to_csv(results)
    print(f"\nSaved {len(results)} rows to experiment_results.csv")
