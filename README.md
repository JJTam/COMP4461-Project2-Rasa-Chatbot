# HCI Project 2 - Human-Robot Interaction in Self-Quarantine
<h2> A Rasa Chatbot by UST Gang Gang </h2>
<img src="square-logo.svg" width=255 height=255 align="right">

This is the project developed by UST Gang Gang Team with the use of Rasa 2.5.1

This project is built and referenced from the following repositories:
* https://github.com/QingyuGuo/rasa-2.5-tutorial
* https://github.com/RasaHQ/rasa-2.x-form-examples
* https://github.com/scalableminds/chatroom
* https://github.com/vishwaspuri/Interactive-Voice-Response

## Environment Setup

1. Need to install [Conda/virtualenv](https://www.anaconda.com/). 


2. Check your environment (require python3.8 / 3.9; upgrade it if needed)

  ```bash
  python --version
  pip --version
  conda -V
  ```
    Upgrade Conda (if needed)

    conda update -n base -c defaults conda
 
3. Clone this repository

  ```bash
  git clone https://github.com/JJTam/COMP4461-Project2-Rasa-Chatbot.git
  ```

4. Change into project directory:

  ```bash
  cd COMP4461-Project2-Rasa-Chatbot/
  ```

5. Create python environment

  ```bash
  conda create --name <environment-name> python=3.8 
  ```

6. Activate the environment

  ```bash
  conda activate <environment-name>
  ```

7. Install required dependencies

  ```bash
  pip install -r requirements.txt
  ```

## Run the project ([learn more](https://rasa.com/docs/rasa/2.x/command-line-interface))

1. Change to the chatbot root

  ```bash
  cd chatbot
  ```

2. Train the model

  ```bash
  rasa train
  ```

3. Start chatting

  ```bash
  rasa shell
  or
  rasa interactive (recommanded for debugging, writing stories)
  ```

4. Run actions (in a new terminal)

  ```bash
  rasa run actions
  ```

### Useful commands [(learn more)](https://rasa.com/docs/rasa/2.x/default-actions/)

  ```bash
  /restart => action_restart
  ```
  ```bash
  /back => action_back
  ```


## Web User Interface

### 1. Chatroom

The project `./UI/chatroom` provides a basic interface for interacting with bots in the webpage, which supports text and voice as input. Please refer to https://github.com/scalableminds/chatroom for more details.

* In your Rasa bot setup, make sure to include the Rasa [REST channel](https://rasa.com/docs/rasa/user-guide/connectors/your-own-website/#rest-channels) in your `credentials.yml` file:
```bash
rest:
  # pass
  ```

* Install the dependencies for web application
```bash
cd UI/chatroom
# install dependencies if you have not installed
npm install -g yarn
yarn install
``` 

* Usage - You need to open 3 terminal/shell windows:


*Terminal-1*: For Rasa server. Depending on your setup you might need to add CORS headers, e.g. `--cors "*"`.

  ```bash
  # change to chatbot directory
  cd chatbot
  # Run Rasa server
  rasa run --credentials ./credentials.yml  --enable-api --auth-token XYZ123 --model ./models --endpoints ./endpoints.yml --cors "*"
  ```

*Terminal-2*: Run Rasa action server if you need customized actions

  ```bash
  # change to chatbot directory
  cd chatbot
  # Run Rasa action server
  rasa run actions
  ```

*Terminal 3*: For web application
   
  ```bash
  cd UI/chatroom
  # run the local host
  yarn serve
  ```
Then open http://localhost:8080/index.html in your browser.


### 2. Interactive-Voice-Response
* The original project: https://github.com/vishwaspuri/Interactive-Voice-Response I make slight modifications here.


* Usage - You need to open 3 terminal/shell windows:


*Terminal-1*:  For Rasa server 

  ```bash
  # change to chatbot directory
  cd chatbot
  # run RASA core server
  rasa run --enable-api --verbose
  ```

*Terminal-2*: For  RASA actions server

  ```bash
  # change to chatbot directory
  cd chatbot
  # run RASA actions server
  rasa run actions
  ```

*Terminal-3*:  For web application

  ```bash
  # change directory to webapp
  cd UI/Interactive-Voice-Response/backend
  # run web application server
  uvicorn app:app --reload --port 8000
  ```

  On successfully running these, commands you will be able to run the chatbot in your browser on the address **localhost:8000**.



## Other Resources

* Rasa official introduction: [Read Docs](https://rasa.com/docs/rasa/2.x/) 
* Rasa 2.x examples: [Learn Rasa programming via simple examples](https://github.com/RasaHQ/rasa-2.x-form-examples)
* Rasa chatbot examples: [Rasa chatbots](https://github.com/RasaHQ)
* If you have questions: [Rasa Community Forum](https://forum.rasa.com/)
