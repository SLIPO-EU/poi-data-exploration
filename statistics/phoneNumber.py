import pandas as pd
import numpy as np
from collections import OrderedDict
from .statistics import Statistics

class PhoneNumber(Statistics):

	categories = {
		('Only numbers', '^[0-9]+$'),
		('Numbers and parentheses', '^(?:[0-9]*[\(][0-9]+[\)][0-9]*)+$'),
		('Numbers and + symbol', '^(?:[0-9]*[\+][0-9]+)+$'),
		('Numbers and - symbol', '^(?:[0-9]*[\-][0-9]+)+$'),
		('Numbers, + and - symbol', '^(?:[0-9]*[+][0-9]+[-][0-9]*)+$'),
		('Numbers, parentheses and + symbol', '^[0-9\(\)\+]+$'),
		('Numbers, parentheses and - symbol', '^[0-9\(\)\-]+$'),
		('Numbers, parentheses, + and - symbol', '^[0-9\(\)\+\-]+$'),
		('Only non numerical characters', '^[^0-9]+$')
	}

	def __init__(self, series, chart_type='pie'):
		super().__init__(series, chart_type)
		self.categories = OrderedDict(self.categories)
		super().checkPatterns(series, self.categories)
