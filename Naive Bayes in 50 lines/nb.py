#Sweet implementation of Naive Bayes Classifier. Credits to the author
#Author: Krishnamurthy Koduvayur Viswanathan
 
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
 
        '''The TrainClassifier method simply counts the number of co-occurrences of each feature value with each class 
           label, and stores them in the form of 3-tuples. These counts are automatically smoothed by using add-one smoothing
            as the default value of count for this dictionary is ‘1’. The counts of the labels is also adjusted by 
            incrementing these counts by the total number of observations.'''

        def TrainClassifier(self):
                for fv in self.featureVectors:
                        self.labelCounts[fv[len(fv)-1]] += 1 #udpate count of the label
                        for counter in range(0, len(fv)-1):
                                self.featureCounts[(fv[len(fv)-1], self.featureNameList[counter], fv[counter])] += 1
 
                for label in self.labelCounts:  #increase label counts (smoothing). remember that the last feature is actually the label
                        for feature in self.featureNameList[:len(self.featureNameList)-1]:
                                self.labelCounts[label] += len(self.features[feature])
 
        def Classify(self, featureVector):      #featureVector is a simple list like the ones that we use to train
                probabilityPerLabel = {}
                for label in self.labelCounts:
                        logProb = 0
                        for featureValue in featureVector:
                                logProb += math.log(self.featureCounts[(label, self.featureNameList[featureVector.index(featureValue)], featureValue)]/self.labelCounts[label])
                        probabilityPerLabel[label] = (self.labelCounts[label]/sum(self.labelCounts.values())) * math.exp(logProb)
                print probabilityPerLabel
                return max(probabilityPerLabel, key = lambda classLabel: probabilityPerLabel[classLabel])
                                
        '''The above method simply reads the feature names (including class labels), their possible values, 
           and the feature vectors themselves; and populate the appropriate data structures defined above.'''

        def GetValues(self):
                file = open(self.trainingFile, 'r')
                for line in file:
                        if line[0] != '@':  #start of actual data
                                self.featureVectors.append(line.strip().lower().split(','))
                        else:   #feature definitions
                                if line.strip().lower().find('@data') == -1 and (not line.lower().startswith('@relation')):
                                        self.featureNameList.append(line.strip().split()[1])
                                        self.features[self.featureNameList[len(self.featureNameList) - 1]] = line[line.find('{')+1: line.find('}')].strip().split(',')
                file.close()
 
        def TestClassifier(self, arffFile):
                file = open(arffFile, 'r')
                for line in file:
                        if line[0] != '@':
                                vector = line.strip().lower().split(',')
                                print "classifier: " + self.Classify(vector) + " given " + vector[len(vector) - 1]                                
		
if __name__ == "__main__":
        model = Model("/home/tennis.arff")
        model.GetValues()
        model.TrainClassifier()
        model.TestClassifier("/home/tennis.arff")