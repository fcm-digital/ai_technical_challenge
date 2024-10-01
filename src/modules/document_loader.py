"""
This module provides functions to work with PDF and Markdown files, so that 
it returns the text in string variables that can be programmatically handled.
"""

import os
import logging
import PyPDF2

def load_policies(policies_path, size, overlap):
    """
    This functions receives the airline policies path, reads all the
    policy documents and returns the information into a dictionary
    with the following format:

    Args:
    - policies_path (str): String with the directory path where the policy 
        documents are stored.
    - size (int): The size of each substring into which the total text of each
        document is split.
    - overlap (int): The number of characters that overlap between 
        consecutive substrings in each document when split.
    
    Returns:
    - policies (dict): A dictionary containing airline policies. The keys 
            represent airline names, and the values are nested dictionaries 
            with specific policy document names for each airline. The values
            for each document are also nested dictionaries with 'fulltext'
            (string with the complete file content) and 'slicedtext' (list 
            containing sliced chunks of the text with some characters
            overlapping) keys.

            This is an example schema of the policies dictionary format:

                policies{
                    airline_1{
                        document_1{
                            'fulltext': (str)
                            'slicedtext': (list)
                        },
                        document_2{
                            ...
                        },
                        ...
                    },
                    airline_2{
                        ...
                    },
                    ...
                }
    """
    policies = {}
    for airline in os.listdir(policies_path):
        if os.path.isdir(os.path.join(policies_path, airline)):
            policies[airline] = {}

    for root, dirs, files in os.walk(policies_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            elif file.endswith('.md'):
                text = extract_text_from_markdown(file_path)
            else:
                continue
            
            airline = root.split('/')[-1]
            policies[airline][file] = {}
            policies[airline][file]['fulltext'] = text
            sliced_text = split_string(text, size, overlap)
            policies[airline][file]['slicedtext'] = sliced_text

            logging.debug(f"Airline: {airline:<20.20}, File: {file:<40.40}, FileLen: {len(text):>10}")

    return policies

def extract_text_from_pdf(pdf_path):
    """
    This function receives a pdf path and returns the pdf 
    text content into a string.

    Args: 
    - pdf_path (str): String with the pdf file path to be read.

    Returns: 
    - text (str): String with the content of the pdf file.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_markdown(md_path):
    """
    This function receives a markdown file path and returns the 
    markdown text content into a string.

    Args: 
    - md_path (str): String with the markdown file path to be read.

    Returns:
    - text (str): String with the content of the markdown file.
    """
    with open(md_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def split_string(text, size, overlap):
    """
    Splits a string into smaller substrings with a specified character 
    overlap.

    Args:
    - text (str): The string to be split.
    - size (int): The size of each substring.
    - overlap (int): The number of characters that overlap between 
        consecutive substrings.

    Returns:
    - substrings (list): A list of resulting substrings.
    """
    if size <= 0:
        raise ValueError("Size must be a positive integer.")
    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")
    if overlap >= size:
        raise ValueError("Overlap must be less than the size of the substrings.")

    substrings = []
    step = size - overlap
    index = 0

    while index < len(text):
        end = index + size
        substring = text[index:end]
        substrings.append(substring)
        index += step

    return substrings
