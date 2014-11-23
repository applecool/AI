from __future__ import division
import collections
import math
 
class Model: 
        def __init__(self, arffFile):
                self.trainingFile = arffFile
                self.features = {}      #all feature names and their possible values (including the class label)
                self.featureNameList = []       #this is to maintain the order of features as in the arff
                self.featureCounts = collections.defaultdict(lambda: 1)#contains tuples of the form (label, feature_name, feature_value)
                self.featureVectors = []        #contains all the values and the label as the last entry
                self.labelCounts = collections.defaultdict(lambda: 0)   #these will be smoothed later