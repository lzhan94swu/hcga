"""plotting functions"""
import os

import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
import seaborn as sns
import shap

import matplotlib.pyplot as plt

# matplotlib.use("agg")




def shap_plots(X,shap_values, folder, filename):  
    # plot summary
    custom_bar_ranking_plot(shap_values, X, folder, filename, max_feats=10)  
    
    custom_dot_summary_plot(shap_values, X, folder, filename, max_feats=10)
    #custom_violin_summary_plot(shap_values, X, max_feats=10)
    
    
#    
#    # plot dependence plot for highest ranking feature
#    feature_order = np.argsort(np.sum(np.mean(np.abs(shap_values), axis=0), axis=0))    
#    shap.dependence_plot(X.columns[feature_order[-1]], shap_values[0], X)
#    
#    # plotting for random observation
#    observation = np.random.randint(X.shape[0])
#    shap.force_plot(explainer.expected_value, rf_shap_values[10,:], X_test.iloc[10,:])
#    
    
           

def custom_bar_ranking_plot(shap_vals, data, folder, filename, max_feats):

    '''
    Function for customizing and saving SHAP summary bar plot. 

    Arguments:
    shap_vals = SHAP values list generated from explainer
    data      = data to explain
    max_feats = number of features to display

    '''
    plt.rcParams.update({'font.size': 14})
    shap.summary_plot(shap_vals, data, plot_type="bar", max_display=max_feats, show=False)
    fig = plt.gcf()
    fig.set_figheight(20)
    fig.set_figwidth(15)
    #ax = plt.gca()
    plt.tight_layout()
    plt.title(f'Feature Rankings-All Classes')
    os.path.join(folder, filename + "_shap_bar_rank.png")
    plt.savefig(os.path.join(folder, filename + "_shap_bar_rank.png"),dpi=200)

    
    

def custom_dot_summary_plot(shap_vals, data, folder, filename, max_feats):
    '''
    Function for customizing and saving SHAP summary dot plot. 

    Arguments:
    shap_vals = SHAP values list generated from explainer
    data      = data to explain
    max_feats = number of features to display

    '''
    num_classes = len(shap_vals)
    for i in range(num_classes):
        plt.figure()
        print(f'Sample Expanded Feature Summary for Class {i}')
        plt.rcParams.update({'font.size': 14})
        shap.summary_plot(shap_vals[i], data, plot_type='dot',max_display=max_feats,show=False)
        fig = plt.gcf()
        fig.set_figheight(20)
        fig.set_figwidth(15)
        #ax = plt.gca()
        plt.tight_layout()
        plt.title(f'Sample Expanded Feature Summary for Class {i}')
        #plt.savefig(f"Sample_Expanded_Feature_Summary_Plot_Class_{i}_{dataname}.png")
        plt.savefig(os.path.join(folder, filename + "_shap_class_{}_summary.png".format(i)),dpi=200)


def custom_violin_summary_plot(shap_vals, data, max_feats):
    '''
    Function for customizing and saving SHAP violin plot. 

    Arguments:
    shap_vals = SHAP values list generated from explainer
    data      = data to explain
    max_feats = number of features to display
    '''
    num_classes = len(shap_vals)
    for i in range(num_classes):
        print(f'Violin Feature Summary for Class {i}')
        plt.rcParams.update({'font.size': 14})
        shap.summary_plot(shap_vals[i], data, plot_type="violin",max_display=max_feats,show=False)
        fig = plt.gcf()
        fig.set_figheight(20)
        fig.set_figwidth(15)
        #ax = plt.gca()
        plt.tight_layout()
        dataname=[ k for k,v in globals().items() if v is data][0]
        plt.title(f'Violin Feature Summary for Class {i}-{dataname}')
        #plt.savefig(f"Vioin_Feature_Summary_Plot_Class_{i}_{dataname}.png")
        plt.show()







def basic_plots(X, top_features, folder="."):
    """main function to plot sklearn analysis"""
    # TODO: add other functions, with argument in this one to select what to plot

    plot_feature_importance(X, top_features, folder=folder)
    #plot_dendrogram_top_features(X, top_features, folder=folder)
    # ...


def plot_feature_importance(X, top_features, folder=".", ext=".svg"):
    """plot the feature importances from sklearn computation"""

    mean_features = np.mean(np.array(top_features), axis=0)
    rank_features = np.argsort(mean_features)[::-1]

    plt.figure()
    plt.bar(np.arange(0, len(X.columns)), mean_features[rank_features])
    plt.xticks(
        np.arange(0, len(X.columns)),
        [X.columns.values.tolist()[i] for i in rank_features],
        rotation="vertical",
    )
    plt.savefig(
        os.path.join(folder, "feature_importance_sklern" + ext), bbox_inches="tight"
    )
    plt.show()


