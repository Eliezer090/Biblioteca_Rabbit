from unittest import TestCase, mock
from rabbit_library import Rabbit
from unittest.mock import MagicMock
import time
import os
import pytest
import signal
from pika.exceptions import StreamLostError
import pika.exceptions
import threading

class TestRabbit(TestCase):
    def setUp(self):
        self.rabbit = Rabbit('localhost', 5672, 'test', 'guest', 'guest')
        self.message_handler_mock = mock.MagicMock()

    def test_getmessages_success(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect'):
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                with mock.patch.object(os, "kill") as mock_kill:
                    self.rabbit.SelectConn = MagicMock()
                    self.rabbit.SelectConn.is_open = False
                    self.rabbit.channel = MagicMock()
                    self.rabbit.getMessages(
                        'test_queue', 'test', self.message_handler_mock, 1)
                    receive_message_mock.assert_called_once_with(
                        'test_queue', 'test', self.message_handler_mock, 1)
                    mock_kill.assert_called_with(os.getpid(), signal.SIGINT)
    
  
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch('pika.PlainCredentials')
    @mock.patch('time.sleep')
    def test_getmessages_success_with_reconnect_10_and_30(self, mock_sleep, mock_PlainCredentials, mock_ConnectionParameters, mock_BlockingConnection):
        with mock.patch.object(os, "kill") as mock_kill:
            self.rabbit.SelectConn = MagicMock()
            self.rabbit.SelectConn.is_open = False
            self.rabbit.channel = MagicMock()
            # Crie uma instância da sua classe
            my_instance = self.rabbit

            # Defina o comportamento esperado para as funções e classes do pika
            mock_PlainCredentials.return_value = 'credentials'
            mock_ConnectionParameters.return_value = 'parameters'
            mock_BlockingConnection.return_value = MagicMock()
            mock_BlockingConnection.return_value.is_open = False
            # Defina o valor de reconnect e qtd_reconnects
            my_instance.reconnect = True
            my_instance.qtd_reconnects = 11
            my_instance.continue_execution = False
            def side_effect(*args, **kwargs):
                if my_instance.qtd_reconnects >= 12:
                    my_instance.reconnect = False

            mock_sleep.side_effect = side_effect
            # Chame a função que você deseja testar
            my_instance.getMessages('test_queue', 'test', self.message_handler_mock, 1)
            # Verifique se qtd_reconnects foi incrementado corretamente, 13 pois ele vai passar 3 vezes é alimentado depois o qtd_reconnects
            self.assertEqual(my_instance.qtd_reconnects, 13)
    
    
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch('pika.PlainCredentials')
    @mock.patch('time.sleep')
    def test_getmessages_success_with_reconnect_more_than_50(self, mock_sleep, mock_PlainCredentials, mock_ConnectionParameters, mock_BlockingConnection):
        with mock.patch.object(os, "kill") as mock_kill:
            self.rabbit.SelectConn = MagicMock()
            self.rabbit.SelectConn.is_open = False
            self.rabbit.channel = MagicMock()
            # Crie uma instância da sua classe
            my_instance = self.rabbit

            # Defina o comportamento esperado para as funções e classes do pika
            mock_PlainCredentials.return_value = 'credentials'
            mock_ConnectionParameters.return_value = 'parameters'
            mock_BlockingConnection.return_value = MagicMock()
            mock_BlockingConnection.return_value.is_open = False
            # Defina o valor de reconnect e qtd_reconnects
            my_instance.reconnect = True
            my_instance.qtd_reconnects = 50
            my_instance.continue_execution = False
            def side_effect(*args, **kwargs):
                if my_instance.qtd_reconnects >= 51:
                    my_instance.reconnect = False

            mock_sleep.side_effect = side_effect
            # Chame a função que você deseja testar
            my_instance.getMessages('test_queue', 'test', self.message_handler_mock, 1)
            # Verifique se qtd_reconnects foi incrementado corretamente, 13 pois ele vai passar 3 vezes é alimentado depois o qtd_reconnects
            self.assertEqual(my_instance.qtd_reconnects, 52)
    
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch('pika.PlainCredentials')
    @mock.patch('time.sleep')
    def test_getmessages_success_with_reconnect_30_and_50(self, mock_sleep, mock_PlainCredentials, mock_ConnectionParameters, mock_BlockingConnection):
        with mock.patch.object(os, "kill") as mock_kill:
            self.rabbit.SelectConn = MagicMock()
            self.rabbit.SelectConn.is_open = False
            self.rabbit.channel = MagicMock()
            # Crie uma instância da sua classe
            my_instance = self.rabbit

            # Defina o comportamento esperado para as funções e classes do pika
            mock_PlainCredentials.return_value = 'credentials'
            mock_ConnectionParameters.return_value = 'parameters'
            mock_BlockingConnection.return_value = MagicMock()
            mock_BlockingConnection.return_value.is_open = False
            # Defina o valor de reconnect e qtd_reconnects
            my_instance.reconnect = True
            my_instance.qtd_reconnects = 30
            my_instance.continue_execution = False
            def side_effect(*args, **kwargs):
                if my_instance.qtd_reconnects >= 32:
                    my_instance.reconnect = False

            mock_sleep.side_effect = side_effect
            # Chame a função que você deseja testar
            my_instance.getMessages('test_queue', 'test', self.message_handler_mock, 1)
            # Verifique se qtd_reconnects foi incrementado corretamente, 13 pois ele vai passar 3 vezes é alimentado depois o qtd_reconnects
            self.assertEqual(my_instance.qtd_reconnects, 33)

    def test_getmessages_error_message_handler(self):
        with self.assertRaises(TypeError):
            self.rabbit.getMessages('queue', 'not_callable', None, 1)

    def test_getmessages_error_queue_None(self):
        with self.assertRaises(ValueError):
            self.rabbit.getMessages(
                None, 'not_callable', self.message_handler_mock, 1)

    def test_getmessages_success_exchange_none(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect'):
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                with mock.patch.object(os, "kill") as mock_kill:
                    self.rabbit.SelectConn = MagicMock()
                    self.rabbit.SelectConn.is_open = False
                    self.rabbit.channel = MagicMock()
                    self.rabbit.getMessages(
                        'test_queue', None, self.message_handler_mock, 1)
                    receive_message_mock.assert_called_once_with(
                        'test_queue', 'test', self.message_handler_mock, 1)

    def test_getmessages_success_set_default_limit_get_messages(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect'):
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                with mock.patch.object(os, "kill") as mock_kill:
                    self.rabbit.SelectConn = MagicMock()
                    self.rabbit.SelectConn.is_open = False
                    self.rabbit.channel = MagicMock()
                    self.rabbit.getMessages(
                        'test_queue', 'test', self.message_handler_mock, None)
                    receive_message_mock.assert_called_once_with(
                        'test_queue', 'test', self.message_handler_mock, 1)

    def test_get_messages_with_Exception(self,):
        with mock.patch.object(self.rabbit, '_Rabbit__is_connected') as is_connected_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                with self.assertLogs(level="ERROR") as log:
                    with mock.patch.object(os, "kill") as mock_kill:
                        self.rabbit.SelectConn = MagicMock()
                        self.rabbit.SelectConn.is_open = False
                        self.rabbit.channel = MagicMock()
                        is_connected_mock.side_effect = Exception(
                            'Error receiving message from rabbit:')
                        self.rabbit.getMessages(
                            'test_queue', 'test', self.message_handler_mock, 1)
                        assert "Error receiving message from rabbit:" in log.output[0]

    def test_post_message_success(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect') as connect_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__send_message') as send_message_mock:
                result = self.rabbit.postMessage(
                    'test_queue', 'test', 'test_message')
                send_message_mock.assert_called_once_with(
                    'test_queue', 'test', 'test_message')
                self.assertTrue(result)



    def test_post_message_error_queue_None(self):
        with self.assertRaises(ValueError):
            self.rabbit.postMessage(
                None, 'test', 'test_message')

    def test_post_message_success_exchange_none(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect') as connect_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__send_message') as send_message_mock:
                result = self.rabbit.postMessage(
                    'test_queue', None, 'test_message')
                send_message_mock.assert_called_once_with(
                    'test_queue', 'test', 'test_message')
                self.assertTrue(result)

    def test_post_message_with_Exception(self,):
        with mock.patch.object(self.rabbit, '_Rabbit__is_connected') as is_connected_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                with self.assertLogs(level="ERROR") as log:
                    is_connected_mock.side_effect = Exception(
                        'Error the send message to rabbit:')
                    self.rabbit.postMessage(
                        'test_queue', 'test', 'test_message')
                    assert "Error the send message to rabbit:" in log.output[0]

    def test_is_connected(self):
        assert not self.rabbit._Rabbit__is_connected()
        self.rabbit.channel = mock.Mock()
        assert not self.rabbit._Rabbit__is_connected()
        self.rabbit.channel.is_closed = False
        assert self.rabbit._Rabbit__is_connected()

    # Connects successfully to RabbitMQ server with valid credentials and parameters
    def test_connect_successfully(self):
        # Mock the pika.BlockingConnection class
        with mock.patch('pika.BlockingConnection') as mock_connection:
            self.rabbit._Rabbit__connect()
            mock_connection.assert_called_once()

    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch('pika.PlainCredentials')
    def test_connect(self, mock_PlainCredentials, mock_ConnectionParameters, mock_BlockingConnection):
        # Crie uma instância da sua classe
        my_instance = self.rabbit

        # Defina o comportamento esperado para as funções e classes do pika
        mock_PlainCredentials.return_value = 'credentials'
        mock_ConnectionParameters.return_value = 'parameters'
        mock_BlockingConnection.return_value = MagicMock()
        mock_BlockingConnection.return_value.channel.return_value.is_closed = False

        # Defina o valor de qtd_reconnects
        my_instance.qtd_reconnects = 1

        # Chame a função que você deseja testar
        my_instance._Rabbit__connect()

        # Verifique se as funções e classes do pika foram chamadas com os argumentos corretos
        mock_PlainCredentials.assert_called_once_with(my_instance.username, my_instance.password)
        mock_ConnectionParameters.assert_called_once_with(
            my_instance.host, my_instance.port, my_instance.virtualhost, 'credentials')
        mock_BlockingConnection.assert_called_once_with('parameters')

        # Verifique se a conexão foi estabelecida corretamente
        self.assertEqual(my_instance.SelectConn, mock_BlockingConnection.return_value)
        self.assertEqual(my_instance.channel, mock_BlockingConnection.return_value.channel.return_value)

        # Verifique se qtd_reconnects e reconnect_delay_system foram redefinidos corretamente
        self.assertEqual(my_instance.qtd_reconnects, 0)
        self.assertEqual(my_instance.reconnect_delay_system, my_instance.reconnect_delay_client)

    def test__send_message_sucess(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.queue_declare = MagicMock()
        self.rabbit.channel.queue_bind = MagicMock()
        self.rabbit.channel.basic_publish = MagicMock()
        self.rabbit._Rabbit__send_message(
            'teste_queue', 'teste_exchange', 'teste_message')
        assert self.rabbit._Rabbit__send_message(
            'teste_queue', 'teste_exchange', 'teste_message')
        self.rabbit.channel.queue_declare.assert_called_with(
            queue='teste_queue', durable=True)
        self.rabbit.channel.basic_publish.assert_called_with(
            exchange="teste_exchange", routing_key='teste_queue', body='teste_message')

    def test__send_message_error_queue_None(self):
        with self.assertRaises(ValueError):
            self.rabbit._Rabbit__send_message(
                None, 'teste_exchange', 'teste_message')

    def test_send_message_exception(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.queue_declare = MagicMock(
            side_effect=Exception('Error'))

        with pytest.raises(Exception):
            with self.assertLogs(level="ERROR") as log:
                assert not self.rabbit._Rabbit__send_message(
                    'teste_queue', 'teste_exchange', 'teste_message')
                assert "Error the send message to rabbit: Error" in log.output[0]

    def test_receive_message(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.queue_declare = MagicMock()
        self.rabbit.channel.queue_bind = MagicMock()
        self.rabbit.channel.basic_consume = MagicMock()

        message_handler = MagicMock()
        self.rabbit._Rabbit__receive_message(
            'teste_queue', 'teste_exchange', message_handler, 1)
        self.rabbit.channel.queue_declare.assert_called_with(
            queue='teste_queue', durable=True)
        self.rabbit.channel.queue_bind.assert_called_with(
            queue='teste_queue', exchange='teste_exchange', routing_key='teste_queue')
        self.rabbit.channel.basic_consume.assert_called_once()

    @mock.patch.object(Rabbit, '_Rabbit__is_connected')
    @mock.patch.object(Rabbit, '_Rabbit__connect')
    def test_receive_message_function_callback(self, connect_mock, is_connected_mock):
        # Set up mock objects
        ch = MagicMock()
        method = MagicMock()
        properties = MagicMock()
        body = "test message"
        message_handler = MagicMock()
        self.rabbit.channel = MagicMock()

        self.rabbit._Rabbit__receive_message(
            'teste_queue', 'teste_exchange', message_handler, 1)

        # Recupera a função que foi passada como callback do basic_consume call_args
        callback = self.rabbit.channel.basic_consume.call_args[1][
            "on_message_callback"
        ]
        # Invoca a função de callback
        callback(ch, method, properties, body)

        # verifica se afunção message_handler foi chamada com os argumentos corretos
        message_handler.assert_called_once_with(ch, method, properties, body)
    
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch('pika.PlainCredentials')
    def test_receive_message_with_continue_execution(self, mock_PlainCredentials, mock_ConnectionParameters, mock_BlockingConnection):
        # Crie uma instância da sua classe
        my_instance = self.rabbit
        my_instance.channel = MagicMock()
        # Defina o comportamento esperado para as funções e classes do pika
        mock_PlainCredentials.return_value = 'credentials'
        mock_ConnectionParameters.return_value = 'parameters'
        mock_BlockingConnection.return_value = MagicMock()
        mock_BlockingConnection.return_value.channel.return_value.start_consuming = MagicMock()

        # Defina o valor de continue_execution
        my_instance.continue_execution = True
        message_handler = MagicMock()
        # Chame a função que você deseja testar
        my_instance._Rabbit__receive_message(
            'teste_queue', 'teste_exchange', message_handler, 1)
        # Verifique se start_consuming foi chamado em um novo thread
        self.assertIsNotNone(my_instance.consume_thread)
        self.assertTrue(my_instance.consume_thread.name != '')

    def test_close_connection(self):
        # Set up Rabbit instance
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.is_closed = False
        # Call __close_connection method
        self.rabbit.close_connection()

        # Check that connection.close was called
        self.rabbit.channel.close.assert_called_once()

    def test_close_connection_exception(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.is_closed = False
        self.rabbit.channel.close.side_effect = Exception("test error")

        with self.assertLogs(level="ERROR") as log:
            self.rabbit.close_connection()
            assert "Error closing connection: test error" in log.output[0]
