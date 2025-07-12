#!/usr/bin/env python3
"""
Test script for LawViksh Backend API
Run this script to test all API endpoints
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint"""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(BASE_URL)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    print("\n🔐 Testing admin login...")
    try:
        data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{API_BASE}/auth/adminlogin", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if result.get("success") and result.get("data", {}).get("access_token"):
            return result["data"]["access_token"]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_user_registration(token=None):
    """Test user registration"""
    print("\n👤 Testing user registration...")
    try:
        data = {
            "name": "Test User",
            "email": f"testuser{int(time.time())}@example.com",
            "phone_number": "+1234567890",
            "gender": "Male",
            "profession": "Student",
            "interest_reason": "Testing the API"
        }
        response = requests.post(f"{API_BASE}/users/userdata", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_creator_registration(token=None):
    """Test creator registration"""
    print("\n👨‍💼 Testing creator registration...")
    try:
        data = {
            "name": "Test Creator",
            "email": f"testcreator{int(time.time())}@example.com",
            "phone_number": "+1234567891",
            "gender": "Female",
            "profession": "Lawyer",
            "interest_reason": "Testing the API"
        }
        response = requests.post(f"{API_BASE}/users/creatordata", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_not_interested_submission(token=None):
    """Test not interested submission"""
    print("\n❌ Testing not interested submission...")
    try:
        data = {
            "name": "Not Interested User",
            "email": f"notinterested{int(time.time())}@example.com",
            "phone_number": "+1234567892",
            "gender": "Other",
            "profession": "Other",
            "not_interested_reason": "Too complex",
            "improvement_suggestions": "Make it simpler",
            "interest_reason": "Not interested in legal resources"
        }
        response = requests.post(f"{API_BASE}/notint/notinteresteddata", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_feedback_submission(token=None):
    """Test feedback submission"""
    print("\n💬 Testing feedback submission...")
    try:
        data = {
            "user_email": f"feedback{int(time.time())}@example.com",
            "visual_design_rating": 4,
            "ease_of_navigation_rating": 5,
            "mobile_responsiveness_rating": 4,
            "overall_satisfaction_rating": 4,
            "task_completion_rating": 5,
            "service_quality_rating": 4,
            "liked_features": "Clean interface and easy navigation",
            "improvement_suggestions": "Add more features",
            "desired_features": "Document templates",
            "legal_challenges": "Finding relevant information",
            "follow_up_consent": "yes",
            "follow_up_email": f"feedback{int(time.time())}@example.com"
        }
        response = requests.post(f"{API_BASE}/feedback/submit", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_admin_endpoints(token):
    """Test admin-only endpoints"""
    if not token:
        print("\n❌ No admin token available, skipping admin tests")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🔒 Testing admin endpoints...")
    
    # Test get users
    try:
        response = requests.get(f"{API_BASE}/users/registereduserdata", headers=headers)
        print(f"Get users - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Users count: {len(data.get('data', []))}")
    except Exception as e:
        print(f"Get users error: {e}")
    
    # Test get creators
    try:
        response = requests.get(f"{API_BASE}/users/registeredcreatordata", headers=headers)
        print(f"Get creators - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Creators count: {len(data.get('data', []))}")
    except Exception as e:
        print(f"Get creators error: {e}")
    
    # Test get feedback
    try:
        response = requests.get(f"{API_BASE}/feedback/all", headers=headers)
        print(f"Get feedback - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Feedback count: {len(data.get('data', []))}")
    except Exception as e:
        print(f"Get feedback error: {e}")
    
    # Test analytics
    try:
        response = requests.get(f"{API_BASE}/users/analytics", headers=headers)
        print(f"Get user analytics - Status: {response.status_code}")
    except Exception as e:
        print(f"Get analytics error: {e}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting LawViksh API Tests")
    print("=" * 50)
    
    # Test basic endpoints
    health_ok = test_health_check()
    root_ok = test_root_endpoint()
    
    if not health_ok:
        print("❌ Health check failed. Make sure the server is running!")
        return
    
    # Test public endpoints
    user_ok = test_user_registration()
    creator_ok = test_creator_registration()
    not_interested_ok = test_not_interested_submission()
    feedback_ok = test_feedback_submission()
    
    # Test admin login
    token = test_admin_login()
    
    # Test admin endpoints
    if token:
        admin_ok = test_admin_endpoints(token)
    else:
        admin_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Health Check: {'✅' if health_ok else '❌'}")
    print(f"Root Endpoint: {'✅' if root_ok else '❌'}")
    print(f"User Registration: {'✅' if user_ok else '❌'}")
    print(f"Creator Registration: {'✅' if creator_ok else '❌'}")
    print(f"Not Interested: {'✅' if not_interested_ok else '❌'}")
    print(f"Feedback Submission: {'✅' if feedback_ok else '❌'}")
    print(f"Admin Login: {'✅' if token else '❌'}")
    print(f"Admin Endpoints: {'✅' if admin_ok else '❌'}")
    
    if all([health_ok, root_ok, user_ok, creator_ok, not_interested_ok, feedback_ok, token, admin_ok]):
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main() 