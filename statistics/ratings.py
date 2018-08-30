import re
import numpy as np
from .statistics import Statistics

"""
The module to extract ratings and create their distribution.
"""
class Ratings(Statistics):

	__unrecognized = 0
	"""	The number of unrecognized entries."""

	data = []
	"""	The distribution data."""

	width = 0
	"""	The width of the bin."""

	def __init__(self, inputSeries, chart_type='pie'):
		"""
		This class first extracts the ratings, it creates the distribution bins
		and finally it writes down the distribution.
		"""
		series = inputSeries.astype('str')
		super().__init__(series, chart_type)
		series = series.map(self.extractRating)
		self.width = self.createBins(series)
		series.map(self.__distribute)
		self.append(self.data)

	def append(self, data):
		for entry in data:
			super().append(entry)

	def extractRating(self, string):
		"""
		Method to extract the rating from a string.

		First it replaces comma to dot and then it extracts a float number.
		"""
		try:
			string = string.replace(',', '.')
			p = re.compile('([0-9.]+)')
			string = p.findall(string)[0]
			if string == 'nan':
				string = ''
			rating = float(string)
			return rating
		except:
			self.__unrecognized += 1
			return float('NaN')

	def createBins(self, series):
		"""
		According to the maximum value in the series, it creates classes with
		maximum value a multiply of 5 and width depending on the maximum value.
		"""
		max_value = (series.max()//5 + 1)*5
		width = max_value / 10 if max_value%10 == 0 else max_value / 5
		for low in np.arange(0, max_value, width):
			self.data.append({'name': str(low) + '-' + str(low+width), 'value': 0})
		return width

	def __distribute(self, value):
		"""
		Classification of the value in the distribution.
		"""
		try:
			bin = int(value // self.width)
			self.data[bin]['value'] += 1
		except:
			pass