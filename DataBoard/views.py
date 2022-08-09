import json

import pandas
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from .metrics import Metric
from scipy.misc import electrocardiogram

sample_metric = Metric(pandas.Series(electrocardiogram()[0:1000]))


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'sample_board.html')


def get_data(request: HttpRequest) -> HttpResponse:
    return JsonResponse({'data': sample_metric.data.to_dict()})


def handle_bot_message(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        msg = request.POST['msg'].lower() # noqa
        sample_points = [{'x': 100, 'y': 1.5}, {'x': 150, 'y': 1.5}]
        if msg == 'sample points':
            return JsonResponse({'points': sample_points})
        if msg == 'sample text':
            return JsonResponse({'msg': 'Sample Message'})
        # TODO: Integrate regex intent detection and entity extraction from virtual-tutor
        if 'lokal' in msg and 'max' in msg:
            return JsonResponse(
                {
                    'msg': 'Ich habe Ihnen die Lokalen Maxima in der Grafik markiert.',
                    'points': sample_metric.get_local_max(),
                }
            )
        if 'max' in msg:
            return JsonResponse(
                {
                    'msg': 'Ich habe Ihnen das globale Maximum in der Grafik markiert.',
                    'points': [sample_metric.get_max()],
                }
            )

        if 'zurück' in msg:
            return JsonResponse(
                {
                    'msg': 'Ich habe den Graphen zurückgesetzt',
                    'cmd': 'reset_chart',
                }
            )

        if 'interpretieren?' in msg:
            return JsonResponse(
                {
                    'msg': 'Eine gute Anleitung, wie Sie mit der Interpretation starten finden Sie '
                           '<a href="https://www.google.de">hier</a>.'}
            )

        return JsonResponse(
            {'msg': 'Das habe ich leider nicht verstanden'}
        )
    return JsonResponse({'text': 'GET-Anforderungen werden von dieser API nicht unterstützt'})
