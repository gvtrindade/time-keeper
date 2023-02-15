# Time-Keeper
A digital time clock system

## Running the app locally

- Create a virtual environment:

      python -m venv /path/to/new/virtual/environment

- Reopen the terminal, it will automatically open the virtual environment
- Install the `requirements.txt` libraries:

      pip install -r requirements.txt

- Inside /timekeeper, create a .env file with the following variables:
  - SECRET_KEY
  - DEBUG
  - EMAIL_HOST
  - EMAIL_PORT
  - EMAIL_USE_SSL
  - EMAIL_HOST_USER
  - EMAIL_HOST_PASSWORD

- Migrate the models to the database:

      python manage.py makemigrations
      python manage.py migrate

- Add the custom admin user:

      echo "from auths.models import CustomUser; admin = CustomUser.objects.create_superuser('admin', password='password'); admin.is_staff = True; admin.save()" | python manage.py shell

- Run the app:

      python manage.py runserver