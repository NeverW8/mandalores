# Mandalores
A playground for some tools that the zHan community uses

## Quickstart
Setup a discord app and get the client id, client secret and redirect uri. You can do this by going to the discord developer portal and creating a new app.

Install the dependencies with pip
> pip3 install -r requirements.txt

Setup a postgresql database and edit the db_setup.sh file to match your database credentials. Then run the script to setup the database.
> ./db_setup.sh

Add your relevant credentials to a file called '.envrc' in the root directory. The file should look like this:
```
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
DISCORD_REDIRECT_URI=
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

Run the app
> python3 main.py

---

**Note**
This is a work in progress and is primarly used for an internal project for the zHan community.

## When doing development..
When we want to test a connnection or population of a database, we've created a dockerfile inside of the _dev_ folder.

