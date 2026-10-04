import csv
import matplotlib.pyplot as plt

flexibility = []
savings = []

with open("results/flexibility_results.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        flexibility.append(int(row["flexibility_hours"]))
        savings.append(float(row["savings_percent"]))

plt.plot(flexibility, savings, marker="o")

plt.xlabel("Scheduling flexibility (hours)")
plt.ylabel("Carbon savings (%)")
plt.title("Effect of Scheduling Flexibility on Carbon Savings")

plt.grid(True)
plt.tight_layout()

plt.savefig("results/flexibility_savings.png", dpi=300)

print("Graph saved to reuslts/flexibility_savings.png")

