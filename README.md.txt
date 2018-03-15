The purpose of this script is to predict the events on the basis of prior information using naive bayes.

The Bayesian Rule is:

 P(C|X) = P(X|C) * P(C)  / P(x)

So for example, 
if we apply this to a Spam Filter, then P(C) would be the probability that the message is Spam, 
and P(X|C) is the probability that the given word (input) is Spam, given that the message is Spam. 
P(X) is just the probability of a word appearing in a message using the given training data.

Input format

The prior data should be in csv file, make sure you follow consistency in defining keys and their values.
'Temp' and 'temp' will be treated as two different things.

DO NOT ADD KEY/VALUE for last column of your csv file.


This script accepts inpt from 'config.ini' file.
