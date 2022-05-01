# Fastapi based Todo List application
This application uses Redis to cache requests, JSON logging to log all the incoming requests and responses and
asyncio based motor driver for storing the data in MongoDB. OAuth2 is used with JWT bearer tokens to ensure security. I have also used Motor driver with AsyncIO to talk to the db. Code is well documented and maintained. It is easy to understand as I have added comments everywhere. I have also made a private bridge to use with redis and todo application in docker to ensure that everything is secure. It also uses Docker to run the entire application and pytest for tesing. Running this application is fairly simple. Below are the steps to do so. Make sure that docker and python is installed before proceeding.

1. `git clone https://github.com/Yash2017/todo-list-fastapi.git` Clone the repository
2. `cd todo-list-fastapi`
3. Edit DockerFile to change the environment variables. Make sure to add MONGODB_CONNECTION_URL as that would be used by the application to talk to MongoDB. You can head over to
[mongodb.com](https://www.mongodb.com/) and create an account or sign in to get your connection url. 
5. `docker build -t todolistfastapi:latest .` This command should build the image with the tag "todolistfastapi:latest"
6. `docker run --name redis -p 6379:6379 redis` This command should build and start the redis image for you
7. `docker stop redis` This command should kill the redis image for you. You don't want to start it now. You would start it later
8. `docker network create todolistappnetwork` This command would create the network "todolistappnetwork"
9. `docker run --rm --net todolistappnetwork --name redis -d redis` This command would start the redis container using our user defined "todolistappnetwork"
bridge
8. `docker run --rm --net todolistappnetwork -it -p 8000:8000 --name todolistfastapi -d todolistfastapi` This command would start the "todolistfastapi" container on port 8000

Yay! We are almost done now. Just head over to [localhost:8000/docs](localhost:8000/docs) to play with the API. To run the tests, simply head over to the testing folder 
by typing `cd testing` and then type `pytest`. Make sure that pytest is installed by typing `pip3 install pytest`. It should automatically run all the tests.
All the log files are saved as log.json and can be easily viewed.
