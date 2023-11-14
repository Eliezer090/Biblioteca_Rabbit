import os
from rabbit_library import Rabbit


class Rabbit_test_library:
    def __init__(self,):
        rabbit_host = os.environ.get('RABBIT_HOST', '0.0.0.0')
        rabbit_port = os.environ.get('RABBIT_PORT', 5672)
        rabbit_virtual_host = os.environ.get('RABBIT_VIRTUAL_HOST', 'VIRTUAL_HOST')
        rabbit_user = os.environ.get('RABBIT_USER', 'guest')
        rabbit_password = os.environ.get('RABBIT_PASSWORD', 'guest')
        self.rabbit = Rabbit(rabbit_host, rabbit_port,
                             rabbit_virtual_host, rabbit_user, rabbit_password)
        self.queue = 'test_message_queue'
        self.exchange = 'exchange'

    def set_message(self)->bool:
        return self.rabbit.postMessage(self.queue,self.exchange, 'teste')

    def get_message(self):
        self.rabbit.getMessages(self.queue,self.exchange, self.process_message, 1)

    def process_message(self, channel, method, properties, body):
        message = body.decode()
        print(f'Retorno do rabbit: {message}')
        channel.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    rabbit = Rabbit_test_library()
    
    print(rabbit.set_message())
    rabbit.get_message()
    