import numpy as np
import pandas as pd
import re
import unicodedata
from .statistics import Statistics

"""
The module to extract opening days.
"""
class Schedule(Statistics):

	distribution = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
	days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	local_days = []

	def __init__(self, inputSeries, chart_type='pie'):
		"""
		The Schedule class converts the input series to lowercase,
		strips accents, finds the dominant locale and finally
		constructs the opening days distribution.
		"""
		super().__init__(inputSeries, chart_type)
		series = inputSeries.str.lower()
		series = series.map(self.strip_accents)
		self.local_days = self.__find_locale(inputSeries)
		series = series.map(self.construct_schedule)
		series = series.map(self.distribute)
		for day in self.distribution:
			self.append({'name': day, 'value': self.distribution[day]})


	def strip_accents(self, s):
		"""
		It strips a string from accents using unicodedata module.
		"""
		return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

	def construct_schedule(self, entry):
		"""
		In a schedule entry, it searches for time patterns,
		and returns the parts without times.
		"""
		p = re.compile('([^0-9]+)[0-9]{1,2}[:.][0-9]{1,2}[^0-9]*[0-9]{1,2}[:.][0-9]{1,2}')
		return p.findall(entry)

	def __add_day(self, index):
		"""
		An auxiliary private method to add one item to the days
		distribution according to input index.
		"""
		day = self.days[index]
		self.distribution[day] += 1

	def __find_locale(self, series):
		"""
		It searches the series for the first day of the week,
		and it returns the week days of the dominant locale.
		"""
		days = {
			'el': ['κυ', 'δε', 'τρ', 'τε', 'πε', 'πα', 'σα'],
			'en': ['su', 'mo', 'tu', 'we', 'th', 'fr', 'sa'],
			'fr': ['di', 'lu', 'ma', 'me', 'je', 've', 'di']
		}
		max_frequency = 0
		dominant_locale = ''
		for locale in days:
			pattern = days[locale][0]
			frequency = np.sum(series.str.contains(pattern))
			if frequency > max_frequency:
				max_frequency = frequency
				dominant_locale = locale
		return days[dominant_locale]


	def distribute(self, entry):
		"""
		Given an input entry, it finds the days range according
		to rules stated below, and sums up the relevant frequency in
		opening days distribution.
		These rules are:
		a. in case days are separated by commas, the days are considered
		separate,
		b. in case there are more than one days with other words in between,
		it is supposed that represents the range of these days.
		"""
		days = self.local_days
		for values in entry:
			start = -1
			end = -1
			for word in values.split(' '):
				if word[0:2] in days:
					index = days.index(word[0:2])
					if start == -1:
						start = index
					else:
						end = index

			if end == -1:
				self.__add_day(start)
			elif start <= end:
				for index in range(start, end + 1):
					self.__add_day(index)
			else:
				for index in range(0, end + 1):
					self.__add_day(index)
				for index in range(start, 7):
					self.__add_day(index)