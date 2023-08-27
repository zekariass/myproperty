from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        custom_data = {
            "data": data,  # The original data from the view
        }
        return super(CustomJSONRenderer, self).render(
            custom_data, accepted_media_type, renderer_context
        )
