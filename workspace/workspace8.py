# Titanic survival prediction following video (Kaggle competition)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

titanic_data = pd.read_csv("workspace/train.csv")
print(titanic_data.head())

# sns.heatmap(titanic_data.corr(), cmap = "YlGnBu")
# plt.show()

## Need to continue