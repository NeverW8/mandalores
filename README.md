
![Linting workflow](https://github.com/NeverW8/mandalores/actions/workflows/linting.yml/badge.svg)
![Build workflow](https://github.com/NeverW8/mandalores/actions/workflows/docker-image.yml/badge.svg)

# Mandalores
A playground for some tools that the zHan community uses

## Quickstart
Setup a discord app and get the client id, client secret and redirect uri. You can do this by going to the discord developer portal and creating a new app.

Install the dependencies with pip
> pip3 install -r requirements.txt

Add your relevant credentials to a file called '.envrc' in the root directory. The file should look like this:
```
ENV=local
DISCORD_CLIENT_ID=<client-id>
DISCORD_CLIENT_SECRET=<client-secret>
DISCORD_REDIRECT_URI=<redirect_uri>
```

### Setting up the database
After you've added your credentials to the .envrc file, you'll need to start up the database,
> docker-compose -d up

Then you want to run the migrations
> ./manage.py migrate

### Running the app
To run the app for developmen you just do:
> ./manage.py runserver 8000

Then you can browse to http://localhost:8000
Then to start the Discord Auth process click the login

To get the sound clips to be generated you need to run the task processor in a seperate terminal as such:
> ./manage.py process_tasks

---
**Note**
This is a work in progress and is primarly used for an internal project for the zHan community.

## When doing development..
When we want to test a connnection or population of a database, we've created a dockerfile inside of the _dev_ folder.

Make sure to update your DATABASE_URL in the .envrc file to match your setup, i.e:

```bash
DATABASE_URL="postgresql+psycopg2://myuser:mysecretpassword@localhost:5432/mydatabase"
```
