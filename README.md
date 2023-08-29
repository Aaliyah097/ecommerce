# New catalog of server components
**Data Driven Implementation**

# DB Scheme
![sb_scheme](assets/db_scheme.png)

# Component Diagram
![component_diagram](assets/component_diagram.png)

# Dependencies
- Django v.4.*
- DRF v.3.*

# Run app
- pip install virtualenv
- virtualenv -p python3 venv
- venv\Scripts\activate.bat OR venv\Scripts\Activate.ps1
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- [optional] python mange.py createsuperuser (default: admin:admin)
- python manage.py runserver