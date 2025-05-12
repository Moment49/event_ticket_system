import logging
from django.conf import settings
from django.http import HttpResponse
import json
import os

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class MaintenaceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization
    def __call__(self, request):
        # logger.info("Request recieved")
        # Code to be executed for each request before
        #the view (and later middleware) are called
        if settings.MAINTENANCE_MODE:
            logger.warning("Application is in maintenace mode")
            return HttpResponse("Application is in maintenace mode. Please try again later")

        response = self.get_response(request)

        # Code to be executed for each request/response after 
        # the view is called
        return response



app_directory = os.path.dirname(__file__)  # This gets the current file's directory 

# Now construct the path for the logins.json file inside your app folder
filename = os.path.join(app_directory, 'login_attempts.json')
class CustomLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.Loginsuccesattempts = 0
        self.failedloginattempts = 0

    def __call__(self, request):
        req_path = request.path
        
        email = request.POST.get('email')  # or use request.data.get('email') if it's a JSON request
        response = self.get_response(request)

        # Execute after the response
        if req_path == '/auth/login/' and request.method == 'POST':
            # Check if the user has successfully logged in
            if request.user.is_authenticated:
                # User successfully authenticated
                self.Loginsuccesattempts += 1
                logger.info(f"Login attempt success: {self.Loginsuccesattempts} by {request.user}")
                data_json = {
                    "user": str(request.user),
                    "loginattempt": str(self.Loginsuccesattempts),
                    "message": "Login attempt success"
                }
                # Update the log file
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'a') as f:
                    if f.tell() > 0:
                        f.write(',\n')
                    json.dump(data_json, f)
                    f.write('\n')
            else:
                # User failed to authenticate
                self.failedloginattempts += 1
                logger.info(f"Failed login attempt: {self.failedloginattempts} by {email}")
                data_json = {
                    "user": email,
                    "loginattempt": str(self.failedloginattempts),
                    "message": "Login attempt failed"
                }
                # Update the log file
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'a') as f:
                    if f.tell() > 0:
                        f.write('\n') 
                    json.dump(data_json, f)
                    f.write('\n')

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        print(f"view name:{view_func.__name__}")
        pass
