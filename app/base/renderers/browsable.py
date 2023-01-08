from rest_framework.renderers import BrowsableAPIRenderer as _BrowsableAPIRenderer


class BrowsableAPIRenderer(_BrowsableAPIRenderer):
    template = 'base/api.html'

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type, renderer_context)
        context['patch_form'] = self.get_rendered_html_form(
            data, renderer_context['view'], 'PATCH', renderer_context['request']
        )
        return context
