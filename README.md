Clone the repo 

Environment Variables used can be found in .env.example

These environment variables should be set before running the app

They can be set by creating the file .env(copy .env.example and change values) in root directory or plain environment variables

If you're running a virtualenv you can start app by running python3 bot/app.py from root directory 

Or you can use docker(this will help you run server locally with minimal fuss)

Install docker and docker-compose in your machine

Instructions be found here 

https://docs.docker.com/engine/installation/

https://docs.docker.com/compose/install/

From the root directory of the project run

docker-compose build

docker-compose up
