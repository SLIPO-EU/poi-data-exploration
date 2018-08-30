import pandas as pd
import re as regex
import numpy as np
from .statistics import Statistics

class PriceRange(Statistics):
	"""docstring for PriceRange"""

	regex = '(\s*[0-9]*)[^0-9]+([0-9]*)'

	def __init__(self, inputSeries, chart_type='pie'):
		super().__init__(inputSeries, chart_type)
		matches = self.createDistribution(inputSeries)
		for key, value in matches.iteritems():
			self.append({'name': key, 'value': int(value)})

	def createDistribution(self, col):
		match = col.str.extract(self.regex, expand=False)
		bins = match.apply(self.bins, axis=1)
		return bins.value_counts().astype('int')

	def bins(self, values):
		empty = True
		try:
			value1 = float(values[0])
			empty = False
		except:
			value1 = ''
		try:
			value2 = -float(values[1])
			empty = False
		except:
			value2 = '+'
		if not empty:
			return str(value1) + str(value2)