"""Utility functions for review0."""
from pypdf import PdfReader


def pdf_to_text(filename, highlight_headers=[]):
    """
    Extract text from a PDF file and return both the full text and the highlight 
    that includes certain sections if provided. 
    This function reads a PDF file, extracts its text content, and optionally
    extracts and highlights specific sections of the text based on provided
    header pairs.
    Args:
        filename (str): The path to the PDF file to be processed.
        highlight_headers (list of tuple, optional): A list of tuples where each tuple
            contains two strings representing the start and end headers of the sections
            to be highlighted. Defaults to an empty list.
    Returns:
        tuple:
            - str: The full extracted text from the PDF.
            - str: The concatenated text of the highlighted sections, if any.
    Notes:
        - If a section defined by the start and end headers is not found in the text,
          a message will be printed indicating the missed section and its headers.
        - The function assumes that the headers provided in `highlight_headers` are
          unique and appear in the text in the correct order.
    Example:
        text, text_highlight = pdf_to_text("example.pdf", [("Abstract", "Introduction"), ("Conclusion", "References")])
    """
    reader = PdfReader(filename)
    text = ""
    text_highlight = ""
    # Get text from PDF
    for i, page in enumerate(reader.pages):
        txt = page.extract_text() 
        text += txt + "\n"
    # Get text highlight including only the parts that match certain section name pairs
    for start, end in highlight_headers: 
        i_s = text.find(start)
        i_e = text.find(end)
        if i_s != -1 and i_e != -1:
            text_highlight += text[i_s:i_e]
        else:
            print("=====> Missed section:", start, i_s, end, i_e)
    return text, text_highlight

def get_criteria(filename):
    """
    Reads a file and extracts a list of questions by filtering out headers 
    and empty lines.

    Args:
        filename (str): The path to the file containing the questions.

    Returns:
        list: A list of strings, where each string is a question extracted 
        from the file.
    """
    questions = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip().strip("\n")
            if line == "" or line.startswith("**"): # Skip headers
                continue
            questions.append(line.strip("*"))
    return questions