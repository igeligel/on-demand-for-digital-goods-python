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

"""Form validation using WTForms"""


from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class PurchaseForm(Form):
    """Validates Klarna On-Demand form data"""
    amount = IntegerField('Amount', validators=[DataRequired()])
    currency = StringField('Currency', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    origin_proof = StringField('Origin proof', validators=[DataRequired()])
    reference = StringField('Reference', validators=[DataRequired()])
    userToken = StringField('User token', validators=[DataRequired()])
