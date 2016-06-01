"""
The .api module contains the core methods used to retrieve publisher data from Nanigans 
(e.g. MoPub):

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
	/sites/:siteId/datasources/componentpublisherstimeRanges
	"""
	
	required_fields = {'source':'componentpublishers'}
	response = PreparedRequest('timeranges', required_fields).send()

	return response

def get_attributes():
	"""Retrieves available attributes for given data source.

	Endpoint:
	/sites/:siteId/datasources/componentpublishersattributes
	"""
	
	required_fields = {'source':'componentpublishers'}
	response = PreparedRequest('attributes', required_fields).send()

	return response

def get_metrics():
	"""Retrieves available metrics for given data source.

	Endpoint:
	/sites/:siteId/datasources/componentpublishersmetrics
	"""
	
	required_fields = {'source':'componentpublishers'}
	response = PreparedRequest('metrics', required_fields).send()

	return response

def get_view(view, depth=0):
	"""Retrieves data for a specific view id. 

	Endpoint:
	/sites/:siteId/datasources/componentpublishersviews/:viewId

	:param view: str, view id of created view
	:param format: str, json
	"""

	required_fields = {'source':'componentpublishers','view':view}
	parameters = {'depth':depth}
	response = PreparedRequest('view', required_fields, parameters).send()
		
	return response

def get_stats(attributes=None, metrics=None, start=None, end=None, depth=0):
	"""Retrieves specific data requested given set of parameters.

	Endpoint:
	/sites/:siteId/datasources/componentpublishersviews/adhoc

	:param attributes: list/str, attributes fields 
	:param metrics: list/str, metrics fields
	:param start: str, start date in %Y-%m-%d format 
	:param end: str, end date in %Y-%m-%d format 
	:param depth: int, dimensions depth of data
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
	required_fields = {'source':'componentpublishers'}

	for day in dates:
		parameters = {'metrics[]=':metrics,
					  'attributes[]=':attributes,
					  'start':day,
					  'end':day,
					  'depth':depth}
		request = PreparedRequest('adhoc', required_fields, parameters)
		response += request.send()

	return response 










