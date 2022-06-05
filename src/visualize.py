import matplotlib.pyplot as plt
import seaborn as sns

from src.calculate import Results


def win_score(results: Results) -> None:
    """
    Generates Win Score bar plot
    """

    plt.figure(0)
    plt.title('Win Score by Nation')
    plt.ylabel('Simulations')
    x = [n.name for n in results.win_score.index]
    y = results.win_score.values
    plot = sns.barplot(x=x, y=y, errwidth=0).get_figure()
    plot.savefig('img/winscore.png')


def nation_loss(results: Results) -> None:

    attacker_name = results.attacker.name
    defender_name = results.defender.name

    attacker_losses = results.army_cost.loc[attacker_name].T
    defender_losses = results.army_cost.loc[defender_name].T

    plt.figure(1)
    fig1, (ax1, ax2) = plt.subplots(2, 1)  # type: ignore

    fig1.suptitle(attacker_name)
    sns.histplot(data=attacker_losses, x='gold', ax=ax1)
    sns.histplot(data=attacker_losses, x='resources', ax=ax2)
    plt.savefig('img/attacker_losses.png')

    plt.figure(2)
    fig2, (ax3, ax4) = plt.subplots(2, 1)  # type: ignore

    fig2.suptitle(defender_name)
    sns.histplot(data=defender_losses, x='gold', ax=ax3)
    sns.histplot(data=defender_losses, x='resources', ax=ax4)
    plt.savefig('img/defender_losses.png')


def army_roi(results: Results) -> None:
    """
    Generates the Army ROI distribution plots
    :return:
    """

    army_cost = results.army_cost

    attacker_name = results.attacker.name
    defender_name = results.defender.name

    attacker_losses = army_cost.loc[attacker_name, 'gold']
    defender_losses = army_cost.loc[defender_name, 'gold']

    attacker_roi = -1 * (defender_losses - attacker_losses)  # type: ignore
    defender_roi = -1 * (attacker_losses - defender_losses)  # type: ignore

    plt.figure(3)
    fig, (ax1, ax2) = plt.subplots(2, 1)  # type: ignore

    fig.suptitle('Gold ROI by Nation')

    ax1.set_xlabel(attacker_name)
    ax1.set_ylabel('Simulations')
    sns.histplot(data=attacker_roi, ax=ax1)

    ax2.set_xlabel(defender_name)
    ax2.set_ylabel('Simulations')
    sns.histplot(data=defender_roi, ax=ax2)

    plt.savefig('img/nation_roi.png')


def unit_deaths(results: Results) -> None:
    """
    Generates unit losses bar plot
    :return: unit losses bar plot
    """

    unit_losses = results.unit_losses.sort_index()

    attacker_name = results.attacker.name
    defender_name = results.defender.name

    attacker = unit_losses.loc[attacker_name, 'deaths'].T  # type: ignore
    defender = unit_losses.loc[defender_name, 'deaths'].T  # type: ignore

    attacker.columns = [u.name for u in attacker.columns]
    defender.columns = [u.name for u in defender.columns]

    plt.figure(4)
    fig, (ax1, ax2) = plt.subplots(2, 1)  # type: ignore

    fig.suptitle('Unit Deaths by Nation')

    ax1.set_xlabel(f'{attacker_name} units')
    ax1.set_ylabel('Unit Deaths')
    sns.boxplot(data=attacker, ax=ax1)

    ax2.set_xlabel(f'{defender_name} units')
    ax2.set_ylabel('Unit Deaths')
    sns.boxplot(data=defender, ax=ax2)

    plt.savefig('img/unit_losses.png')


def charts(results: Results):
    """
    Visualize battle results
    :return: plot visualizations
    """

    # set visualization palette
    sns.set(palette="Set3",
            style="white",
            rc={
                'figure.figsize': (12.8, 9.6),
                'figure.dpi': 72
            })

    win_score(results)
    nation_loss(results)
    army_roi(results)
    unit_deaths(results)
