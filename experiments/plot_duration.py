import csv
import matplotlib.pyplot as plt


durations = []
savings = []

with open("results/duration_results.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        durations.append(
            int(row["duration_hours"])
        )
        savings.append(
            float(row["savings_percent"])
        )


plt.plot(
    durations,
    savings,
    marker="o"
)

plt.xlabel("Workload duration (hours)")
plt.ylabel("Carbon savings (%)")
plt.title(
    "Effect of Workload Duration on "
    "Carbon Savings"
)

plt.xticks(durations)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "results/duration_savings.png",
    dpi=300
)

print(
    "Graph saved to "
    "results/duration_savings.png"
)