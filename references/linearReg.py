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
plt.plot(x_fake[:100], y_fake[:100], 'g')
plt.plot(x, y, 'ok', ms=10);

# We create the model.
lr = lm.LinearRegression()

# We train the model on our training dataset.
# np.newaxis is just to transpose x[] row array into column array
lr.fit(x[:, np.newaxis], y)

# Now, we predict points with our trained model.
y_lr = lr.predict(x_fake[:, np.newaxis])

plt.plot(x_fake[:100], y_lr[:100], 'r')

plt.show()
print x_fake[:, np.newaxis]
