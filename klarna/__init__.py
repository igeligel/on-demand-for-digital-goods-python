#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019-present Klarna AB

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Backend server for Klarna On-Demand"""

import requests
import base64

from .forms import PurchaseForm
from flask import Flask, jsonify, render_template, request
from flask_wtf.csrf import CsrfProtect
from werkzeug.exceptions import BadRequest


__author__ = 'Mattias Granlund'

app = Flask(__name__)  # Flask rules!
app.config.from_object('klarna.config')
CsrfProtect(app)

@app.route('/')
def route_home():
    """Renders the Klarna On-Demand template"""
    return render_template('home.html',
                           api_key=app.config['API_KEY'],
                           amount=7,
                           currency='SEK')

@app.route('/purchase', methods=['POST'])
def route_purchase():
    """Handles a purhcase request"""

    form = PurchaseForm(request.form)
    form.validate()  # Throws exception if data is invalid.

    # Let's declare the URL components at runtime for sake of clarity.
    api_hostname = 'inapp.playground.klarna.com'
    order_endpoint = '/api/v1/users/%s/orders' % form.userToken.data
    order_url = 'https://%s%s' % (api_hostname, order_endpoint)

    payload = {
        'user_token': form.userToken.data,
        'reference': form.reference.data,  # Item reference
        'name': form.name.data,  # Item description
        'order_amount': form.amount.data,
        'order_tax_amount': 0,
        'currency': form.currency.data,
        'origin_proof': form.origin_proof.data
    }

    api_secret = app.config['API_SECRET']
    api_key = app.config['API_KEY']

    # To make an authorized request we concatenate the api key and secret
    # using a colon separator, and base64 encode the result.
    auth_token = base64.b64encode('%s:%s' % (api_key, api_secret))
    headers = {'Authorization': 'Basic ' + auth_token}

    req = requests.post(order_url, data=payload, headers=headers)
    if req.status_code == 201:
        # A 201 Created status indicates the purchase was successful.
        return jsonify(data={'status': 'success'})
    else:
        # For any other status code you are likely to see an error message in
        # the response body.
        return jsonify(data={'status': req.text})
