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