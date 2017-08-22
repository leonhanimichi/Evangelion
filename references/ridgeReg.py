#!/usr/bin/python

import numpy as np
import scipy.stats as st
import sklearn.linear_model as lm
import matplotlib.pyplot as plt
#%matplotlib inline

f = lambda x: np.exp(3 * x)

x_fake = np.linspace(0., 2, 200)

y_fake = f(x_fake)


x = np.array([0, .1, .2, .5, .8, .9, 1])
y = f(x) + np.random.randn(len(x))

plt.figure(figsize=(15,6))
plt.plot(x_fake[:200], y_fake[:200], '--k')
plt.plot(x, y, 'ok', ms=10)

lrp = lm.RidgeCV()

#we are iterating through 2 numbers of degrees (2 and 5), s is just a symbol for plotting
for deg, s in zip([2, 6, 10], ['-', '-', '-']):
	lrp.fit(np.vander(x, deg + 1), y)  #ALERT! FITTING HERE
	y_lrp = lrp.predict(np.vander(x_fake, deg + 1)) #ALERT! TESTING HERE
	plt.plot(x_fake[:200], y_lrp[:200], s, label='degree ' + str(deg))
	plt.legend(loc=2)
	#plt.xlim(0, 1.4)
	plt.ylim(-10, 40)

plt.show()
#print x_fake[:, np.newaxis]
