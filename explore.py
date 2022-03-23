import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_categorical_and_continuous_vars(df, continuous_features, categorical_features):
    for cat in categorical_var:
        for con in continuous_var:
            fig, ax = plt.subplots(ncols=3, sharey=True, sharex=True, figsize=(14,8))
            sns.boxplot(x=cat, y= con, data=train, ax=ax[0])
            sns.swarmplot(x=cat, y= con, data=train, ax=ax[0], zorder=0)
            sns.stripplot(x=cat, y= con, data=train, ax=ax[1])
            sns.barplot(x=cat, y=con, data=train, ax=ax[2])
            plt.show()