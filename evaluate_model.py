import matplotlib.pyplot as plt
import utils
import numpy as np
from sklearn import metrics



def train_model(model, train_data, **feature_args):
    X_train = model.make_features(train_data, **feature_args)
    y_train = utils.is_fishy(train_data)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, test_data, y_lim=10, **feature_args):

    X = model.make_features(test_data, **feature_args)
    is_fishy = utils.is_fishy(test_data)

    f, (a1, a2) = plt.subplots(1, 2, figsize=(20,5))

    score = model.predict_proba(X)[:,1]
    score_fishy = score[is_fishy]
    score_nonfishy =  score[~is_fishy]

    new_score_fishy = a1.hist(score_fishy, bins=200,
            normed=True, color='b', alpha=0.5, label="fishy score")
    new_score_nonfishy = a1.hist(score_nonfishy, bins=200,
            normed=True, color='r', alpha=0.5, label="nonfishy score")
    a1.legend()
    a1.set_ylim(0, y_lim)
    a1.set_xlim(0, 1)

    fpr, tpr, _ = metrics.roc_curve(is_fishy, score)
    auc = metrics.auc(fpr, tpr)
    a2.plot(fpr, tpr, label='ROC curve (area = %0.2f)')

    plt.show()

    total = sum(new_score_fishy[0] + new_score_nonfishy[0])
    non_overlap = sum(abs(new_score_fishy[0] - new_score_nonfishy[0]))
    overlap = total - non_overlap
    error = overlap / total

    print model
    print
    print "AUC:", auc
    print "For cutoff of 0.5:"
    predicted = score > 0.5
    print metrics.classification_report(is_fishy, predicted,
                                    target_names=['non-fishing', 'fishing'])
    false_positives = (predicted & ~(is_fishy)).sum() / float(len(is_fishy))
    print "False positive rate:", false_positives



def compare_auc(models, test_data):
    is_fishy = utils.is_fishy(test_data)
    f, a1 = plt.subplots(figsize=(12,12))
    for (name, mdl, kwargs) in models:
        X = mdl.make_features(test_data, **kwargs)
        score = mdl.predict_proba(X)[:,1]
        fpr, tpr, _ = (metrics.roc_curve(is_fishy, score))
        auc = metrics.auc(fpr, tpr)
        a1.plot(fpr, tpr, label='{0}: {1:.2f} AUC'.format(name, auc))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.show()
