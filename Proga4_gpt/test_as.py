import requests, pprint, pytest
from requests.auth import HTTPBasicAuth
import json

link="https://hr.recruit.liis.su/qa0/v1/api/<tester>/posts"
link_id="https://hr.recruit.liis.su/qa0/v1/api/<tester>/post"

resp=requests.get(link)
resp_json=resp.json()

pprint.pprint(resp_json)

@pytest.mark.get1
def test_get1():
    resp = requests.get(link)
    resp_json=resp.json()
    assert resp.status_code==200
    for item in resp_json:
        assert "title" in item
        assert "content" in item
        assert "publication_datetime" in item


@pytest.mark.get1_id
def test_get1_id():
    id = 849
    resp = requests.get(link_id+f"/{id}")
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'application/json'



@pytest.mark.post1
def test_post1():
    start = {
        "title":"yourpostname",
        "content":"yourpostcontent"
    }
    resp = requests.post(link, json=start, auth=HTTPBasicAuth('ruby', '123'))
    resp_json=resp.json()
    assert resp.status_code==201
    assert "title" in resp_json
    assert "content" in resp_json
    assert "publication_datetime" in resp_json
