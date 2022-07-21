# Team03 - FoodShare

## Instructions

1. Download/git clone https://git.shefcompsci.org.uk/com6103-2021-22/team03/project.git
2. Extract in a folder
3. If you were a win user, please open a powershell and use the following commands directly;
   If you were a mac user, please change the second command to 'source venv/bin/activate'

Commands:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py runserver


In config /settings.py the stripe keys belong to one of the team members - just put your own details in here (not all of these are connected to the project)

# Stripe Payment
1. PUBLISHABLE_KEY = ' '
2. SECRET_KEY = ' '

# Login Url
Login url is 'http://127.0.0.1:8000/'

# Admin Login
There is a user type identification when logining, thereby redirecting the admin users to admin dashboard automatically.
Please use following account to login the administration system:
username: admin
password: 123456

# Test Account
Individual user:
    username: Estrella
    password: 200228ct
Business user:
    username: MikeJ
    password: 200228ct
    
# Test for Bulk Uploading
Please use a csv file in the same format 'bulk_upload_example.csv' to test this feature
