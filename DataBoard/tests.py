import json

import pandas
from django.http import JsonResponse
from django.test import Client, SimpleTestCase, LiveServerTestCase
from .metrics import Metric


class MetricTestCase(SimpleTestCase):
    def setUp(self) -> None:
        from scipy.misc import electrocardiogram

        sample_series = pandas.Series(electrocardiogram()[0:200])
        self.metric = Metric(sample_series)

    def test_get_max(self):  # TODO: Update!
        actual_max = self.metric.get_max()
        expected_max = {"x": 125, "y": 1.82}
        self.assertEqual(
            actual_max, expected_max, "Maximum value for sample Dataset should be 1.82"
        )


class BotMessageTestCase(LiveServerTestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_handle_bot_message_empty(self):
        response: JsonResponse = self.client.post("/bot_message_api/", {"msg": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"msg": "Das habe ich leider nicht verstanden"},
        )

    def test_handle_bot_message_max_value(self):
        response: JsonResponse = self.client.post(
            "/bot_message_api/", {"msg": "Wo liegt der maximale Ausschlag?"}
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(
            response_body["msg"],
            "Ich habe Ihnen das globale Maximum in der Grafik " "markiert.",
        )
        self.assertEqual(response_body["points"], [{"x": 125, "y": 1.82}])

    def test_handle_bot_message_local_max_values(self):
        response: JsonResponse = self.client.post(
            "/bot_message_api/", {"msg": "Welche lokalen Maxima gibt es?"}
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(
            response_body["msg"],
            "Ich habe Ihnen die Lokalen Maxima " "in der Grafik markiert.",
        )
        self.assertEqual(response_body["points"][0], {"x": 69, "y": 0.015})
