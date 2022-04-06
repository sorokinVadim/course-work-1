from coursework.models import *


def test_client():
    client = Client("Vadim", "Sorokin", 19, 88888888)
    assert client.is_valid(), True
    client = Client("", "", 19, 00000000)
    assert client.is_valid(), False
    client = Client("Vadim", "Sorokin", 17, 00000000)
    assert client.is_valid(), False
    client = Client("Vadim", "Sorokin", 19, 00)
    assert client.is_valid(), False




