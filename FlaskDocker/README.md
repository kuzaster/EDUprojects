# How to run FinalApp:

 - Install [Python 3.8](https://www.python.org/downloads/)
- Install [Docker](https://www.docker.com/)
- Open terminal
- Clone the [repository](https://github.com/kuzaster/python_training_2020/tree/main/FinalApp)
- Go to main directory of the project `/FinalApp`
- Create virtual environment and activate it
- Install packages from requirements `pip install -r requirements.txt`
 - Run `flask run` 
- Open up your web browser and enter (http://localhost:5000/) in the address field to see the working app
- You could _add, change or remove_ containers from a browser or _config-file.yaml_ in a directory of the project `/FinalApp/app`

# Example. How to add a new container:

- Run app and open main page (http://localhost:5000/) in your browser
- Push the button `Add new container`
- At the opened page fill next fields:
  - ContainerName: `inanimate-echo-server`
  - ImageName: `inanimate/echo-server`
  - Port: `8080`
  - PublicURL: `http://localhost:10000`
- Push the button `Add and run container`
- After few seconds you will see the page of the new container