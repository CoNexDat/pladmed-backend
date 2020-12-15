from json import JSONEncoder
from pladmed.models.probe import Probe

class JsonEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Probe):
			return obj.public_data()

		return JSONEncoder.default(self, obj)
