import sys
import numpy as np

from agents import CheapAgent, RandomAgent
from Agent_spamu import Agent_spamu #addition
from product import Product

if __name__ == '__main__':
    data_path = "./datasets/"
    data_group = "dataset1"
    # if you like, you can read the data_path and data_group using sys.argv
    
    X = np.loadtxt(data_path + data_group +  "_X.csv", dtype=float, delimiter=',') # features
    y = np.loadtxt(data_path + data_group +  "_y.csv", dtype=int) # bad (0) or good (1)
    prices = np.loadtxt(data_path + data_group +  "_p.csv", dtype=float) # prices

    value = 1000.
    
    num_products = X.shape[0]
    
    products = []
    
    for i in range(num_products):
        products.append(Product(X[i], value, prices[i]))
    
    #agent = CheapAgent("cheap")
    #agent = RandomAgent("random")
    agent = agent_spamu("spamu")
    
    agent_wealth = 0
    
    num_good_products_agent_has = 0
    
    # We'll gift you two random products, we'll give them to you for free
    
    seed = 42
    
    rs = np.random.RandomState(seed)
    
    # choose a good product
    
    good_products = np.nonzero(y==1)[0]
    chosen = rs.choice(good_products)
    products[chosen].price = 0 # it's our gift to you
    
    agent.add_to_my_products(products[chosen], 1)
    num_good_products_agent_has += 1
    
    agent_wealth += products[chosen].value
    
    del products[chosen]
    y = np.delete(y, chosen)
    
    # choose a bad product
    
    bad_products = np.nonzero(y==0)[0]
    chosen = rs.choice(bad_products)
    products[chosen].price = 0 # it's our gift to you
    
    agent.add_to_my_products(products[chosen], 0)
    
    
    del products[chosen]
    y = np.delete(y, chosen)
    
    num_products_you_can_choose = num_products / 2
    
    for _ in range(num_products_you_can_choose):
        chosen = agent.choose_one_product(products)
        agent.add_to_my_products(products[chosen], y[chosen])
        
        #print "Agent %s chose %s" %(agent, products[chosen])
        
        agent_wealth -= products[chosen].price
        
        if y[chosen] == 1: # a good product
            agent_wealth += products[chosen].value
            num_good_products_agent_has += 1
        
        del products[chosen]
        y = np.delete(y, chosen)
    
    
    print "{}'s final wealth:\t${:,.2f}".format(agent, agent_wealth)
    
    print "%s has %d good products." %(agent, num_good_products_agent_has)
        

    
    
    