import pandas as pd

class Statistics(object):

	def __init__(self, series, chart_type='pie'):
		self.chart_type = chart_type
		self.chart = {'type': chart_type, 'data': []} if chart_type == 'pie' else {'type': chart_type, 'data': {'name': [], 'value': []}}

	def append(self, row):
		if self.chart_type == 'pie':
			self.chart['data'].append(row)
		else:
			self.chart['data']['name'].append(row['name'])
			self.chart['data']['value'].append(row['value'])

	def reduceOther(self, chart, threshold=0.04):
		data = chart['data']
		values = []
		total = 0
		indices_to_delete = []
		enumeration = data if chart['type'] == 'pie' else data['value']
		for entry in enumeration:
			value = entry['value'] if chart['type'] == 'pie' else entry
			values.append(value)
			total += value
		limit = int(round(threshold*total, 0))
		for index, value in enumerate(values):
			if value <= limit:
				del values[index]
				if chart['type'] == 'pie':
					del data[index]
				else:
					del data['value'][index]
					del data['name'][index]

		return {'type': chart['type'], 'data': data}

	def checkPatterns(self, series, patterns):
		"""
		Iterate over patterns and construct the distribution of their appearance in the series.
		"""
		col = series
		for desc in patterns:
			pattern = r'^' + patterns[desc] + '$'
			match = col.str.match(pattern)
			col = pd.Series([col[index] for index, cond in match.iteritems() if not cond])
			try:
				value = int(match.value_counts()[1])
			except:
				value = 0
			else:
				self.append({'name': desc, 'value': value})
			if len(col)==0:
				break
		if len(col) > 0:
			row = {'name': 'unrecognized pattern', 'value': len(col)}
			self.append(row)