def plot_dendogram_top_features(
    X, top_features, top_feat_indices, image_folder, top_N=40
):
    df_topN = pd.DataFrame(
        columns=top_features_list[:top_N], data=X[:, top_feat_indices[:top_N]]
    )
    cor = np.abs(df_topN.corr())
    Z = linkage(cor, "ward")

    plt.figure()
    dn = dendrogram(Z)
    plt.savefig(
        image_folder + "/dendogram_top{}_features.svg".format(top_N), bbox_inches="tight"
    )


def plot_heatmap_top_features():
    new_index = [int(i) for i in dn["ivl"]]
    top_feats_names = [top_features_list[i] for i in new_index]
    df = df_top40[top_feats_names]
    cor2 = np.abs(df.corr())
    plt.figure()
    sns.heatmap(cor2, linewidth=0.5)
    plt.savefig(
        image_folder + "/heatmap_top40_feature_dependencies.svg", bbox_inches="tight"
    )


def plot_top_features(X, top_feats, feature_names, image_folder, threshold=0.9):
    """
    Plot the dendogram, heatmap and importance distribution of top features
    """

    mean_importance = np.mean(np.asarray(top_feats), 0)
    sorted_mean_importance = np.sort(mean_importance)[::-1]

    top_feat_indices = np.argsort(mean_importance)[::-1]
    top_features_list = []
    for i in range(len(top_feat_indices)):
        top_features_list.append(feature_names[top_feat_indices[i]])

    top_features_list = list(dict.fromkeys(top_features_list))

    df_top40 = pd.DataFrame(
        columns=top_features_list[:40], data=X[:, top_feat_indices[:40]]
    )
    cor = np.abs(df_top40.corr())
    Z = linkage(cor, "ward")

    plt.figure()
    dn = dendrogram(Z)
    plt.savefig(image_folder + "/endogram_top40_features.svg", bbox_inches="tight")

    new_index = [int(i) for i in dn["ivl"]]
    top_feats_names = [top_features_list[i] for i in new_index]
    df = df_top40[top_feats_names]
    cor2 = np.abs(df.corr())
    plt.figure()
    sns.heatmap(cor2, linewidth=0.5)
    plt.savefig(
        image_folder + "/heatmap_top40_feature_dependencies.svg", bbox_inches="tight"
    )

    # Taking only features till we have reached 90% importance
    sum_importance = 0
    final_index = 0
    for i in range(len(sorted_mean_importance)):
        sum_importance = sum_importance + sorted_mean_importance[i]
        if sum_importance > threshold:
            final_index = i
            break
    if final_index < 3:  # take top 2 if no features are selected
        final_index = 3

    plt.figure()
    plt.plot(np.sort(mean_importance)[::-1])

    plt.xlabel("Features")
    plt.ylabel("Feature Importance")
    plt.xscale("log")
    plt.yscale("symlog", nonposy="clip", linthreshy=0.001)
    plt.axvline(x=final_index, color="r")
    plt.savefig(
        image_folder + "/feature_importance_distribution.svg", bbox_inches="tight"
    )

    # import pickle as pkl
    # pkl.dump(np.sort(mean_importance)[::-1], open('importance_data/'+image_folder+'.pkl','wb'), pkl.HIGHEST_PROTOCOL)


def top_features_importance_plot(
    g, X, top_feat_indices, feature_names, y, name="xgboost", image_folder="images"
):
    """ 
    Plot the top feature importances
    """

    import matplotlib.cm as cm
    import random

    # mean_importance = np.mean(np.asarray(top_feats),0)
    # top_feat_indices = np.argsort(mean_importance)[::-1]
    plt.figure()
    cm = cm.get_cmap("RdYlBu")
    sc = plt.scatter(X[:, top_feat_indices[0]], X[:, top_feat_indices[1]], cmap=cm, c=y)
    plt.xlabel(feature_names[top_feat_indices[0]])
    plt.ylabel(feature_names[top_feat_indices[1]])
    plt.colorbar(sc)
    plt.savefig(
        image_folder + "/scatter_top2_feats_" + g.dataset + "_" + name + ".svg",
        bbox_inches="tight",
    )


def plot_violin_feature(
    g, X, y, feature_id, feature_names, name="xgboost", image_folder="images"
):
    """
    Plot the violins of a feature
    """

    import random

    feature_data = X[:, feature_id]

    data_split = []
    for k in np.unique(y):
        indices = np.argwhere(y == k)
        data_split.append(feature_data[indices])

    import seaborn as sns

    plt.figure()
    sns.set(style="whitegrid")
    ax = sns.violinplot(data=data_split, palette="muted", width=1)
    ax.set(xlabel="Class label", ylabel=feature_names[feature_id])
    plt.savefig(
        image_folder
        + "/violin_plot_"
        + g.dataset
        + "_"
        + str(feature_names[feature_id])
        + "_"
        + name
        + ".svg",
        bbox_inches="tight",
    )
