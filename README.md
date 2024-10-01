# AI Technical Challenge Solution

## 1. Setup and Deployment
### 1.1. Python version requirements
This application has been developed using Python 3.8.10, so it is recommended to use the same Python version.
### 1.2. How to set up the application
1. Create a Python virtual environment and activate it:
> python3 -m venv ai_venv

> source ai_venv/bin/activate
2. Clone this repository and move to the root path of the repository:
> git clone git@github.com:AlejandroDiazD/ai_technical_challenge.git

> cd ai_technical_challenge
3. Install Python requirements:
> python3 -m pip install -r requirements.txt

### 1.1. How to run the application
1. Run the app:
> python3 src/app.py
2. Open a web browser and search the following URL:
> http://127.0.0.1:5000/
3. Use the chat to ask questions and then automatically receive answers.

## 2. Design explanation
### 2.1. Technologies used
The solution has been based on a Flask local server for the web interface and on OpenAI API for the backend of the application.

**Flask** is a slim web framework, and has been used to develop the web interface due to its ease of use and quick setup, allowing a quick development and deployment of the interface as the focus of the challenge is on the backend of the application.

**OpenAI API** has been used to develop the backend of the application in charge of answering user questions. It has been selected because it already provides pre-trained LLM models and because it was recommended in the challenge description.

**PyPDF2** is an open-source Python module that has been used to read airline policy PDF documents and transform them into string variables that can be programmatically managed by the application.

### 2.2. Code structure and explanation
The code is in the */src* directory of the repository, and it is structured into a main file *app.py* that runs the Flask server making use of the *PoliciesChatbot* class defined in *chatbot.py* module to run the backend and answer the user questions. The *PoliciesChatbot* class makes use of the functions defined in the other module *document_loader.py* for reading PDF and Markdown documents.
The different parts of the code are explained in next sections. It is recommended to read the explanations along with the code:
* app.py
* chatbot.py
* document\_loader.py

#### app.py
This code setups a simple web interface based on Flask that allows users to ask policy related questions and receive responses from the chatbot. The logic of the application for answering the questions has been designed in the *PoliciesChatbot* of the *chatbot.py* module. To get question answers, the app just calls the *run_step()* method of the *PoliciesChatbot* class.

#### chatbot.py
This module implements the *PoliciesChabot* class in charge of running the backend of the application. The different methods of the class are explained below:
* **\_\_init\_\_ (self, policies, model)**: The class requires the path of the policy documents and the name of the model to be used. In this solution, "gpt-4o" model has been used.
* **run_step (self, question)**: This method implements a multi-step process to answer the user questions. In each step, different conditions are checked  

#### document_loader.py



### 2.3. Challenges encountered
**Challenge**: 
**Solution**: 


**Challenge**: 
**Solution**: 



