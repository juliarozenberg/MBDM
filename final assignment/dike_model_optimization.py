from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
)
from ema_workbench.em_framework.optimization import EpsilonProgress
from ema_workbench.util import ema_logging

from problem_formulation import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns
import os
# ...existing code...

def sum_over(*args):
    numbers = []
    for entry in args:
        try:
            value = sum(entry)
        except TypeError:
            value = entry
        numbers.append(value)

    return sum(numbers)


def sum_over_time(*args):
    data = np.asarray(args)
    summed = data.sum(axis=0)
    return summed

archives_dir = "./archives"
os.makedirs(archives_dir, exist_ok=True)

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)


    model, steps = get_model_for_problem_formulation(2)

    reference_values = {
        "Bmax": 175,
        "Brate": 1.5,
        "pfail": 0.5,
        "discount rate 0": 3.5,
        "discount rate 1": 3.5,
        "discount rate 2": 3.5,
        "ID flood wave shape": 4,
    }
    scen1 = {}

    for key in model.uncertainties:
        name_split = key.name.split("_")

        if len(name_split) == 1:
            scen1.update({key.name: reference_values[key.name]})

        else:
            scen1.update({key.name: reference_values[name_split[1]]})

    ref_scenario = Scenario("reference", **scen1)

    convergence_metrics = [EpsilonProgress()]

    espilon = [1e3] * len(model.outcomes)
    # define robustness_functions as all dikemodel.outcomes except Gelderland investment costs and gelderland anual demage

    from ema_workbench.em_framework import sample_uncertainties
    n_scenarios = 2
    scenarios = sample_uncertainties(model, n_scenarios)

    dikemodel = model
    MAXIMIZE = ScalarOutcome.MAXIMIZE
    MINIMIZE = ScalarOutcome.MINIMIZE


    robustness_functions = [
        outcome for outcome in model.outcomes ]

    print(robustness_functions)




    from ema_workbench.em_framework.optimization import ArchiveLogger, EpsilonProgress


    nfe = int(10)

    convergence_metrics = [
        ArchiveLogger(
            "./archives",
            [l.name for l in model.levers],
            [o.name for o in robustness_functions],
            base_filename="robust_optimization.tar.gz",
        ),
        EpsilonProgress(),
    ]


    from ema_workbench import SequentialEvaluator

    with SequentialEvaluator(model) as evaluator:
        results, convergence = evaluator.robust_optimize(
            robustness_functions, scenarios,
            nfe=nfe, epsilons=[0.05,]*len(robustness_functions),
            convergence=convergence_metrics,
        )

        fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True)
        fig, ax1 = plt.subplots(ncols=1)
        ax1.plot(convergence.epsilon_progress)
        ax1.set_xlabel("nr. of generations")
        ax1.set_ylabel(r"$\epsilon$ progress")
        plt.savefig(os.path.join(archives_dir, "convergence_plot.png"))
        sns.despine()
