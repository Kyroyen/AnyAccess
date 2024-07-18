from rest_framework.throttling import AnonRateThrottle

class WebUnauthThrottle(AnonRateThrottle):

    def __init__(self):
        self.rate = "3/hour"
        super().__init__()
