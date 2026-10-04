import csv
import matplotlib.pyplot as plt


scenario_data = {
    "low": {"flexibility": [], "savings": []},
    "medium": {"flexibility": [], "savings": []},
    "high": {"flexibility": [], "savings": []}
}


with open("results/scenario_results.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        scenario = row["scenario"]

        scenario_data[scenario]["flexibility"].append(
            int(row["flexibility_hours"])
        )

        scenario_data[scenario]["savings"].append(
            float(row["savings_percent"])
        )


for scenario, data in scenario_data.items():
    plt.plot(
        data["flexibility"],
        data["savings"],
        marker="o",
        label=scenario.capitalize()
    )


plt.xlabel("Scheduling flexibility (hours)")
plt.ylabel("Carbon savings (%)")

plt.title(
    "Effect of Scheduling Flexibility and "
    "Carbon-Intensity Variability"
)

plt.legend(title="Variability")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "results/scenario_comparison.png",
    dpi=300
)

print(
    "Graph saved to "
    "results/scenario_comparison.png"
)