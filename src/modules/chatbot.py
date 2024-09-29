"""
This module contains the main class of the application, a Chatbot to answer
the questions asked by the clients.
"""
from openai import OpenAI

class PoliciesChatbot:
    """
    """

    def __init__(self, policies, model="gpt-4o"):
        """
        Initializes an instance of the PoliciesChatbot class.

        This constructor sets up the chatbot with the provided policies and 
        model. It also initializes an OpenAI client for processing requests.

        Args:
        - policies (dict): A dictionary containing airline policies. The keys 
            represent airline names, and the values are nested dictionaries 
            with specific policy document names for each airline. The values
            for each document are also nested dictionaries with 'fulltext'
            (string with the complete file content) and 'slicedtext' (list 
            containing sliced chunks of the text with some characters
            overlapping) keys.
        - model (str, optional): The model identifier to use with the OpenAI 
            client (default is "gpt-4o").
        
        Attrs:
        - client (OpenAI): An instance of the OpenAI client used for 
            generating responses.
        - policies (dict): Stores the provided airline policies.
        - model (str): The model identifier used for processing responses.
        - airlines (list): A list of airline names extracted from the keys of 
            the 'policies' dictionary.
        """
        self.client = OpenAI()
        self.policies = policies
        self.model = model
        self.airlines = list(policies.keys())

    def run_step(self, question):
        """
        Executes a multi-step process to answer user questions related to 
        airline policies.

        This method follows a series of logical steps to determine whether a 
        given question is related to airline policies. If the question is 
        policy related, it then identifies the airline name, locates the 
        most appropiate policy document, and extracts the specific information 
        to answer the question. If any step fails, it provides a default 
        response based on the process step of the failure.

        Args:
        - question (str): Input message from the user.

        Returns
        - (str): Answer to the user's question. A default answer is provided
            if any step to obtain the information fails.
        """
        # 1. Is an airline policies related question?
        policies_related = self.get_is_policies_related(question)
        if policies_related == "True":
            # 2. Get airline name
            airline = self.get_airline_name(question)
            if airline in self.airlines:
                # 3. Get necessary document
                    document = self.get_necessary_document(
                                        question, airline)
                    if document in self.policies[airline]:
                        # 4. Look for the information to answer the question
                        info = self.get_info_from_document(
                                        question, airline, document)
                        # 5. Check if information was found successfully 
                        if info != "False":
                            # Yes --> Answer the question
                            return info
                        else:
                            # No --> Read the other documents
                            for document in self.policies[airline]:
                                info = self.get_info_from_document(
                                                question, airline, document)
                                if info != "False":
                                    # Yes --> Answer the question
                                    return info  
                            else: 
                                return(self.answer_default(4))
                    else:
                        return(self.answer_default(3))
            else:
                return(self.answer_default(2))

        else:
            return(self.answer_default(1))

    def get_is_policies_related(self,message):
        """
        Receives an input message and returns True or False depending if it 
        is a question airline policies related or not.

        Args:
        - message (str): Input message from the user.

        Returns:
        - (str): "True" if the messafe is a question related to airline flight
            policies, "False" if not. 
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                "role": "system", 
                "content": 
                    """
                    Act as if you are the foremost expert in airline flight 
                    policy assistance. I will provide you with messages from 
                    airport customers. Your task is to determine if the 
                    message is a question related to an airline policy or not. 
                    To do this, perform the following actions:

                    1. Analyze the content of the message in great detail.
                    2. Identify if it is a question or not. If it is not a 
                    question, the message can be discarded.
                    3. If it is a question, identify whether it is related to
                    something that could be asked at an airport or about an 
                    airline's flight policy, or if it is unrelated. If it is 
                    unrelated, the message can be discarded.
                    Finally, identify if the question specifically relates to 
                    an airline flight policy, or if it could be another type 
                    of question typically asked at an airport.
                    4. If it is not specifically related to an airline flight 
                    policy, discard the message, even if it is related to 
                    other airport matters.

                    The output you should provide must be one of these options:
                    - If it is a question related to an airline's flight 
                    policy: Only "True".
                    - If any other case, only answer "False".
                    """
                },
                {
                    "role": "user",
                    "content": 
                            f"""
                            <Message>: "{message}".
                            """
                }
            ]
        )
        return completion.choices[0].message.content

    def get_airline_name(self, question):
        """
        Receives an input message that is an airline policies related 
        question. Tries to obtain the name of the airline the question
        is about.

        Args: 
        - question (str): Input message from the user with a question 
            related to airline policies.

        Returns:
        - (str): Name of the airline if it was identified in the question,
            "None" in any other case.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                "role": "system", 
                "content": 
                    f"""
                    Act as if you are the foremost expert in airline flight 
                    policy assistance. I will now write questions related to 
                    airline flight policies. These questions are made by 
                    customers at an airport. Your task is to obtain the name 
                    of the airline mentioned in the question. To do this, 
                    follow these steps:

                    1. Analyze the content of the question in great detail.
                    2. dentify the name of the airline.
                    3. If it is an airline from this list 
                    {list(self.policies.keys())}, format the airline's name exactly 
                    as it appears in the list.
                    4. Finally, return the name of the airline.

                    The output you should provide must be one of these options:
                    - Only "None" if the airline's name was not identified.
                    - Only the name of the airline if it has been identified.
                    """ 
                },
                {
                    "role": "user",
                    "content": 
                            f"""
                            <Question>: "{question}".
                            """
                }
            ]
        )
        return completion.choices[0].message.content

    def get_necessary_document(self, question, airline):
        """
        Receives an input message that is an airline policies related 
        question and the name of the airline the question is about. Tries to 
        select the most appropiate document to obtain the information asked 
        in the question.

        Args:
        - question(str): Input message from the user with a question 
            related to airline policies.
        - airline (str): Name of the airline the question is about.

        Returns:
        - (str): Name of the most appropiate airline policy document to look 
            for the information asked in the question.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                "role": "system", 
                "content": 
                    f"""
                    Act as if you are the foremost expert in airline flight 
                    policy assistance. I will now write questions related to 
                    airline flight policies. These questions are made by 
                    customers at an airport. Your task is to obtain the name 
                    of the most appropriate document in which to search for 
                    the information to answer the question, from a list of 
                    documents that I will provide you. To do this, follow 
                    these steps:

                    1. Analyze the content of the question in great detail.
                    2. Create a list of topics into which the question can be 
                    classified.
                    3. Analyze the list of documents I provide.
                    4. Create a list of topics that each of these documents might 
                    contain.
                    5. Select the document from the list that you consider most 
                    likely to contain the answer to the question.
                    6. Finally, return the name of the document exactly as it 
                    appears in the list.

                    The output you should provide must be only the name of the 
                    document you have selected.
                    """ 
                },
                {
                    "role": "user",
                    "content": 
                            f"""
                            <Question>: "{question}".
                            <List of documents>: "{list(self.policies[airline].keys())}"
                            """
                }
            ]
        )
        return completion.choices[0].message.content

    def get_info_from_document(self, question, airline, document):
        """
        Receives an input message that is an airline policies related 
        question, the name of the airline the question is about and the 
        document in which to look for the information. Tries to obtain the 
        necessary information from the document to answer the question.

        Args:
        - question (str): Input message from the user with a question 
            related to airline policies.
        - airline (str): Name of the airline the question is about.
        - document (str): Name of the document in which to look for the 
            information asked in the question.

        Returns:
        - (str): Answer with the information asked in the question if the
            information was found in the document, "False" if the information 
            was not found.
        """
        for text in self.policies[airline][document]['slicedtext']:

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                    "role": "system", 
                    "content": 
                        f"""
                        Act as if you are the foremost expert in airline 
                        flight policy assistance. I will now provide you with 
                        a question related to airline flight policies and a 
                        text in which you can search for the information to 
                        answer that question. These questions are made by 
                        customers at an airport. Your task is to obtain the 
                        answer to that question in a clear and precise manner. 
                        To do this, follow these steps:

                        1. Analyze the content of the question in great detail.
                        2. Analyze the content of the text with the information
                        in great detail.
                        3. Search for keywords that link the question to the 
                        information in the text.
                        4. If you find the necessary information, formulate a 
                        clear and precise answer to respond to the question.

                        The output you should provide must be one of these two 
                        options:

                        - If you have found the necessary information: Respond
                        with the answer to the question that you formulated in 
                        step 4.
                        - If you have not found the necessary information: 
                        Simply respond with "False".
                        """ 
                    },
                    {
                        "role": "user",
                        "content": 
                                f"""
                                <Question>: "{question}".
                                <Text with information>: "{text}"
                                """
                    }
                ]
            )
            
            if completion.choices[0].message.content == "False":
                pass
            else:
                return completion.choices[0].message.content
        return "False"
        
    def answer_default(self, option):
        """
        This method receives an option number and returns default answer for 
        each option.

        Args:
        - option (int): Number to select the answer option.

        Returns:
        - answer (str): String with the selected default answer.
        """
        if   option == 1:
            answer = """
                I'm very sorry, but I can only answer questions related to 
                airline flight policies. Please, ask me a question.
                """

        elif option == 2:
            answer = f"""
                I'm very sorry, but I couldn't identify the airline name in 
                your question or I don't have information abut this specific 
                airline. Try again specifying one of this airline names in 
                your question: 
                "{self.airlines_string}".
                """

        elif option == 3:
            answer = (
                """
                Sorry, I couldn't find the airline policies document with 
                the requested information, try again specifying more in detail
                the necessity of your question.
                """)

        elif option == 4:
            answer = (
                """
                Sorry, I couldn't find the information your requested, try 
                again specifying more in detail your necessity or rephrase
                your question.
                """)
        
        return answer