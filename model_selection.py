from db_handler.db_handler import DatabaseHandler
from utils.catalog_utils import setup_cache_temp_folder
from config.paths import graphs_path
import pandas as pd
import os
import numpy as np
import itertools
import matplotlib.pyplot as plt
from statistics import mean
import seaborn as sns
from numpy import set_printoptions
from sklearn.metrics import mean_squared_error, r2_score, f1_score, precision_score, recall_score, confusion_matrix
from sklearn.metrics import roc_curve, classification_report, auc
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.impute import SimpleImputer
from sklearn import preprocessing
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import neighbors
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)
pd.options.display.width = 0
pd.set_option('display.max_rows', None)


def plot_roc_and_confusion_matrix(y_test, predicted, pred_proba, iteration=None, model_name=None, save_dir=None):
    matrix = confusion_matrix(y_test, predicted)
    # gather area under the curve
    fpr, tpr, _ = roc_curve(y_test, pred_proba[:, 1], 1)
    roc_auc = auc(fpr, tpr)
    # create the subplot for area under the curve
    fig, axs = plt.subplots(2, 2, figsize=(10, 5))
    fig.suptitle('ROC curve for fold {}'.format(iteration), fontsize=16)
    plt.subplot(1, 2, 1)
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Song - Video Matches - %03s ROC' % (model_name))
    plt.legend(loc="lower right")
    # create the subplot for confusion matrix
    plt.subplot(1, 2, 2)
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix, %03s' % (model_name))
    plt.colorbar()
    tick_marks = np.arange(len([0, 1]))
    plt.xticks(tick_marks, [0, 1], rotation=45)
    plt.yticks(tick_marks, [0, 1])
    fmt = 'd'
    thresh = matrix.max() / 2.
    for i, j in itertools.product(range(matrix.shape[0]), range(matrix.shape[1])):
        plt.text(j, i, format(matrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if matrix[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    fig.subplots_adjust(top=0.88)
    if save_dir:
        try:
            plt.savefig(save_dir + "roc_" + str(model_name) + "_" + str(iteration) + ".png")
        except FileNotFoundError:
            oldmask = os.umask(000)
            os.makedirs(save_dir, exist_ok=True, mode=0o755)
            os.umask(oldmask)
            plt.savefig(save_dir + "roc_" + str(model_name) + "_" + str(iteration) + ".png")
    else:
        plt.show()

if __name__ == '__main__':
    db = DatabaseHandler('file_system_catalogs')
    db_connection = db.connection
    feat_tables = ['audio_features', 'video_features', 'symbolic_features']
    for table in feat_tables:
        if not db.check_for_existing_tables(table=table):
            raise BaseException("The {} table is missing. Run extract_features.py".format(table))

    with open('db_handler/sql/collect_features_for_model.sql') as q_file:
        sql = q_file.read()
        data = pd.read_sql(sql=sql, con=db_connection, index_col='id')

    data = data.drop(labels=['audio_id', 'clip_id', 'midi_id'], axis=1)

    data.describe().T.to_csv('./var/dataset_description.csv')

    total_instances = data.y.count()
    match = data.y.sum()
    fake = data.y.count() - match
    print('Total data points: ' + str(total_instances) +
          '\nNumber of matches: ' + str(match) +
          '\nNumber of fakes: ' + str(fake))
    empty_cols = [col for col in data.columns if (data[col] == 0).all()]
    print('The number of columns with only zero values is: {}'.format(str(len(empty_cols))))
    print('These are:')
    for col in empty_cols:
        print(col)
    print("We remove those from the dataset")
    data = data.drop(empty_cols, axis=1)

    cols_with_nas = [col for col in data.columns if len(data[data[col].isna()])>0.4*len(data)]
    if len(cols_with_nas) == 0:
        print("There are no columns with more than 40% empty values")
    else:
        print("We have removed the following columns because they were more than 40% empty:")
        for col in cols_with_nas:
            print(col)
        data = data.drop(empty_cols, axis=1)
    #
    # df = data.melt(id_vars=['y'])
    # cols = data.columns
    # grid = sns.axisgrid.FacetGrid(df[df.variable.isin(cols)], col='variable', sharey=False, col_wrap=5)
    # grid.map(sns.boxplot, 'tumor_type', 'value')

    X = data.drop(['y', 'video_id'], axis=1)
    groups = data['video_id']
    y = data.y

    print('The maximum value in the dataframe is: ' + str(X.max().max()))
    print('The minimum value in the dataframe is: ' + str(X.min().min()))
    print('The mean value in the dataframe is: ' + str(round(X.mean().mean(), 3)))

    corr = X.corr(method='pearson')
    corr_a = corr.abs()
    s = corr_a.unstack().sort_values(kind="quicksort")
    pairs = set(s[s > 0.7].index)
    clean_pairs = set([tuple(sorted(i)) for i in pairs if i[0] != i[1]])
    print('There are ' + str(len(clean_pairs)) + ' pairs with at least 80% correlation.')
    print('The top 15 are:')
    for pair in sorted(clean_pairs)[0:15]:
        print(pair)

    singles = []
    drops = []

    # only keep one for each pair of highly correlated features.
    for pair in sorted(clean_pairs):
        if pair[1] not in drops:
            drops.append(pair[1])
        if pair[0] not in drops and pair[0] not in singles:
            singles.append(pair[0])
    data = data[singles]

    imp = SimpleImputer(missing_values=np.NaN, strategy='mean')
    min_max_scaler = preprocessing.MinMaxScaler()
    logo = LeaveOneGroupOut()
    logo.get_n_splits(X, y, groups)

    # we choose a common seed for all algorithms
    seed = 2015
    # we choose a common number of trees for ensembles
    num_trees = 800

    models = [('Decision Tree', DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=seed)),
              ('Logistic Regression', LogisticRegression(random_state=seed, solver='liblinear')),
              ('kNN', neighbors.KNeighborsClassifier(n_neighbors=3, weights='uniform', n_jobs=-1)),
              ('SVM', svm.SVC(kernel='poly', C=1, gamma='auto', cache_size=12288, probability=True)),
              ('Random Forest',RandomForestClassifier(n_estimators=num_trees,max_depth=1,n_jobs=-1,random_state=seed)),
              ('Bagged Trees', BaggingClassifier(
                  base_estimator=DecisionTreeClassifier(criterion='gini', max_depth=1, random_state=seed),
                  n_estimators=num_trees, random_state=seed, n_jobs=-1)),
              ('AdaBoost', AdaBoostClassifier(
                  base_estimator=DecisionTreeClassifier(criterion='gini', max_depth=1, random_state=seed),
                  n_estimators=num_trees, random_state=seed)),
              ('XGBoost', XGBClassifier(nthread=8, use_label_encoder=False))]

    fold_results = {}
    for name, model in models:
        fold_results[name] = {
            'accuracy': [],
            'precision': [],
            'recall': [],
            'f1': []
        }

    i = 0
    for train_index, test_index in logo.split(X, y, groups):
        # print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]  # %%
        # fit the transformations
        X_train = imp.fit_transform(X_train)
        X_test = imp.transform(X_test)

        X_train = min_max_scaler.fit_transform(X_train)
        X_test = min_max_scaler.transform(X_test)
        for name, model in models:
            # fit the model
            model.fit(X_train, y_train)
            predicted = model.predict(X_test)
            pred_proba = model.predict_proba(X_test)
            # gather metrics
            accuracy = model.score(X_test, y_test)
            precision = precision_score(y_test, predicted)
            recall = recall_score(y_test, predicted)
            f1 = f1_score(y_test, predicted)
            fold_results[name]['accuracy'].append(accuracy)
            fold_results[name]['precision'].append(precision)
            fold_results[name]['recall'].append(recall)
            fold_results[name]['f1'].append(f1)

            print("%03s: Accuracy: %0.2f Precision: %0.2f Recall: %0.2f F_1 score: %0.2f"
                  % (name, accuracy, precision, recall, f1))
            plot_roc_and_confusion_matrix(y_test,
                                          predicted,
                                          pred_proba,
                                          iteration=i,
                                          model_name=name,
                                          save_dir=graphs_path)
        i += 1

    compare = {}

    for model, results in fold_results.items():
        model_stats = {}
        for metric, values in results.items():
            model_stats[metric] = mean(values)
        compare[model] = model_stats

    model_comparison = pd.DataFrame(compare)
    model_comparison.T.to_csv('./var/model_results_drop_corr_800_trees_depth1.csv')
    print('end')
