from rest_framework import renderers
import json


# This renderer class helps us to get the Json response in a particular format.
# You can modify the json response for each view function OR you can just create this
# class once and call it in the view function.
class UserRenderer(renderers.JSONRenderer):

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ""

        if "ErrorDetail" in str(data):
            response = json.dumps({"errors_new": data})

        else:
            response = json.dumps({"data": data})

        # for debugging only
        # import pdb
        # pdb.set_trace()
        return response
