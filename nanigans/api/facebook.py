"""
The .api.facebbok module contains the core methods used to retrieve data from native Facebook 
ads data from Nanigans:

	.get_timeranges:: used to retrieve built-in time range for data sources
	.get_attributes:: used to retrieve all dimensions available for data source
	.get_metrics:: used to retrieve all metrics available for data source
	.get_view:: used to retrieve a specific view created in the Nanigans interface
	.get_stats:: used to retrieve data for user-defined queries

"""

from datetime import date, timedelta
from ..utils import generate_dates
from ..models import PreparedRequest, Response


def get_timeranges():
	"""Retrieves available time ranges for given data source.

	Endpoint:
	/sites/:siteId/datasources/placements/timeRanges

	:param site: str, unique site id assigned by Nanigans
	:param source: str, dataSource field 
	"""
	
	required_fields = {'source':'placements'}
	response = PreparedRequest('timeranges', required_fields).send()

	return response


def get_attributes():
	"""Retrieves available attributes for given data source.

	Endpoint:
	/sites/:siteId/datasources/placements/attributes
	"""

	required_fields = {'source':'componentplacements'}
	response = PreparedRequest('attributes', required_fields).send()

	return response


def get_metrics():
	"""Retrieves available metrics for given data source.

	Endpoint:
	/sites/:siteId/datasources/placements/metrics
	"""

	required_fields = {'source':'placements'}
	response = PreparedRequest('metrics', required_fields).send()

	return response


def get_view(view, depth=0):
	"""Retrieves data for a specific view id. 

	Endpoint:
	/sites/:siteId/datasources/placements/views/:viewId

	:param view: str, view id of created view
	:param depth: int, dimension depth of data
	"""

	required_fields = {'source':'placements','view':view}
	parameters = {'format':format,'depth':depth}
	response = PreparedRequest('view', required_fields, parameters).send()

	# The fbSpend field returns string integers with comma separator.
	# The commas need to be removed to perform operations on them.

	if response.data[0]['fbSpend']: 
		for record in response.data:
			record['fbSpend'] = record['fbSpend'].replace(',','')
	
	return response


def get_stats(attributes=None, metrics=None, start=None, end=None, depth=0):
	"""Retrieves specific data requested given set of parameters.

	Endpoint:
	/sites/:siteId/datasources/placements/views/adhoc
	
	:param attributes: list/str, attributes fields 
	:param metrics: list/str, metrics fields
	:param start: str, start date in %Y-%m-%d format 
	:param end: str, end date in %Y-%m-%d format 
	:param depth: int, dimension depth of data
	"""

	if isinstance(metrics, str):
		metrics = [metrics]
	if not metrics:
		metrics = ['impressions','clicks','fbSpend']
	if isinstance(attributes, str):
		attributes = [attributes]
	if not attributes:
		attributes = ['budgetPool','strategyGroup','adPlan']

	if start == None or end == None:
		start = (date.today()-timedelta(days=7)).strftime('%Y-%m-%d')
		end = (date.today()-timedelta(days=1)).strftime('%Y-%m-%d')

	dates = generate_dates(start,end)
	response = Response()
	required_fields = {'source':'placements'}

	for day in dates:
		parameters = {'metrics[]=':metrics,
					  'attributes[]=':attributes,
					  'start':day,
					  'end':day,
					  'depth':depth}
		request = PreparedRequest('adhoc', required_fields, parameters)
		record = request.send()

		# The fbSpend field returns string integers with comma separator.
		# The commas need to be removed to perform operations on them.

		if record.data['fbSpend']:
			record.data['fbSpend'] = record.data['fbSpend'].replace(',','')
		response += record
		if response.errors:
			break

	return response 










