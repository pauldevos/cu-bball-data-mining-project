from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os
import math

path = "../clean_data/"

def discretize(df, field, k, init='k-means++'):
    print("Discretizing %s using k-means clustering" % field)
    
    X = pass_df[field].fillna(value=0.0).values.reshape(-1, 1)

    kmeans = KMeans(n_clusters=k, init=init).fit(X)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    disc_data = np.array([])
    for i in range(len(labels)):
        disc_data = np.append(disc_data, centers[labels[i]][0])
    print("Cluster centers for %s:" % field)
    for center in centers:
        print(center[0])
    df['%s_cluster_centroid' % field] = disc_data
    return df

def construct_dataframe():
    
    df = pd.DataFrame()
    files = os.listdir(path)
    for f in files:
        if 'CleanedData' in f:
            print("Grabbing data from %s" % f)
            df = df.append(pd.read_csv("%s%s" % (path, f)))
    return df

if __name__ == '__main__':
    pass_df = construct_dataframe()
    pass_df = discretize(pass_df, "HullArea", 2)
    pass_df = discretize(pass_df, "PassDist", 2)
    pass_df = discretize(pass_df, "ShotClock", 2)
    pass_df.to_csv('CleanedData_AllPasses_discretized.csv', index=False)
