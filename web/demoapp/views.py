import random
from django.shortcuts import render
from . import tasks
import neurokit2 as nk
import pandas as pd
import json


def index(request):
    context = {}
    return render(request, 'demoapp/index.html', context)


def celery_index(request):
    context = {}
    return render(request, 'demoapp/celery_index.html', context)


def random_add(request):
    a, b = random.choices(range(100), k=2)
    tasks.add.delay(a, b)
    context = {'function_detail': 'add({}, {})'.format(a, b)}
    return render(request, 'demoapp/celery_detail.html', context)


def random_mul(request):
    a, b = random.choices(range(100), k=2)
    tasks.mul.delay(a, b)
    context = {'function_detail': 'mul({}, {})'.format(a, b)}
    return render(request, 'demoapp/celery_detail.html', context)


def random_xsum(request):
    array = random.choices(range(100), k=random.randint(1, 10))
    tasks.xsum.delay(array)
    context = {'function_detail': 'xsum({})'.format(array)}
    return render(request, 'demoapp/celery_detail.html', context)


def neurokit_index(request):
    data = pd.read_csv("/Users/siyuqian/Study/django-docker/712AF22B_Mar11_14-07-59.csv");
    # Generate 15 seconds of PPG signal (recorded at 250 samples / second)
    # ppg = nk.ppg_simulate(duration=15, sampling_rate=250, heart_rate=70)
    ppg = nk.ppg_process(data['PPG'], sampling_rate=50)

    # Clear the noise
    ppg_clean = nk.ppg_clean(ppg)

    # Peaks
    peaks = nk.ppg_findpeaks(ppg_clean, sampling_rate=100)

    # Compute HRV indices
    hrv_indices = nk.hrv(peaks, sampling_rate=100, show=True)
    result = hrv_indices.to_json()
    parsed = json.loads(result)
    context = {'response' : json.dumps(parsed)}
    return render(request, 'neurokit/neurokit_index.html', context)
