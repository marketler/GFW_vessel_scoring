# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v2.0.0 - 2020-03-13

### Added

* [GlobalFishingWatch/gfw-eng-tasks#34](https://github.com/GlobalFishingWatch/gfw-eng-tasks/issues/34): Adds
    support for python 3.


## 1.1 - 2019-05-10

  - Bump version to 1.1.
  - Pin version of scikit learn to 0.20 since we are still using python 2.7
  - Example vessel scoring
  - give shell friendly name
  - add figure source for document:
  - Update README.md
  - 61 add measures offset
  - Offset zero by default
  - Added PASSWORD option


## multi-model-1.0 - 2016-11-20

  - Bugfix for AddMeasures
  - Support offsets for add_measures (#62)
      *Supportoffsetsforadd_measures
      *Somedocumentation
      *Bugfix
      *debug;add50%offset;checkimprovement
      *makeasclosetopre-shiftedversionaspossiblefortesting
      *centerranges
      *pulloutis_daylightasapredictor
      *usesegmentsindedupping
  - use segments in dedupping
  - pull out is_daylight as a predictor
  - center ranges
  - dedup messages
  - make as close to pre-shifted version as possible for testing
  - debug; add 50% offset; check improvement
  - Bugfix
  - Some documentation
  - Support offsets for add_measures
  - add PDF documentation of ML fishing score
  - More notebook cleanup
  - Moved more code to the modules and made the training use the same system used for production
  - Some notebook cleanup
  - Consolidate Notebooks
  - Edit text of Compare-Models
  - update Compare-Models text
  - remove models not in notebbooks
  - Make text in compare-with-dal more generic and rename to compare-models
  - move Dal Comparison
  - Accuracy vs ais degredation
  - Add model descriptions
  - move and rename model-description notebook
  - fix mispellings
  - fixed typo in AIS notebook
  - create model sensitivity notebook
  - add plots using binned data as comparison
  - Look at vessels with 100-200 PPD
  - add title for improved section
  - Improve fishing hours versus pts_per_day plot
  - add plot fishing hours vs pts-per-day at different max_gaps
  - remove redundant graph
  - combine plots
  - add fishing hours plots for dropped out data as well
  - prettier plots
  - Use fishing hours in point density comparison; compare effect of max gap
  - fix info leak and and add results using non-even training
  - fix notebook bug; add measure_count field to measures
  - add comparison of fishing hours
  - improve database munging (add_features / add_all_features); update notebook
  - rough draft - creation of reduced measures is messy
  - rerun all models
  - create model sensitivity notebook
  - Fix typos; clarify text
  - Bugfix and attribution
  - Added source links and description of the gear type specific models
  - Compare ps with dal
  - Add model comparisons to Model Descriptions notebook
  - add alignment to mulitline eqn in the hopes github renders correctly
  - Move markdown back to notebook
  - initial model descriptions
  - add missing  retry
  - some description of model history
  - Rename notebook to 'Compare with Dal.ipynb'
  - Compare all results, not just PS
  - Add notebook comparing Dalhousie and GFW PS results
  - Switch RF model to use colspec
  - fix to use utcfromtimestamp
  - 11 daylight
  - Updated README with new data location
  - Bugfixed notebooks
  - Got time-of-day stuff to work
  - Bugfixes to day/night
  - First attempt at using daylight
  - Script to predict manually
  - Merge branch 'multi-model' into evaluate-non-model-results
  - Refactor so we can evalutae results from external models

## release-1.0 - 2016-06-18

  - Remove unnecessary dependencies
  - Bugfix for missing dependency
  - Delete Broken model.ipynb
  - Install libatlas-dev first
  - + coveralls
  - + Building at Travis.  We can at least test the install process.
  - + .idea/, venv/, etc.
  - Remove unecessary dependencies and import optional depdencies in functions at runtime.
  - Added a script to anonymize mmsis
  - Multi model stuff
  - API bugfix
  - Bugfixes and new models
  - Add measures port rh
  - Bugfixes and final test
  - Generate all columns
  - Bugfix
  - Track down pipeline problem.
  - Added build files to gitignore
  - fix(?) new add measures
  - Broken model
  - Broken model?
  - Screen out points with speed==None
  - Removed ipython checkpoints from git
  -   * Improve way Kristina's data is fixed
  -   * Add method to turn CSV transit data
  -   * test how model is performing on new transit data and on
  -   previously dumped models.
  - Bugfix
  - Generalized the numpy2message stuff
  - Began converting to new stream based API
  - Ported the rolling measures / add measures code from benthos-pipeline
  - Update README.md
  - Create LICENSE
  - Update README.md
  - Find and change add_measures to fix unscaled data
  - Added trained models to git
  - Merge branch 'installation'
  - Load models again
  - harmonize interface between LogisticModel and LogisticScorer
  - Basic pip install code
  - Basic pip install code
  - Cleanup
  - Bugfixed imports
  - Updated import paths
  - More cleanup
  - Added datasets and virtualenv to gitignore
  - More cleanup
  - Removed old stuff and reorganized the data a bit (classified-filtered.npz -> data/alex)
  - Bugfix
  - Better graphing
  - Rerun some notebook cells with better output
  - Added right-hand-side scale
  -   * Tweak Model interface so that we can use GridSearchCV from sklearn.
  -   * Setup Optimize_model.ipynb to use grid search
  -   * Add bad tracks that Egil created to Compare_single_model.ipynb
  -   * Added LogisticScorer class for possible use with Pipeline
  -   * Incorporated Egil's changes to the evaluate_model.py, plus more.
  - Added precision/recall to graphs
  - Refactor models
  - Slight generalizations to work with new dataset
  - Continue refactoring
  - - Fold make_features options into models instead.
  - - Setup notebooks to loop over models rather than doing by hand
  - - Clean up and add docstrings.
  - Add multi-mindow logistic model
  - Generalized scripts a bit
  - add 12 hour heuristic
  - Modify score_development to use load_dataset_by_vessel
  - Start branch to refactor models to make them easier to compare
  -   * Made sklearn-like models for Logistic, Random Forest and Legacy models
  -   * Wrote preliminary evaluation code.
  -   -> interface needs work
  - 486 Classifier gives fishing score for transits
  - Link to data
  - New scoring of all of Alex and Kristinas data
  - Scoring using Kristinas data
  - Score development bugfixing so it works for purse seiners too
  - Bugfixed parsing of Kristinas data
  - Oups
  - Merge branch 'master' of github.com:GlobalFishingWatch/vessel-scoring
  - Measurs with different windows, classified-filtered with lat/lon
  - Create README.md
  - Scored trawlers too
  - New logistic regression, plus some of Kristinas data
  - Some tools to deal with Kristinas data
  - Score reimplementation in numpy
  - Precision vs recall
  - Precision vs recall
  - Precision vs recall
  - Better score again
  - Better score
  - Better scoring
  - Used all different window sizes in score development
  - Added data for different window sizes
  - Stuff
  - Split up evaluation and development
  - Extracted some logic into modules
  - Some new data and more tools
  - Bugfix to exclude near-shore scores
  - Created a new optimal score
  - More work towards a better scoring fit
  - Matched polynomials to fishing probabilities for all variables
  - More data, and converted the notebook to use structured arrays
  - Better graphing
  - Requirements for ipython
  - Initial commit
