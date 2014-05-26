from flask import Response, json


class JsonResponse(Response):
    def __init__(self, raw_data, status=200):
        data = json.dumps(raw_data)
        super(JsonResponse, self).__init__(data,
                                           status=status,
                                           content_type='application/json')
