#! /usr/bin/python
'''
Created on Mar 15, 2018

@author: usman.mohyuddin

The purpose of this script is to predict events 
using Baysian rule which states as 

P(C|X) = P(X|C)P(C) / P(X)

where 
(if we take example of spam detection)


P(C)    =   Prior = would be probability that the message is spam
P(X|C)  =   Likelihood =  is the probability that the given word (input) is Spam, given that the message is Spam.
P(X)    =   Evidence = is just the probability of a word appearing in a message using the given training data.
P(C|X)  =   Posterior
'''
import csv
import sys
from configparser import ConfigParser
from builtins import str

lines = ''
no_of_columns = 0

class NaiveBayes(object):
    '''
    classdocs
    '''
    column_header = ''
    positve_dictionary = {}
    negative_dictionary = {}
    sum_of_positive_values = 0
    sum_of_negative_values = 0
    
    key_set = set()
    
    
    def __init__(self,column):
        '''
        initialize with name/header of particular column
        '''
        self.column_header = column        
        
        
    # Extract the key,values from given coloumns
    # and hold records of each key according to its value 
    def extract_and_preprocess(self,start,end):
    
        # Extract all the keys of features
        key_list = [key.strip() for key in start]
    
        # It will keep unique keys only
        self.key_set = set(key_list)
    
        # Dictionary which holds positive (yes) values of keys
        self.positive_dict = {key:0 for key in self.key_set}
    
        # Dictionary which holds negative (no) values of keys
        self.negative_dict = {key:0 for key in self.key_set}
    
        # iterate over all lines of file and put values
        # in positive or negative dictionaries accordingly
        for x,y in zip(start,end):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        
            # extract key from line
            key = x.strip()
        
            # extract values from line
            value = y.strip()
        
            #depending upon values, add in respective dictionary
            if value.lower() == 'yes':
                
                # increment in sum of respective key 
                self.positive_dict[key] = self.positive_dict[key] + 1 
        
            elif value.lower() == 'no':
                
                # increment in sum of respective key
                self.negative_dict[key] = self.negative_dict[key] + 1 
        

                
    def frequency_table(self):
        
        # Format & Print Frequency Table
        
        print('\n'*1)
        print('Frequency Table')
        print('-' * 35)

        # headers of columns
        print("{:18} {:10} {:12}".format(self.column_header,'Yes',' No'))
        print('-' * 35)

        # print the frequency-table w.r.t keys and their YES,NO frequency
        for key in self.key_set:
            print("{:10} {:10} {:10}".format(key,self.positive_dict[key],self.negative_dict[key]))
        print('-' * 35)

        # calculate and print frequency of positive(Yes) and negative(No)
        
        self.sum_of_positive_values = sum(self.positive_dict.values())
        self.sum_of_negative_values = sum(self.negative_dict.values())
        
        overall_positive = self.sum_of_positive_values/(self.sum_of_positive_values + self.sum_of_negative_values)
        overall_negative = self.sum_of_negative_values/(self.sum_of_positive_values + self.sum_of_negative_values)
        
        print("{:18} {:10} {:10}".format('',format(overall_positive,'.2f'),format(overall_negative,'.2f')))



    def likelihood_table(self):
        
        # Format & Print Likelihood Table 
        print('\n'*1)
        print('Likelihood Table')
        print('-' * 48)


        # headers of columns
        print("{:18} {:10} {:12} {:12}".format(self.column_header,'Yes',' No', 'P(x)'))
        print('-' * 48)


        # print the likelihood-table w.r.t keys and their YES,NO values
        for key in self.key_set:
            positive_likelihood = self.positive_dict[key]/self.sum_of_positive_values
            negative_likelihood = self.negative_dict[key]/self.sum_of_negative_values
            p_of_x = (self.positive_dict[key] + self.negative_dict[key]) / (self.sum_of_positive_values + self.sum_of_negative_values)
        
            print("{:18} {:10} {:12} {:12}".format(key,format(positive_likelihood, '.2f'),
                                               format(negative_likelihood,'.2f'),format(p_of_x,'.2f')))
        
        print('-' * 48)
        print('\n'*1)
        
    #def compute_frequency(self):
    #   print(sum(self.positive_dict['Normal'].values())
        
    def command(self,feature):
        
        pos_frequency = (self.positive_dict[feature]/self.sum_of_positive_values) 
        neg_frequency = (self.negative_dict[feature]/self.sum_of_negative_values)
        

        return pos_frequency,neg_frequency
        
    def prior_probability_multiply_likelihood(self,pos,neg):
        
        positive_posterior = pos *  (self.sum_of_positive_values/(self.sum_of_positive_values + self.sum_of_negative_values))
        negative_posterior = neg *  (self.sum_of_negative_values/(self.sum_of_positive_values + self.sum_of_negative_values))

        
        flag = 'YES' if (positive_posterior/(positive_posterior+negative_posterior)) >= (negative_posterior/(positive_posterior+negative_posterior)) else 'NO' 
        print('Should do it ?  ',str(flag))
        
if __name__ == '__main__':
    
    
    #read file name from command line
    file = sys.argv[1]
    col = ''
    with open(file) as f:
        
        reader = csv.DictReader(f, delimiter = ',')
        col = reader.fieldnames
        #row = next(reader)
        no_of_columns = len(col)
        lines = f.readlines()
    
    #print(lines)
    
    
    objects_list = []
    for i in range(no_of_columns-1):
        obj = NaiveBayes(col[i])
        objects_list.append(obj)
        
        
    for i in range(no_of_columns-1):
        first_colum = [x.strip().split(',')[i] for x in lines]
        last_colum =  [x.strip().split(',')[-1] for x in lines]
        
        objects_list[i].extract_and_preprocess(first_colum,last_colum)
        objects_list[i].frequency_table()
        objects_list[i].likelihood_table()
    
    config = ConfigParser()
    config.read('config.ini')

    
    key_list = []
    value_list = []
    
    for section in config.sections():
            for (key,value) in config.items(section):
                value_list.append(value)
                key_list.append(key.title())
                
    
    pos = 1
    neg = 1
    
    for i in range(no_of_columns - 1):
        positives, negatives =  objects_list[i].command(value_list[i])
        pos = pos * positives
        neg = neg * negatives
    
    objects_list[0].prior_probability_multiply_likelihood(pos, neg)
