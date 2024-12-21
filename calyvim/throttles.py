from rest_framework.throttling import UserRateThrottle

class ResendEmailThrottle(UserRateThrottle):
    rate = "2/minute"