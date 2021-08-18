from rest_framework import renderers
import json

class PostRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({
                'page': data.get('offset'),
                'results': data.get('items'),

                'total_results': data.get('total')
            })
            # response = json.dumps({
            #     'page': data.get('offset'),
            #     'tracks': {
            #         'href': data.get(),
            #         'items': data.get('items'),
            #     },
            #     'total_results': data.get('total')
            # })
            # response = json.dumps({'data': data.items})

        return response
        # return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)

class PaginationOffsetRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({
                'href': data.get('href'),
                'offset': data.get('offset'),
                'results': data.get('items'),
                'limit': data.get('limit'),
                'next': data.get('next'),
                'previous': data.get('previous'),
                'total_results': data.get('total'),
                'total_pages': round(data.get('total')/data.get('limit'))
            })
            # response = json.dumps({
            #     'page': data.get('offset'),
            #     'tracks': {
            #         'href': data.get(),
            #         'items': data.get('items'),
            #     },
            #     'total_results': data.get('total')
            # })
            # response = json.dumps({'data': data.items})

        return response
        # return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class FeedRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({
                # 'page': data.albums.get('offset'),
                # 'results': data.get('albums').get('items'),
                'results': data.get('items'),

                # 'total_results': data.albums.get('total')
            })
            # response = json.dumps({
            #     'page': data.get('offset'),
            #     'tracks': {
            #         'href': data.get(),
            #         'items': data.get('items'),
            #     },
            #     'total_results': data.get('total')
            # })
            # response = json.dumps({'data': data.items})

        return response
        # return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)

class AlbumFeedRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({
                # 'page': data.albums.get('offset'),
                # 'results': data.get('albums').get('items'),
                'results': data,

                # 'total_results': data.albums.get('total')
            })
            # response = json.dumps({
            #     'page': data.get('offset'),
            #     'tracks': {
            #         'href': data.get(),
            #         'items': data.get('items'),
            #     },
            #     'total_results': data.get('total')
            # })
            # response = json.dumps({'data': data.items})

        return response
        # return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
