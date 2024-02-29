### First installation
1. Run `npm install` to install FlowBite and TailwindCSS
2. Run `pip install django-compress` to install Django Compress
3. Run the server `python manage.py runserver`

### Errors:
1. No module named `rest_framework`:
    - Run `pip install djangorestframework`
2. No such table `product_product`:
    - Run `python manage.py migrate`
3. `src/output.css` could not be found in...
    - Run `npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch`

### How to launch with Docker?
Run `docker compose up --build web` to build and launch docker image.