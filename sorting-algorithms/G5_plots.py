import csv
from collections import defaultdict

import matplotlib.pyplot as plt

CSV_FILE = "experiment_results.csv"
ALGORITHMS = ["BubbleSort", "InsertionSort", "MergeSort"]
CATEGORY_ORDER = ["sorted", "few_descents", "random", "many_descents", "reverse_sorted"]
MARKERS = {"BubbleSort": "o", "InsertionSort": "s", "MergeSort": "^"}


def load_data(filename=CSV_FILE):
    """Διαβάζει το CSV και επιστρέφει data[category][algorithm] = {n: (avg_time, avg_comparisons)}."""
    data = defaultdict(lambda: defaultdict(dict))
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["n"])
            category = row["category"]
            algorithm = row["algorithm"]
            avg_time = float(row["avg_time_sec"])
            avg_comparisons = float(row["avg_comparisons"])
            data[category][algorithm][n] = (avg_time, avg_comparisons)
    return data


def plot_time_vs_n(data, category="random", filename="plot_time_vs_n.png"):
    """Γράφημα Ι: χρόνος εκτέλεσης ως προς n, για κάθε αλγόριθμο (κατηγορία εισόδου: random)."""
    plt.figure(figsize=(7, 5))
    for algo in ALGORITHMS:
        sizes = sorted(data[category][algo].keys())
        times = [data[category][algo][n][0] for n in sizes]
        plt.plot(sizes, times, marker=MARKERS[algo], label=algo)
    plt.xlabel("n (μέγεθος εισόδου)")
    plt.ylabel("Μέσος χρόνος εκτέλεσης (s)")
    plt.title(f"Χρόνος εκτέλεσης ως προς n (κατηγορία: {category})")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved {filename}")


def plot_comparisons_vs_n(data, category="random", filename="plot_comparisons_vs_n.png"):
    """Γράφημα ΙΙ: αριθμός συγκρίσεων ως προς n, για κάθε αλγόριθμο (κατηγορία εισόδου: random)."""
    plt.figure(figsize=(7, 5))
    for algo in ALGORITHMS:
        sizes = sorted(data[category][algo].keys())
        comparisons = [data[category][algo][n][1] for n in sizes]
        plt.plot(sizes, comparisons, marker=MARKERS[algo], label=algo)
    plt.xlabel("n (μέγεθος εισόδου)")
    plt.ylabel("Μέσος αριθμός συγκρίσεων")
    plt.title(f"Αριθμός συγκρίσεων ως προς n (κατηγορία: {category})")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved {filename}")


def plot_descents_effect(data, n=5000, filename="plot_descents_effect.png"):
    """Γράφημα ΙΙΙ: επίδραση του αριθμού descents (μέσω των κατηγοριών εισόδου, σε
    αύξουσα σειρά presortedness) στον χρόνο εκτέλεσης κάθε αλγορίθμου, για σταθερό n."""
    plt.figure(figsize=(8, 5))
    for algo in ALGORITHMS:
        times = [data[category][algo][n][0] for category in CATEGORY_ORDER]
        plt.plot(CATEGORY_ORDER, times, marker=MARKERS[algo], label=algo)
    plt.xlabel("Κατηγορία εισόδου (αύξων αριθμός descents →)")
    plt.ylabel("Μέσος χρόνος εκτέλεσης (s)")
    plt.title(f"Επίδραση presortedness στον χρόνο εκτέλεσης (n={n})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved {filename}")


def print_random_table(data, category="random"):
    """Τυπώνει πίνακα (κατηγορία: random) με χρόνο & συγκρίσεις ανά αλγόριθμο,
    για όλα τα μεγέθη n -- υποστηρίζει τα γραφήματα 'χρόνος/συγκρίσεις vs n'."""
    print(f"\nResults table for category={category}, all sizes")
    header = f"{'n':>6s} {'algorithm':14s} {'avg_time_sec':>14s} {'avg_comparisons':>16s}"
    print(header)
    print("-" * len(header))
    sizes = sorted(data[category][ALGORITHMS[0]].keys())
    for n in sizes:
        for algo in ALGORITHMS:
            t, c = data[category][algo][n]
            print(f"{n:6d} {algo:14s} {t:14.6f} {c:16.0f}")


def print_summary_table(data, n=5000):
    """Τυπώνει πίνακα (για αντιγραφή στην αναφορά PDF) με χρόνο & συγκρίσεις ανά
    αλγόριθμο και κατηγορία, για σταθερό n."""
    print(f"\nResults table for n={n}")
    header = f"{'category':15s} {'algorithm':14s} {'avg_time_sec':>14s} {'avg_comparisons':>16s}"
    print(header)
    print("-" * len(header))
    for category in CATEGORY_ORDER:
        for algo in ALGORITHMS:
            t, c = data[category][algo][n]
            print(f"{category:15s} {algo:14s} {t:14.6f} {c:16.0f}")


if __name__ == "__main__":
    data = load_data()
    plot_time_vs_n(data)
    plot_comparisons_vs_n(data)
    plot_descents_effect(data)
    print_random_table(data)
    print_summary_table(data)
