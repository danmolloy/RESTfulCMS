# RESTful|CMS
## Overview
This project allows a user create blogs which are available at an API endpoint do render on their front end. It features user auth and CRUD database operations. 

## Features
- **Front-End integration** Adheres to RESTful principles for a well-defined and predictable API structure. Simply integrate into a front-end framework of your choice with the url `<url>/api/<str:username>/`.
- **User Authentication and Authorization** leverages Django's built-in authentication to ensure no one can access your account.
- **Blog Post** Define a BlogPost with title, body, status and publish date.
- **List and Detail Views** Seperate views to see a preview of all of your posts or one in detail.
- **CSS Styling** Responsive design principles using vanilla CSS to ensure the application adapts to different screen sizes and devices.


## Stack
The entire project has been built with Django & Python3. It uses a variety of built in Django libraries such as Django Auth, Templates and Tests.

## Testing
Unit tests have been written with `django.test` to cover all models, templates and views, focusing on maintaining a predictable UI, seamless CRUD operations with the database and auth logic. All tests are regularly reviewed to ensure failures are swiftly captured, and the site continues to be manually tested across a variety of screen sizes.

## Credit
The entire project is designed and built by Daniel Molloy.

## Running this project locally
Run this project locally with `python3 manage.py runserver`. It should automatically run on port `127.0.0.1`. 

To use the CMS, ensure your front end is in `CORS_ALLOWED_ORIGINS` in mycms/settings.py.

For more information about running Django, go to [Django Project](https://www.djangoproject.com/).