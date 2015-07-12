# content of conftest.py
import pytest
from marshmallow import Schema, fields
import os
import sys
class SecretsContainer(Schema):
    calendars = fields.List(fields.String())


def pytest_addoption(parser):
    parser.addoption("--secrets", action="store",
        help="Configuration Options Path")

@pytest.fixture
def secrets(request):
    spath = request.config.getoption("--secrets") or "test_options.json"
    fstring = "{}"
    if os.path.exists(spath):
        with open(spath) as f:
            fstring = f.read()

    marshalled, errors = SecretsContainer().loads(fstring)

    if errors:
        pytest.exit("Errors with the secrets container unmarshal")

    return marshalled
