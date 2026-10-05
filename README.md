# Carbon-Aware Workload Scheduling Simulator

A Python simulator for investigating the potential carbon savings of shifting computational workloads to lower-carbon periods.

## Research Question

**How does workload flexibility affect the potential carbon savings achievable through temporal workload shifting?**

The project compares a baseline scheduler, which executes a workload as soon as it becomes available, with a carbon-aware scheduler that searches for the lowest-carbon execution window available before the workload deadline.

## How It Works

Each workload is represented as a job with:

- an earliest start time
- a deadline
- a duration
- a power requirement

The baseline scheduler executes the job at its earliest possible start time.

The carbon-aware scheduler evaluates each valid hourly start time between the earliest start and latest possible start. It estimates the emissions associated with each execution window and selects the lowest-carbon option.

For an hourly timestep:

`Energy (kWh) = Power (kW) × Time (h)`

and:

`Emissions (gCO2e) = Energy (kWh) × Carbon Intensity (gCO2e/kWh)`

## Experiment 1: Scheduling Flexibility

A two-hour, 1 kW workload was evaluated with:

- 0 hours flexibility
- 1 hour flexibility
- 3 hours flexibility
- 6 hours flexibility

The initial synthetic carbon-intensity trace demonstrated that additional flexibility can provide access to lower-carbon execution windows.

However, flexibility alone does not guarantee savings. If newly available execution periods have equal or higher carbon intensity, the scheduler retains the earlier start time.

| Flexibility | Baseline emissions (gCO2e) | Green emissions (gCO2e) | Savings |
| ---: | ---: | ---: | ---: |
| 0h | 470 | 470 | 0.0% |
| 1h | 470 | 470 | 0.0% |
| 3h | 470 | 380 | 19.1% |
| 6h | 470 | 220 | 53.2% |

![Effect of scheduling flexibility](results/flexibility_savings.png)

## Experiment 2: Carbon-Intensity Variability

Three synthetic carbon-intensity scenarios were created with the same mean intensity of **200 gCO2e/kWh**, but different levels of temporal variability.

| Scenario | Mean (gCO2e/kWh) | Standard deviation (gCO2e/kWh) |
| --- | ---: | ---: |
| Low variability | 200.0 | 5.8 |
| Medium variability | 200.0 | 31.6 |
| High variability | 200.0 | 80.0 |

The same two-hour workload was tested at each flexibility level.

| Flexibility | Low variability | Medium variability | High variability |
| --- | ---: | ---: | ---: |
| 0h | 0.0% | 0.0% | 0.0% |
| 1h | 0.0% | 0.0% | 0.0% |
| 3h | 3.6% | 14.6% | 26.7% |
| 6h | 7.2% | 35.4% | 66.7% |

These controlled simulations suggest that the value of scheduling flexibility depends strongly on temporal variation in carbon intensity. Greater flexibility creates more scheduling opportunities, but substantial carbon savings require sufficiently lower-carbon periods to exist within the available scheduling window.

![Scenario comparison](results/scenario_comparison.png)

## Experiment 3: Workload Duration

To investigate how workload characteristics affect carbon-aware scheduling, workloads of different durations were evaluated using a fixed six-hour scheduling flexibility window.

The workloads had durations of 1, 2 and 4 hours and were evaluated against the same synthetic carbon-intensity trace.

| Duration | Baseline emissions (gCO2e) | Green emissions (gCO2e) | Savings |
| ---: | ---: | ---: | ---: |
| 1h | 280 | 120 | 57.1% |
| 2h | 600 | 200 | 66.7% |
| 4h | 1120 | 480 | 57.1% |

The results show that carbon savings do not necessarily increase or decrease monotonically with workload duration. Instead, the achievable saving depends on how the workload duration aligns with the timing and length of lower-carbon periods.

In this synthetic trace, the two-hour workload aligned particularly well with the lowest-carbon period, while the four-hour workload also had to execute during surrounding higher-carbon hours.

![Workload duration results](results/duration_savings.png)

## Project Structure

```text
data/           Carbon-intensity datasets
experiments/    Experiment and plotting scripts
report/         Technical research report
results/        Generated experimental results and figures
src/            Scheduler, models, emissions and data-loading code
tests/          Automated unit tests
```

## Running the Project

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the automated tests:

```bash
python -m unittest discover -v
```

Run the three experiments:

```bash
python -m experiments.flexibility_experiment
python -m experiments.scenario_experiment
python -m experiments.duration_experiment
```

Generate the figures:

```bash
python -m experiments.plot_flexibility
python -m experiments.plot_scenarios
python -m experiments.plot_duration
```

## Current Assumptions and Limitations

The current simulator:

- uses synthetic carbon-intensity data
- assumes carbon intensity is known in advance
- uses hourly scheduling resolution
- models non-preemptive workloads that run continuously once started
- assumes constant power consumption during execution
- currently models a single workload without compute-capacity constraints

These assumptions keep the model transparent and allow the effects of scheduling flexibility, carbon-intensity variability and workload duration to be investigated systematically.

## Research Report

A more detailed discussion of the methodology, experimental design, results, limitations and relevant carbon-aware computing research is available in the full technical report:

**[Read the full research report](report/report.md)**

## Future Work

Potential extensions include using real-world carbon-intensity data, modelling multiple workloads and compute-capacity constraints, investigating forecast uncertainty, variable workload power profiles, finer scheduling resolution, and alternative strategies for handling incomplete carbon-intensity data.