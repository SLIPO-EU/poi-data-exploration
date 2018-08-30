import numpy as np
import pandas as pd
import re
from .statistics import Statistics

"""
Tools to extract categories and create the relevant distribution.
"""
class Categorical(Statistics):

	categories = []

	def __init__(self, inputSeries, chart_type='pie'):
		"""
		The Categorical class extracts the categories from the input series.
		For each category it constructs a data list with the distribution data.
		"""
		super().__init__(inputSeries, chart_type)
		self.categories = self.checkCategorical(inputSeries)
		for category in self.categories:
			value = np.sum(inputSeries.str.contains(category))
			self.append({'name': category, 'value': int(value)})

	def checkPattern(self, value, series):
		"""
		Given a value, this method returns the frequency this value
		occurs in the input series.
		"""
		pattern = '(?:^|\ )'+re.escape(value)+'(?:$|\ )'
		freq = np.sum(series.str.contains(pattern))
		return freq

	def checkCategorical(self, inputSeries):
		"""
		The actual method which finds the categories in series containing categorical data.
		According to sequential occurence of words, this method constructs the categories.
		"""
		words = inputSeries.str.split(" ").apply(pd.Series).stack().reset_index(drop=True)
		words = words.str.strip()
		categories = []

		test = []
		test_str = ''
		freq2 = 0
		for index, value in words.iteritems():
			original = test_str
			test.append(value)
			test_str = ' '.join(test)
			if (test_str in categories):
				test = []
				test_str = ''
				freq2 = 0
				continue
			freq1 = freq2
			freq2 = self.checkPattern(test_str, inputSeries)
			if (freq1 !=0 and freq2 != freq1):
				categories.append(original)
				if (value in categories):
					test = []
					test_str = ''
					freq2 = 0
				else:
					test = [value]
					test_str = value
					freq2 = self.checkPattern(value, inputSeries)
		return categories