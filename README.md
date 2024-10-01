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
* document_loader.py

#### 2.2.1. app.py
This code setups a simple web interface based on Flask that allows users to ask policy related questions and receive responses from the chatbot. The logic of the application for answering the questions has been designed in the *PoliciesChatbot* of the *chatbot.py* module. To get question answers, the app just calls the *run_step()* method of the *PoliciesChatbot* class.

#### 2.2.2. chatbot.py
This module implements the *PoliciesChabot* class in charge of running the main part of the backend of the application. The different methods of the class are explained below:
* **\_\_init\_\_ (self, policies, model)**: The class requires the path of the policy documents and the name of the model to be used. In this solution, "gpt-4o" model has been used.
* **run_step (self, question)**: This method implements a multi-step process to answer the user questions.
The solution to respond to user questions based on the information obtained from airline policy documents has been broken down into different steps, so the program tackles the problem gradually instead of trying to solve it all at once. By breaking the problem into smaller and simpler tasks, greater robustness and control over the responses provided by the LLM model have been achieved, thus avoiding unexpected answers and facilitating the identification of the point where the process may have failed.
The problem has been divided into the following steps (it is recommended to read the explanation along with the diagram provided in [Run Step Flowchart](./figures/run_step_flowchart.jpg) for greater clarity):
1. The system classifies the user's message to determine if it is a question related to airline policies or not. If it is, the next step is carried out. If not, a default response is provided to the user.
2. The system obtains the name of the airline the question is about. This way, the search for information can be conducted exclusively in the documents of that specific airline. If the name is obtained and belongs to one of the airlines for which information is available, the next step is carried out. If not, a default response is provided to the user.
3. The system analyzes the question to identify the document in which it is most likely to find the information from all those available. This document selection is performed by the LLM itself based on the document names and its reasoning about their content. If a document that may contain the information is found, the next step is carried out. If not, a default response is provided to the user.
4. The system analyzes the document in search of the information. Given that the input of the selected model, gpt-4, has a maximum limit of 128,000 tokens in the context window, the *split_string()* function has been implemented in the *document_loader.py* module to allow splitting the LLM input into smaller text chunks if necessary, enabling it to search for the information gradually within these chunks of text.
5. Finally, the system checks if the information could be obtained from the text. If so, the user is provided with the requested information. If not, step 4 is iterated over all the airline's existing documents until the information is found. If the information is not found after checking all the documents, a default response is given.
To carry out all these steps, the *run_step()* method utilizes the other methods defined in the class. 

* **get_is_policies_related(self,message)**: This method is used in step 1 to determine if the input is a question related to airline policies or not.

* **get_airline_name(self, question)**: This method is used in step 2 to obtain the airline name from the question.

* **get_necessary_document(self, question, airline)**: This method is used in step 3 to obtain the document name in which to look for the information.

* **get_info_from_document(self, question, airline, document)**: This method is used in step 4 to obtain the required information from the selected document.

* **answer_default(self, option)**: This method returns the different default answers.

#### 2.2.3. document_loader.py
This module provides functions to work with PDF and Markdown files, so that it returns the text in string variables that can be programmatically handled.

* **load_policies(policies_path, size, overlap)**: This functions receives the airline policies path, reads all the policy documents and returns the information into a dictionary. 

* **extract_text_from_pdf(pdf_path)**: This function receives a pdf path and returns the pdf text content into a string.

* **extract_text_from_markdown(md_path)**: This function receives a markdown file path and returns the markdown text content into a string.

* **split_string(text, size, overlap)**: This function splits a string into smaller substrings with a specified character overlap.


### 2.3. Challenges encountered
**Challenge**: Input length limit in the context window of the LLM when processing the policy documents.

**Solution**: Implement a function to split the text into smaller chunks.


**Challenge**: The system is unable to answer the question due to the complexity of the task.

**Solution**: Divide the problem into simpler tasks in which the uncertainty of the model's response is reduced.


**Challenge**: The user question is not well formulated.

**Solution**: Automation of default responses that help guide the user to rephrase the question to make it easier for the system to find the desired information.


**Challenge**: Unexpected responses from the system.

**Solution**: Limit the output of the LLM at the different steps to predefined response options, which facilitates the program's flow through if/else conditionals.


**Challenge**: Incorrect response from the system even after dividing the task into simpler tasks.

**Solution**: Guide the LLM's reasoning through a predefined chain of thoughts.


### 2.4. Future improvements
* Use embeddings and vector database techniques to improve the efficiency and execution speed of the application.



