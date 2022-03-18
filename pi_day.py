from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kstest, uniform

# data collected on pi day 2022, March 14th
# 29 people participated

x_list = [
    14, 12, 17, 5, 56, 39, 21, 67,
    4, 42, 6, 7, 47, 13, 14, 73,
    51, 57, 76, 1, 4, 8, 13, 19,
    77, 17, 98, 33, 9, 60, 50, 10,
    52, 12, 44, 37, 32, 4, 75, 3,
    6, 6, 10, 68, 0, 4, 20, 11,
    40, 33, 67, 2, 4, 0, 86, 61,
    17, 19, 75, 47, 44, 38, 22, 64,
    31, 96, 87, 49, 57, 17, 1, 3,
    75, 7, 18,
]

y_list = [
    77, 13, 5, 99, 2, 7, 31, 87,
    4, 64, 66, 38, 72, 29, 3, 37,
    52, 33, 53, 7, 86, 3, 1, 91,
    87, 12, 13, 82, 4, 18, 64, 92,
    13, 85, 89, 21, 95, 98, 3, 21,
    66, 90, 10, 99, 1, 21, 2, 22,
    4, 44, 2, 78, 84, 100, 6, 23,
    89, 8, 22, 33, 75, 33, 56, 65,
    9, 71, 82, 15, 21, 13, 69, 1,
    7, 42, 72,
]


def test_uniformity(datasets):
    """ tests if the passed-in datasets are uniformly distributed between 0 and 100, 
    with a Kolmogorov-Smirnov statistical test """
    print(f"{'KS Stat':^12} {'pvalue':^12} {'Uniform?':^8}")
    for ds in datasets:
        ksstat, pvalue = kstest(ds, uniform(loc=0.0, scale=100.0).cdf)
        uni = "YES" if pvalue > 0.05 else "NO"
        print(f"{ksstat:12.3f} {pvalue:12.8f} {uni:^8}")


def process_xs_and_ys(
    x_list, y_list, experiment_name, explain_text, title_pi_hat, title_dart,
    xlabel_pi_hat, ylabel_pi_hat, xlabel_dart, ylabel_dart,
):
    """ based on a list of (x,y) coordinates, iteratively compute estimates of pi, 
    make graphs and write them to files at each step """
    pi_hat_list = []
    inside_x_list = []
    inside_y_list = []
    nb_inside_disk_list = []
    outside_x_list = []
    outside_y_list = []
    nb_outside_disk_list = []

    nb_samples = len(x_list)
    nb_inside_disk = 0
    for i in range(nb_samples):
        is_inside = (x_list[i] ** 2 + y_list[i] ** 2) < 10000
        if is_inside:
            nb_inside_disk += 1
            inside_x_list.append(x_list[i])
            inside_y_list.append(y_list[i])
        else:
            outside_x_list.append(x_list[i])
            outside_y_list.append(y_list[i])

        nb_inside_disk_list.append(nb_inside_disk)
        nb_outside_disk_list.append(i - nb_inside_disk)

        nb_inside_square = (i + 1)
        pi_hat = nb_inside_disk * 4 / nb_inside_square
        pi_hat_list.append(pi_hat)

    print(f"{pi_hat_list[-1]:.3f}")

    plt.style.use("seaborn-whitegrid")

    for idx in range(nb_samples):

        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        axs[0].plot(
            inside_x_list[0: nb_inside_disk_list[idx] + 1],
            inside_y_list[0: nb_inside_disk_list[idx] + 1],
            "D", markerfacecolor="none", color="#47c6a9",
        )
        axs[0].plot(
            outside_x_list[0: nb_outside_disk_list[idx] + 1],
            outside_y_list[0: nb_outside_disk_list[idx] + 1],
            "D", color="#47c6a9",
        )
        dashed_circle = plt.Circle((0, 0), 100, color="black", linestyle='dashed', linewidth=1, fill=False)
        axs[0].add_patch(dashed_circle)
        axs[0].set_aspect("equal")
        axs[0].set_title(title_dart)
        axs[0].set_xlabel(xlabel_dart)
        axs[0].set_ylabel(ylabel_dart)
        axs[0].set_xlim(0, 100)
        axs[0].set_ylim(0, 100)

        axs[1].plot(range(idx + 1), pi_hat_list[0: idx + 1], color="#47c6a9")
        axs[1].plot(range(nb_samples), np.full(
            nb_samples, np.pi), color="black", linestyle='dashed', linewidth=1)
        axs[1].set_xlim(0, nb_samples)
        axs[1].set_ylim(2.5, 4.1)
        axs[1].set_title(title_pi_hat)
        axs[1].set_xlabel(xlabel_pi_hat)
        axs[1].set_ylabel(ylabel_pi_hat)

        full_explain_text = (
            explain_text
            + "\n"
            + r"$\widehat{\mathrm{\pi}} \rightarrow "
            + f"{pi_hat_list[idx]:.3f}"
            + r"$"
        )

        axs[1].text(0.6, 0.15, full_explain_text, transform=fig.transFigure)
        fig.tight_layout()
        plt.savefig(f"out_tmp/{experiment_name}_{idx:05d}.png")
        if idx == (nb_samples - 1):
            plt.savefig(experiment_name + ".png")
        plt.close()


