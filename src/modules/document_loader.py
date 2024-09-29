"""
This module contains some util functions to work with pdf and markdown 
documents.
"""

import os
import logging
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    This function receives a pdf path, reads it and returns the pdf 
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
    This function receives a markdown file path, reads it and returns the 
    markdown text content into a string.

    Args: 
    - md_path (str): String with the markdown file path to be read.

    Returns:
    - text (str): String with the content of the markdown file.
    """
    with open(md_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def load_policies(policies_path):
    """
    This functions receives the airline policies path, reads all the
    policies documents and returns the information into a dictionary
    with the following format:

    Args:
    - policies_path (str): String with the directory path where the policy 
        documents are stored.
    
    Returns:
    - policies (dict): Dictionary in which the keys are the airline names, 
        classifying the policy documents by airline. Each airline is a 
        dictionary itself too, in which the keys are the document names.
        Finally, each document is also a dictionary with the keys 'fulltext'
        and 'slicedtext'. Full text is a string with all the file content, and
        sliced text is a list containing sliced chunks of the text with some
        overlapping, to ease providing that text as smaller inputs to the LLM
        model.
        This is a schema of the policies dictionary format:

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
            sliced_text = split_string(text, 2000, 200)
            policies[airline][file]['slicedtext'] = sliced_text

            logging.debug(f"Airline: {airline:<20.20}, File: {file:<40.40}, FileLen: {len(text):>10}")

    return policies

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
