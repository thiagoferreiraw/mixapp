#!/bin/bash
echo "Deploying to heroku..."
heroku git:remote -a aqueous-scrubland-68580
#git push heroku master
heroku config:set DATABASE_NAME=$DATABASE_NAME
heroku config:set DATABASE_USER=$DATABASE_USER
heroku config:set DATABASE_PASSWORD=$DATABASE_PASSWORD
heroku config:set DATABASE_HOST=$DATABASE_HOST
heroku config:set DATABASE_PORT=$DATABASE_PORT
heroku config:set SOCIAL_AUTH_FACEBOOK_KEY=$SOCIAL_AUTH_FACEBOOK_KEY
heroku config:set SOCIAL_AUTH_FACEBOOK_SECRET=$SOCIAL_AUTH_FACEBOOK_SECRET
heroku run python manage.py migrate
heroku ps:scale web=1