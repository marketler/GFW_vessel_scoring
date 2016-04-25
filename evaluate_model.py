import matplotlib.pyplot as plt
import utils
import numpy as np
from sklearn import metrics
from IPython.core.display import display, HTML



def train_model(model, train_data):
    """train `model` with `train_data`

    example:

    model = train_model(LogisticModel(window=3600), train_data)


    """
    X_train = model.make_features(train_data)
    y_train = utils.is_fishy(train_data)
    model.fit(X_train, y_train)
    return model


# TODO break this into a plotting and a text part
def evaluate_model(model, test_data, name=None):
    """Plot some graphs and compute some metrics on a model

    model - a trained model
    test_data - data to use on the evalutions

    """
    X = model.make_features(test_data)
    is_fishy = utils.is_fishy(test_data)

    score = model.predict_proba(X)[:,1]
    score_fishy = score[is_fishy]
    score_nonfishy =  score[~is_fishy]

    precisions, recalls, thresholds = metrics.precision_recall_curve(is_fishy, score)


    model_description = str(model) if (name is None) else name
    display(HTML("<h1>%s</h1>" % model_description))


    ylim = 10.0

    f, (a1, a2) = plt.subplots(1, 2, figsize=(20,5))

    a1_precall = a1.twinx()
    def convert_range(ax_f):
        y1, y2 = ax_f.get_ylim()
        a1_precall.set_ylim(y1, y2 / ylim)
        a1_precall.figure.canvas.draw()
    a1.callbacks.connect("ylim_changed", convert_range)

    new_score_fishy = a1.hist(score_fishy, bins=200,
            normed=True, color='b', alpha=0.5, label="fishy score")
    new_score_nonfishy = a1.hist(score_nonfishy, bins=200,
            normed=True, color='r', alpha=0.5, label="nonfishy score")

    a1_precall.plot(thresholds, precisions[:-1], color='g', label='Precision')
    a1_precall.plot(thresholds, recalls[:-1], color='b', label='Recall')

    a1.legend()
    a1.set_ylim(0, ylim)
    a1.set_xlim(0, 1)

    a1.set_ylabel('Histogram')
    a1_precall.set_ylabel('Curve')

    fpr, tpr, _ = metrics.roc_curve(is_fishy, score)
    auc = metrics.auc(fpr, tpr)
    a2.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    a2.legend()

    plt.show()

    total = sum(new_score_fishy[0] + new_score_nonfishy[0])
    non_overlap = sum(abs(new_score_fishy[0] - new_score_nonfishy[0]))
    overlap = total - non_overlap
    error = overlap / total

    print "For cutoff of 0.5:"
    predicted = score > 0.5
    print metrics.classification_report(is_fishy, predicted,
                                    target_names=['non-fishing', 'fishing'])
    false_positives = (predicted & ~(is_fishy)).sum() / float(len(is_fishy))
    print "False positive rate:", false_positives



def compare_auc(models, test_data):
    is_fishy = utils.is_fishy(test_data)
    f, a1 = plt.subplots(figsize=(12,12))
    for (name, mdl) in models:
        X = mdl.make_features(test_data)
        score = mdl.predict_proba(X)[:,1]
        fpr, tpr, _ = (metrics.roc_curve(is_fishy, score))
        auc = metrics.auc(fpr, tpr)
        a1.plot(fpr, tpr, label='{0}: {1:.3f} AUC'.format(name, auc))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.show()
