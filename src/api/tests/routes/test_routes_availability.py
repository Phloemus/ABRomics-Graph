
import requests

from config.constants import QUERIES 
from config.config import API_BASEPATH


def test_get_sample_sources():
    r = requests.post(url = f"/{API_BASEPATH}/sample-sources")
    assert r.status_code == True
