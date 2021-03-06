from __future__ import absolute_import
from __future__ import unicode_literals
import json

import logging

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from collections import OrderedDict
import requests
from requests_oauthlib import OAuth2


@login_required
def bbof_get_fhir(request, resource_type):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    endpoint = '/protected/bluebutton/fhir/v1/%s/?patient=59b99cd030c49e0001481f44&_format=json' % (
        resource_type)

    url = urljoin(
        getattr(
            settings,
            'OAUTH2IO_HOST',
            "https://dev.bluebutton.cms.fhirservice.net"), endpoint)
    print(url)
    # % (request.user.username)

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content
    else:
        content = response.content

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_eob(request):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(
        getattr(
            settings,
            'OAUTH2IO_HOST',
            "https://dev.bluebutton.cms.fhirservice.net"),
        '/protected/bluebutton/fhir/v1/ExplanationOfBenefit/')
    # ?patient=%s % (request.user.username)
    print("EOB URL", url)
    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}

    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content

    else:
        content = response.json()

    # print(content)

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_coverage(request):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(
        getattr(
            settings,
            'OAUTH2IO_HOST',
            "https://dev.bluebutton.cms.fhirservice.net"),
        '/protected/bluebutton/fhir/v1/Coverage/?_format=json')
    # patient = % s? request.user.username
    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}

    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content
    else:
        content = response.json()

    # print(content)

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_patient(request):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(
        getattr(
            settings,
            'OAUTH2IO_HOST',
            "https://dev.bluebutton.cms.fhirservice.net"),
        '/protected/bluebutton/fhir/v1/Patient/'
        '?_format=json')

    # % (request.user.username)

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content
    else:
        content = response.content

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)
