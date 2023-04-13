import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scikit-learn.cluster import KMeans

conv_path = r"c:\users\frank\Documents\DME\Eindopdracht_without_raw\data\Processed"
with open(conv_path + "\E214_A.pkl", "rb") as f:
    df = pickle.load(f)

# g = sns.FacetGrid(df, col="Truck_State")
# g.map(sns.scatterplot, "engine_speed", "EnginePower", alpha=0.7)
# plt.show()

print(np.sum(df.No_State))
print(np.sum(df.working))
print(len(df.engine_speed))


# Load the dataframepoetry add
df = pd.read_csv("data.csv")

# Determine the number of clusters
k = ...

# Extract the signals data from the dataframe
signals_data = df.iloc[:, 0:50].values

# Initialize the k-means object with the number of clusters
kmeans = KMeans(n_clusters=k)

# Fit the k-means object to the signals data
kmeans.fit(signals_data)

# Get the cluster assignments for each data point
labels = kmeans.labels_

# Add the cluster assignments to the original dataframe
df["Cluster"] = labels


