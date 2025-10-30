"""
Test suite for the High School Management System API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Reset activities to initial state before each test"""
    # Store original activities
    original_activities = copy.deepcopy(activities)
    
    # Reset to clean state for testing
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        }
    })
    
    yield
    
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)


class TestRootEndpoint:
    """Test the root endpoint"""
    
    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Test the GET /activities endpoint"""
    
    def test_get_activities_success(self, client, fresh_activities):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Basketball Team" in data
        
        # Verify structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestSignupEndpoint:
    """Test the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, fresh_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Basketball Team/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Signed up test@mergington.edu for Basketball Team"
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "test@mergington.edu" in activities_data["Basketball Team"]["participants"]
    
    def test_signup_nonexistent_activity(self, client, fresh_activities):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_signup_already_signed_up(self, client, fresh_activities):
        """Test signup when already signed up"""
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"
    
    def test_signup_activity_full(self, client, fresh_activities):
        """Test signup when activity is full"""
        # Fill up the Basketball Team (max 15 participants)
        for i in range(15):
            client.post(f"/activities/Basketball Team/signup?email=student{i}@mergington.edu")
        
        # Try to add one more
        response = client.post(
            "/activities/Basketball Team/signup?email=overflow@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Activity is full"
    
    def test_signup_with_url_encoded_activity_name(self, client, fresh_activities):
        """Test signup with URL-encoded activity name"""
        response = client.post(
            "/activities/Programming%20Class/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Signed up test@mergington.edu for Programming Class"


class TestUnregisterEndpoint:
    """Test the DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, fresh_activities):
        """Test successful unregister from an activity"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "michael@mergington.edu" not in activities_data["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_activity(self, client, fresh_activities):
        """Test unregister from non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_not_signed_up(self, client, fresh_activities):
        """Test unregister when not signed up"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student is not signed up for this activity"
    
    def test_unregister_with_url_encoded_activity_name(self, client, fresh_activities):
        """Test unregister with URL-encoded activity name"""
        response = client.delete(
            "/activities/Programming%20Class/unregister?email=emma@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Unregistered emma@mergington.edu from Programming Class"


class TestEdgeCases:
    """Test edge cases and error scenarios"""
    
    def test_signup_empty_email(self, client, fresh_activities):
        """Test signup with empty email"""
        response = client.post("/activities/Chess Club/signup?email=")
        assert response.status_code == 400
        assert response.json()["detail"] == "Email cannot be empty"
    
    def test_unregister_empty_email(self, client, fresh_activities):
        """Test unregister with empty email"""
        response = client.delete("/activities/Chess Club/unregister?email=")
        assert response.status_code == 400
        assert response.json()["detail"] == "Email cannot be empty"
    
    def test_signup_invalid_email_format(self, client, fresh_activities):
        """Test signup with invalid email format"""
        response = client.post("/activities/Chess Club/signup?email=invalid-email")
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid email format"
    
    def test_unregister_invalid_email_format(self, client, fresh_activities):
        """Test unregister with invalid email format"""
        response = client.delete("/activities/Chess Club/unregister?email=invalid-email")
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid email format"
    
    def test_signup_missing_email_parameter(self, client, fresh_activities):
        """Test signup without email parameter"""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == 422  # Validation error
    
    def test_unregister_missing_email_parameter(self, client, fresh_activities):
        """Test unregister without email parameter"""
        response = client.delete("/activities/Chess Club/unregister")
        assert response.status_code == 422  # Validation error


class TestDataIntegrity:
    """Test data integrity and state management"""
    
    def test_multiple_signups_and_unregisters(self, client, fresh_activities):
        """Test multiple signups and unregisters maintain data integrity"""
        # Sign up multiple students
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        for email in emails:
            response = client.post(f"/activities/Basketball Team/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all are signed up
        activities_response = client.get("/activities")
        basketball_participants = activities_response.json()["Basketball Team"]["participants"]
        for email in emails:
            assert email in basketball_participants
        
        # Unregister one
        response = client.delete("/activities/Basketball Team/unregister?email=student2@mergington.edu")
        assert response.status_code == 200
        
        # Verify only that one was removed
        activities_response = client.get("/activities")
        basketball_participants = activities_response.json()["Basketball Team"]["participants"]
        assert "student1@mergington.edu" in basketball_participants
        assert "student2@mergington.edu" not in basketball_participants
        assert "student3@mergington.edu" in basketball_participants
    
    def test_activity_capacity_tracking(self, client, fresh_activities):
        """Test that activity capacity is properly tracked"""
        # Get initial state
        activities_response = client.get("/activities")
        initial_count = len(activities_response.json()["Basketball Team"]["participants"])
        
        # Add a participant
        client.post("/activities/Basketball Team/signup?email=new@mergington.edu")
        
        # Verify count increased
        activities_response = client.get("/activities")
        new_count = len(activities_response.json()["Basketball Team"]["participants"])
        assert new_count == initial_count + 1
        
        # Remove the participant
        client.delete("/activities/Basketball Team/unregister?email=new@mergington.edu")
        
        # Verify count returned to original
        activities_response = client.get("/activities")
        final_count = len(activities_response.json()["Basketball Team"]["participants"])
        assert final_count == initial_count