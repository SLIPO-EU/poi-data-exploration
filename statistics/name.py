import pandas as pd
import re as regex
import numpy as np
from collections import OrderedDict
from .statistics import Statistics

class Name(Statistics):

	__groups = OrderedDict([
			('greek', '(?:[ςερτυθιοπασδφγηξκλζχψωβνμΕΡΤΥΘΙΟΠΑΣΔΦΓΗΞΚΛΖΧΨΩΒΝΜέύίόάήϋΰϊΐΈΎΊΌΆΉΫΪ0-9]+(?:$|\ ))'),
			('english', '(?:[a-zA-Z0-9]+(?:$|\ ))'),
			('(other or mixed language)', '(?:[^\(^\[^\]^\ )]+(?:$|\ ))')
		])

	def __init__(self, series, chart_type='pie'):
		super().__init__(series, chart_type)
		col = series
		i = 20
		while col.size > 0:
			i -= 1
			for key in self.__groups:
				row = {}
				regex = self.__groups[key] + '{'+str(i)+'}(?:(?:\(|\[)[^)^\]]+(?:\)|\])(?:$|\ ))*'
				match = col.str.match(regex)
				row["name"] = str(i) + ' ' + key + ' word(s)'
				try:
					row["value"] = int(match.value_counts()[1])
				except:
					row["value"] = 0
				else:
					self.append(row)
				col = pd.Series([col[index] for index, cond in match.iteritems() if not cond])
			if i==1:
				row['name'] = 'unrecognized'
				row['value'] = len(col)
				break