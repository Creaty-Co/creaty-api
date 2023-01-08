from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.decorators import action

from app.base.consumers.mixins.json import AsyncJsonConsumerMixin


class EchoConsumer(AsyncJsonConsumerMixin, AsyncAPIConsumer):
    def __init__(self):
        AsyncJsonConsumerMixin.__init__(self)
        AsyncAPIConsumer.__init__(self)

    @action()
    async def echo(self, *args, **kwargs):
        return {'scope': self.scope, 'args': args, 'kwargs': kwargs}, 200
