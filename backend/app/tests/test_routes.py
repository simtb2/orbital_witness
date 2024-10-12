from main import app
from fastapi.testclient import TestClient
from unittest import mock
from schemas.usage import Usage, UsageList

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Orbital Witness"}

def test_404():
    response = client.get("/foo")
    assert response.status_code == 404
    assert response.json() == {"message": "This Page Does Not Exist!"}

def test_get_usage_for_current_period():
    mock_usage_1: Usage = Usage(message_id=1, timestamp="foo", report_name="bar", credits_used=10.0)
    mock_usage_2: Usage = Usage(message_id=2, timestamp="bar", report_name="foo", credits_used=20.0)
    mock_usage_3: Usage = Usage(message_id=3, timestamp="foobar", report_name="barfoo", credits_used=30.0)
    mock_usage_list = UsageList(usage=[mock_usage_1, mock_usage_2, mock_usage_3])
    
    with mock.patch('services.usage_service.UsageService.get_usage_for_current_period', return_value=mock_usage_list):
        response = client.get("api/v1/usage")
        
        assert response.status_code == 200
        assert response.json() == {
            "usage": [
                {"message_id": 1, "timestamp": "foo", "report_name": "bar", "credits_used": 10.0},
                {"message_id": 2, "timestamp": "bar", "report_name": "foo", "credits_used": 20.0},
                {"message_id": 3, "timestamp": "foobar", "report_name": "barfoo", "credits_used": 30.0},
            ]
        }
