class BasePaginationMixin:
    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {'type': 'integer', 'example': 123},
                'results': schema,
            },
        }
