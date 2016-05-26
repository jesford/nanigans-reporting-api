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
from ..models import PreparedRequest, Adapter, Response


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

	:param site: str, unique site id assigned by Nanigans
	:param source: str, dataSource field 
	"""

	required_fields = {'source':'componentplacements'}
	response = PreparedRequest('attributes', required_fields).send()

	return response


def get_metrics():
	"""Retrieves available metrics for given data source.

	Endpoint:
	/sites/:siteId/datasources/placements/metrics

	:param site: str, unique site id assigned by Nanigans
	:param source: str, dataSource field 
	"""

	required_fields = {'source':'placements'}
	response = PreparedRequest('metrics', required_fields).send()

	return response


def get_view(view, depth=0):
	"""Retrieves data for a specific view id. 

	Endpoint:
	/sites/:siteId/datasources/placements/views/:viewId

	:param site: str, unique site id assigned by Nanigans
	:param source: str, dataSource field 
	:param view: str, view id of created view
	:param format: str, json
	"""

	required_fields = {'source':'placements','view':view}
	parameters = {'format':format,'depth':depth}
	response = PreparedRequest('view', required_fields, parameters).send()
	
	return response


def get_stats(attributes=None, metrics=None, start=None, end=None, depth=0):
	"""Retrieves specific data requested given set of parameters.

	Endpoint:
	/sites/:siteId/datasources/placements/views/adhoc

	:param site: str, unique site id assigned by Nanigans
	:param source: str, dataSource field 
	:param metrics: list/str, metrics fields
	:param attributes: list/str, attributes fields 
	:param start: str, start date in %Y-%m-%d format 
	:param end: str, end date in %Y-%m-%d format 
	:param format: str, json 
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
		response += request.send()

	return response 









