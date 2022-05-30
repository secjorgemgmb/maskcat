import matplotlib.pyplot as plt
from numpy import int64
import pandas as pd

plt.close("all")

inter = 10
folder = "..\\experiments\\maskcat_loop50-200"
main_df = pd.DataFrame()

for i in range (0, 10):
    df = pd.read_csv("{}\\generations\\maskcat_generaciones_rep{}.csv".format(folder, i), delimiter=";").drop("SolutionArray", axis = 1)
    serie = pd.Series(df["BestFitness"])
    main_df["Rep {}".format(i+1)] = serie


interval = [a for a in range (0, len(df)+inter, inter)]
ax = main_df.plot(xticks=interval)
# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)

plt.savefig("{}\\lines.png".format(folder, i), format="png", dpi=1200)

