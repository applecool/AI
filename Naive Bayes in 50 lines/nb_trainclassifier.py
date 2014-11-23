def TrainClassifier(self):
                for fv in self.featureVectors:
                        self.labelCounts[fv[len(fv)-1]] += 1 #udpate count of the label
                        for counter in range(0, len(fv)-1):
                                self.featureCounts[(fv[len(fv)-1], self.featureNameList[counter], fv[counter])] += 1
 
                for label in self.labelCounts:  #increase label counts (smoothing). remember that the last feature is actually the label
                        for feature in self.featureNameList[:len(self.featureNameList)-1]:
                                self.labelCounts[label] += len(self.features[feature])