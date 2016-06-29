Model Descriptions
------------------


## Heuristic Model

The first model developed is referred to as the
*heuristic model* and was derived by observing that there were
correlations between fishing behaviour and several of the
values present in AIS messages. In particular, the
likelihood that a vessel was fishing tends to increase with
the standard deviation of the speed ($\sigma_s$) and course
($\sigma_c$), but to decrease with mean speed. These features
were used to develop the *heursitic model*:
$$
fishing\_score = \frac{2}{3}\left(\sigma_{s_m} + \sigma_{c_m} + \overline{s_m}\right) \\
s_m = 1.0 - \min\left(1, speed\,/\,17\right) \\
c_m = course\,/\,360 \\
$$
where the means and standard deviations are computed over a one hour window.

The heuristic model performs reasonably well trawlers and
longliners, but poorly for purse seiners.

ADD TAG/REVISION INFO TO SEE SPECIFIC CODE.


## Generic Model

A series of logistic regression models were then developed
using the same three features found in the *heursitic
model*. In order to increase the expressiveness of the
logistic model, powers of the 3 base features are added to
the features. Thus, the full feature vector consits of:
$$
\sigma_{s_m}, \sigma_{s_m}^2,\ldots, \sigma_{s_m}^n, \sigma_{c_m}, \sigma_{c_m}^2,\ldots, \sigma_{c_m}^n,
\overline{s_m},\overline{s_m}^2, \ldots \overline{s_m}^n \\
$$
where $n$ is what we shall be refer to as the *feature order*.
Note that that despite the odd form of
$s_m$, from the point of view of the
logistic model, it's equivalent to the the speed
capped at 17 knots.

The first of the logistic models, referred to as the
*generic model*, is the model currently in use and
is a logistic model using a 12 hour time window
a feature order of 6. One model is trained for all gear
types. This model generally performs bettter than the
heuristic model, but still performs rather poorly on purse
seiners. The 12-hour window was arrived at by plotting the model
accuracy versus window size. There is a different optimal
window size for each gear type, but 12 hours performed
well for a model trained and tested on all gear types.

ADD TAG/REVISION INFO TO SEE SPECIFIC CODE.

## Multi-Window Model

The multi-window model, which is on the verge of being deployed,
is a logistic model similar to the *generic model* except that
is use uses
multiple time windows, ranging in duration from one-half to
twenty four hours. Using multiple window sizes both provides
a richer feature set and avoids the needs to optimize over
window size. In
addition separate models are trained for each of the three
primary gear types: longliners, trawlers and purse seines.
We are also experimenting with adding other features.
In particular, whether it is currently daylight appears to
be a very useful feature for predicting purse seine fishing.
These changes, taken together, dramatically improve the
performance, particularly of purse seiners.


## Future Models

It is straightforward to use the multi-window logistic
model features described above with a random forest or neural net
model. In early experiments, both of these model types offer
slightly improved performance relative to logistic model while at
the same eliminating the need to augment the feature vector
with powers of the base features.

We eventually plan to experiment with using convolutional or
recurrent neural networks to find features in the AIS data
directly rather than hand engineering the features.


General Notes
-------------

The precision of the models vary by gear type: Long liners are easiest to
predict, even for a model trained on all gear types,
followed by trawlers; purse seiners are the worst.

We have evaluated the models using a separate test set (and
for window size and feature order, optimization, using
separate train-, validation- and test-sets) plotting
precision/recall and ROC curves.

We have also evaluated the generic model on each gear type
separately as well as on the combined data set. In addition,
for longliners we have cross trained and validated between
two separately labelled datasets with slightly different
labeling methods (Kristinas' and Alex data).

