from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """Test GET /activities endpoint"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Test structure of an activity
    activity = next(iter(activities.values()))
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)

def test_signup_for_activity():
    """Test POST /activities/{activity_name}/signup endpoint"""
    activity_name = "Chess Club"
    email = "test_user@mergington.edu"
    
    # First try signing up
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Verify student was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]
    
    # Try signing up again (should fail)
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    """Test signing up for a non-existent activity"""
    response = client.post(
        "/activities/NonexistentClub/signup",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_from_activity():
    """Test POST /activities/{activity_name}/unregister endpoint"""
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    
    # First verify the user is registered
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]
    
    # Try unregistering
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Verify student was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
    
    # Try unregistering again (should fail)
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_unregister_nonexistent_activity():
    """Test unregistering from a non-existent activity"""
    response = client.post(
        "/activities/NonexistentClub/unregister",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
