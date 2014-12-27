from agents import Agent
from sklearn.naive_bayes import BernoulliNB,GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
#from sklearn.tree import DecisionTreeClassifier

import numpy as np

class Agent_spamu(Agent):

	def __init__(self, name, seed=0):
		super(Agent_spamu, self).__init__(name)
		
		self.train_count =0 
		self.X = []
		self.y =[]
		self.list_classifiers = []
		
		#GaussianNB
		self.list_classifiers.append(GaussianNB())
		
		#SVC
		self.list_classifiers.append(SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.0,
  			kernel='rbf', max_iter=-1, probability=True, random_state=None,
    		shrinking=True, tol=0.001, verbose=False))
		
		#LogisticRegression
		val_C = [1.0,5.0,18.0,50.0,100.0]
		for value in val_C:
			self.list_classifiers.append(LogisticRegression(C=value, fit_intercept=True))
		
		#BernoulliNB
		alpha_val = [-100,-50,-10,-5,0,1]
		for value in alpha_val:
			self.list_classifiers.append(BernoulliNB(alpha=value, binarize=0.0, class_prior=None, fit_prior=True))
		
	
	#overriding the add_to_my_products method in agents file
	def add_to_my_products(self, product, label):
		self.my_products.append(product)
		self.product_labels.append(label)
		
		self.X.append(product.features)
		self.y.append(label)
	
	
	
	def fit_classifier(self, X_train,y_train,X_validation, y_validation, products, products_labels): 
		potential = {}
		
		
		for classifier in self.list_classifiers:
			classifier.fit(X_train,y_train)
			potential[classifier] = 0
		
		for classifier in self.list_classifiers:
			no_products = X_validation.shape[0]
			for i in range(no_products):
				proba = classifier.predict_proba(X_validation[i])[0][1]
				if proba == proba:
					if proba > products[i].price / products[i].value:
						if products_labels[i] ==1:
							potential[classifier] += (products[i].value - products[i].price)
						else:
							potential[classifier] -= products[i].price
				else:
					pass
		
		
		self.classifier = classifier
		for classifier in self.list_classifiers:
			if potential[self.classifier] < potential[classifier]:
				self.classifier = classifier
		
		
		self.classifier.fit(np.array(X_train.tolist() + X_validation.tolist()),np.array(y_train.tolist() + y_validation.tolist()))
		
		
		
	def choose_one_product(self, products):
		
		self.train_count = self.train_count+1
		print(self.train_count)
		
		X_train = np.array([])
		y_train = np.array([])
		new_products = []
		
		if self.train_count < 4:
			X_train = np.array(self.X)
			y_train = np.array(self.y)
			
			X_val = np.array(self.X)
			y_val = np.array(self.y)
			
			new_product_labels = self.product_labels
			new_products = self.my_products
		
		elif self.train_count >= 4:
			X_train = np.array(self.X[:len(self.X)/2])
			y_train = np.array(self.y[:len(self.y)/2])
			
			X_val = np.array(self.X[len(self.X)/2:])
			y_val = np.array(self.y[len(self.y)/2:])
			
			new_product_labels = self.product_labels[len(self.product_labels)/2:]
			new_products = self.my_products[len(self.my_products)/2:]
			
			
		self.fit_classifier(X_train, y_train, X_val, y_val, new_products, new_product_labels)
			
		
		max_val = 0
		good_products = 0
		for val in range(len(products)):
			new_proba = self.classifier.predict_proba(products[val].features)[0][1]
			new_value = new_proba*(products[val].value - products[val].price)
			if(new_value>max_val):
				max_val=new_value
				good_products=val
		
		print good_products
		return good_products
	
				
		