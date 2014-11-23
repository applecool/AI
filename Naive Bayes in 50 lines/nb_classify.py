def Classify(self, featureVector):      #featureVector is a simple list like the ones that we use to train
                probabilityPerLabel = {} #store the final probability for each class label
                for label in self.labelCounts:
                        logProb = 0
                        for featureValue in featureVector:
                                logProb += math.log(self.featureCounts[(label, self.featureNameList[featureVector.index(featureValue)], featureValue)]/self.labelCounts[label])
                        probabilityPerLabel[label] = (self.labelCounts[label]/sum(self.labelCounts.values())) * math.exp(logProb)
                print probabilityPerLabel
                return max(probabilityPerLabel, key = lambda classLabel: probabilityPerLabel[classLabel])