def plot_howto(file_name):
    """ simple graph to explain the principle of pi estimation """
    plt.clf()
    fig = plt.figure(figsize=(6, 6))
    ax = plt.axes()

    disk = plt.Circle((0, 0), 100, color='#47c6a9')
    dashed_circle = plt.Circle((0, 0), 100, color="black", linestyle='dashed', linewidth=1, fill=False)

    ax.add_patch(disk)
    ax.add_patch(dashed_circle)

    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.title(r"How to estimate $\mathrm{\pi}$")
    explain_text = r"""
    
    Area of the quarter disk: $A_d = (\mathrm{\pi} \times r^2)/4$
    Area of the square: $A_s = r^2$
    A point $(x, y)$ drawn randomly is inside the disk
    with probability $A_d/A_s$

    $\mathrm{\pi}$ can thus be approximated by counting:
    how many random points are inside the disk (${n}_{d}$), 
    how many random points are inside the square (${n}_{s}$),
    and computing this:
    
    $\widehat{\mathrm{\pi}} \simeq 4 \times {n}_{d}/{n}_{s}$

    Let's do it!
    """
    ax.text(0.15, 0.18, explain_text, transform=fig.transFigure)
    ax.set_aspect("equal")
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    plt.xlabel(r"$r$")
    plt.ylabel(r"$r$")
    plt.savefig(file_name)


###
###

# general explanation
plot_howto("0_how_to_estimate_pi.png")

# Experiment 1:
# Use raw data
test_uniformity([x_list, y_list])

process_xs_and_ys(
    x_list,
    y_list,
    experiment_name="1_raw_75",
    explain_text=r"""Collectively we are not random (at least not uniform),
as confirmed by a statistical test.
$75$ points do not get us very close to $\mathrm{\pi}$.""",
    title_pi_hat=r"Collective estimation of $\mathrm{\pi}$ - Raw data",
    title_dart='"Random" points inside or outside a disk',
    xlabel_pi_hat="Time",
    ylabel_pi_hat=r"Estimation of $\mathrm{\pi}$ - Raw data",
    xlabel_dart="X",
    ylabel_dart="Y",
)

# Experiment 2:
# bootstrap = use axial symmetries to add more samples
# x,y -> 100-x,y
# x,y -> 100-x,100-y
# x,y -> x,100-y

N = len(x_list)
hundreds = np.full(N, 100)
h_minus_x = np.subtract(hundreds, x_list)
h_minus_y = np.subtract(hundreds, y_list)

aug_x_list = np.append(x_list, [h_minus_x, x_list, h_minus_x])
aug_y_list = np.append(y_list, [h_minus_y, h_minus_y, y_list])

test_uniformity([aug_x_list, aug_y_list])

process_xs_and_ys(
    aug_x_list,
    aug_y_list,
    experiment_name="2_augmented_300",
    explain_text=r"""Even with augmented data (using axial symmetries), 
we are still not uniformly random,
as confirmed by a statistical test.
But we get a bit closer to $\mathrm{\pi}$.""",
    title_pi_hat=r"Collective estimation of $\mathrm{\pi}$ - Augmented data",
    title_dart='"Random" points inside or outside a disk - Augmented data',
    xlabel_pi_hat="Time",
    ylabel_pi_hat=r"Estimation of $\mathrm{\pi}$ - Augmented data",
    xlabel_dart="X",
    ylabel_dart="Y",
)

# Experiment 3:
# use the decimals of Pi as a random number generator - 300 points

# Here is an API to get decimals of pi, thank you Weibing.
# https://uploadbeta.com/api/pi/?cached&n=1200
# import requests
# from textwrap import wrap
# num_pairs = 100
# li = [int(i) for i in wrap(requests.get(f"https://uploadbeta.com/api/pi/?cached&n={num_pairs*4}").text[1:-1], 2)]
# print(list(zip(li[::2], li[1::2])))

pi_300_pairs = "0314159265358979323846264338327950288419716939937510582097494459\
    2307816406286208998628034825342117067982148086513282306647093844609550582231\
    7253594081284811174502841027019385211055596446229489549303819644288109756659\
    3344612847564823378678316527120190914564856692346034861045432664821339360726\
    0249141273724587006606315588174881520920962829254091715364367892590360011330\
    5305488204665213841469519415116094330572703657595919530921861173819326117931\
    0511854807446237996274956735188575272489122793818301194912983367336244065664\
    3086021394946395224737190702179860943702770539217176293176752384674818467669\
    4051320005681271452635608277857713427577896091736371787214684409012249534301\
    4654958537105079227968925892354201995611212902196086403441815981362977477130\
    9960518707211349999998372978049951059731732816096318595024459455346908302642\
    5223082533446850352619311881710100031378387528865875332083814206171776691473\
    0359825349042875546873115956286388235378759375195778185778053217122680661300\
    1927876611195909216420198938095257201065485863278865936153381827968230301952\
    0353018529689957736225994138912497217752834791315155748572424541506959508295\
    331168617278558890750983817546374649393192550604009277016711390098488240"

li = [int(i) for i in wrap(pi_300_pairs, 2)]

pi_x_list = list(li[::2])
pi_y_list = list(li[1::2])

test_uniformity([pi_x_list, pi_y_list])

process_xs_and_ys(
    pi_x_list,
    pi_y_list,
    experiment_name="3_pi_300",
    explain_text=r"""With a proper random number generator
(inspired by the decimals of $\mathrm{\pi}$),
$300$ iterations get even closer to $\mathrm{\pi}$.""",
    title_pi_hat=r"Estimation of $\mathrm{\pi}$ with proper random numbers",
    title_dart="Random points inside or outside a disk",
    xlabel_pi_hat="Time",
    ylabel_pi_hat=r"Estimation of $\mathrm{\pi}$",
    xlabel_dart="X",
    ylabel_dart="Y",
)

# Use these commands to create animated gifs!
# convert -delay 10 -loop 1 out_tmp/1_* 1_raw_75_anim.gif &
# convert -delay 4 -loop 1 out_tmp/2_* 2_augmented_300_anim.gif &
# convert -delay 4 -loop 1 out_tmp/3_* 3_pi_300_anim.gif &
