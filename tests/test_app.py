import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Original activities data for reset
ORIGINAL_ACTIVITIES = {
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
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and intramural games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["marcus@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and compete in matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Theater Production": {
        "description": "Perform in school plays and develop acting skills",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "ryan@mergington.edu"]
    },
    "Digital Art Club": {
        "description": "Create digital artwork using design software and tools",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["maya@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation skills and compete in debate competitions",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "ava@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore scientific concepts through experiments and projects",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["chloe@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test"""
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES)

client = TestClient(app)

def test_root_redirect():
    """Test root endpoint redirects to static index"""
    # Arrange
    # (client is set up)

    # Act
    response = client.get("/", allow_redirects=False)

    # Assert
    assert response.status_code == 302
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test getting all activities returns correct data"""
    # Arrange
    # (activities reset to original)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data == ORIGINAL_ACTIVITIES
    assert len(data) == 9  # number of activities

def test_signup_valid():
    """Test successful signup for an activity"""
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_participants = ORIGINAL_ACTIVITIES[activity]["participants"].copy()

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == len(initial_participants) + 1

def test_signup_duplicate():
    """Test signup fails when student already signed up"""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already in participants

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}

def test_signup_invalid_activity():
    """Test signup fails for non-existent activity"""
    # Arrange
    activity = "NonExistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_remove_participant_valid():
    """Test successful removal of participant"""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # exists in participants
    initial_participants = ORIGINAL_ACTIVITIES[activity]["participants"].copy()

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == len(initial_participants) - 1

def test_remove_participant_not_found():
    """Test removal fails when participant not in activity"""
    # Arrange
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}

def test_remove_participant_activity_not_found():
    """Test removal fails for non-existent activity"""
    # Arrange
    activity = "NonExistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}