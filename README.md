# Mandalores
A playground for some tools that the zHan community uses

## Quickstart
Setup a discord app and get the client id, client secret and redirect uri. You can do this by going to the discord developer portal and creating a new app.

Install the dependencies with pip
> pip3 install -r requirements.txt

Add your relevant credentials to a file called '.envrc' in the root directory. The file should look like this:
```
DISCORD_CLIENT_ID=<not_needed>
DISCORD_CLIENT_SECRET=<not_needed>
DISCORD_REDIRECT_URI=<redirect_uri>
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Running the app
After you've setup the database and added your credentials to the .envrc file, you'll need to build the dockerfile.
> docker build -t mandalores .

Then you can run the docker container, exposing the correct port.
> docker run -p 5000:5000 mandalores

---

**Note**
This is a work in progress and is primarly used for an internal project for the zHan community.

## When doing development..
When we want to test a connnection or population of a database, we've created a dockerfile inside of the _dev_ folder.

Make sure to update your DATABASE_URL in the .envrc file to match your setup, i.e:

```bash
DATABASE_URL="postgresql+psycopg2://myuser:mysecretpassword@localhost:5432/mydatabase"
```
