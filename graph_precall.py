from matplotlib.pyplot import *
from numpy import *

def graph_precall(x, col):
    steps = 20

    precall = np.zeros((steps,), dtype=[('precision', 'f8'), ('recall', 'f8')])
    cutoffs = linspace(0, 1, steps)

    for idx, cutoff in enumerate(cutoffs):
        xpos = x[x['classification'] > 0.5]
        positives = float(x[x[col] > cutoff].shape[0])
        true_positives = float(xpos[xpos[col] > cutoff].shape[0])
        true = float(xpos.shape[0])

        if true_positives == 0.0:
            precall['precision'][idx] = Inf
        else:
            precall['precision'][idx] = true_positives / positives
        if true == 0.0:
            precall['recall'][idx] = Inf
        else:
            precall['recall'][idx] = true_positives / true
        

    histfig = figure(figsize=(20,5))
    subplot = histfig.add_subplot(121)

    subplot.plot(precall['recall'], precall['precision'])
    xlabel("recall")
    ylabel("precision")

    subplot = histfig.add_subplot(122)
    subplot.plot(cutoffs, precall['precision'], label="precision")
    subplot.plot(cutoffs, precall['recall'], label="recall")
    legend()
    xlabel("cutoff")
    show()
