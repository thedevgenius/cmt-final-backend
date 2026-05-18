import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status

# This automatically gets your CustomUser model that we created earlier
User = get_user_model()

def send_and_store_otp(phone):
    """
    Checks/creates a user, sends an OTP via MSG91, and stores the response in memory.
    """
    # ------------------------------------------------------------------
    # STEP 1: Check if user exists or not, add user if they don't
    # ------------------------------------------------------------------
    # Using 'phone_number' because that is the field name on your CustomUser model
    user, created = User.objects.get_or_create(
        phone=phone,
        # defaults={'full_name': 'New User'} # Default name for new signups
    )

    # ------------------------------------------------------------------
    # STEP 2: Send OTP to MSG91 API
    # ------------------------------------------------------------------
    url = "https://api.msg91.com/api/v5/widget/sendOtp"
    payload = {
        "widgetId": settings.MSG_WIDGET_ID,
        "identifier": phone,
    }
    headers = {
        "content-type": "application/json",
        "authkey": settings.MSG_AUTH_KEY
    }

    try:
        # Make the POST request to MSG91
        response = requests.post(url, json=payload, headers=headers)
        
        # Raise an exception if the HTTP request failed (e.g., 404 or 500)
        response.raise_for_status() 
        
        # Parse the JSON response
        response_data = response.json()

        message = response_data["message"]

        # ------------------------------------------------------------------
        # STEP 3: Store the response in memory
        # ------------------------------------------------------------------
        # Create a unique cache key based on the user's phone number
        cache_key = f"msg91_otp_response_{phone}"
        
        # Store the response in Django's cache memory for 5 minutes (300 seconds)
        cache.set(cache_key, message, timeout=300)

        return {
            "success": True,
            "user_created": created,
            "message": "OTP sent successfully",
            "data": message
        }

    except requests.exceptions.RequestException as e:
        # Handle network errors, invalid API keys, etc.
        return {
            "success": False,
            "error": str(e)
        }
    
def verify_otp_service(phone: str, otp: str) -> dict:
    """Handles the business logic for verifying an OTP."""
    cache_key = f"msg91_otp_response_{phone}"
    req_id = cache.get(cache_key)

    if not req_id:
        return {
            "success": False, 
            "error": "Expired OTP or no request found.", 
            "status": status.HTTP_400_BAD_REQUEST
        }

    url = "https://api.msg91.com/api/v5/widget/verifyOtp"
    payload = {
        "widgetId": settings.MSG_WIDGET_ID,
        "reqId": req_id,
        "otp": otp
    }
    headers = {
        "content-type": "application/json",
        "authkey": settings.MSG_AUTH_KEY
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("type") != "success":
            return {
                "success": False, 
                "error": "Invalid or expired OTP.", 
                "status": status.HTTP_400_BAD_REQUEST
            }

        # Clear cache on success so OTP cannot be reused
        cache.delete(cache_key)
        
        return {"success": True, "status": status.HTTP_200_OK}

    except requests.exceptions.RequestException:
        return {
            "success": False, 
            "error": "Could not connect to the SMS gateway.", 
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }