"""Main module."""
from utils import pdf_to_text, get_criteria
from llm import load_model, query, load_vectorstore, get_qarag_prompt

import typer
from rich.console import Console
from typing_extensions import Annotated

app = typer.Typer()
console = Console()

@app.command()
def review(content_file: Annotated[str, typer.Argument(help="Path to file containing the content to be reviewed")], criteria_file: Annotated[str, typer.Argument(help="Path to file containing the review criteria")], model_name: str = "mistral", temperature: float = 0.7, num_ctx: int = 4096):
    """Console script for review0 technical review functionality."""
    console.print("Review0: The baseline review tool")
    # Parse PDF
    text, text_highlight = pdf_to_text(content_file, [("Abstract", "Introduction")]) 
    #print(text, "\n----------------\n")
    #print(text_highlight, "\n----------------\n")
    # Get summary from the highlight using LLM
    if text_highlight != "":
        prompt = "Generate bullet point technical summary and assess scientific and business merit for the following proposal. Include main the challenges, strengths, weaknesses and potential risks."
        model = load_model(model_name, temperature, num_predict = 1024, num_ctx=num_ctx) 
        result = query(model, prompt + text_highlight)
    print(result.content)
    print("\n----------------\n\n")
    # Get list of questions
    #criteria_file = "../../data/criteria.txt"
    questions = get_criteria(criteria_file)
    # Get answers to questions using RAG
    vector_store, _ = load_vectorstore("nomic-embed-text", [content_file], [text]) 
    for question in questions:
        print("Question:", question)
        prompt = get_qarag_prompt(model_name, vector_store, "What is the " + question) 
        answer = model.invoke(prompt)
        print(answer.content)
        print("\n----------------\n")
    return

@app.command()
def revise(content_file: Annotated[str, typer.Argument(help="Path to file containing the content to be revised for language/grammer")], model_name: str = "mistral", temperature: float = 1, num_ctx: int = 4096):
    """Console script for review0 language revision functionality."""
    console.print("Review0: The baseline review tool")
    # Parse PDF
    text, _ = pdf_to_text(content_file) 
    # Get split texts from the document 
    _, all_splits = load_vectorstore("nomic-embed-text", [content_file], [text], chunk_size=4000, chunk_overlap=40) 
    #print(len(all_splits))
    # Iterate over splits and check language issues
    prompt = "Highlight major grammer issues and spelling errors in the following text and suggest corrections as a bullet list. Ignore whitespace, punctuation and capitilization errors." # any language issues
    model = load_model(model_name, temperature, num_predict = 512, num_ctx=num_ctx) 
    for text_split in all_splits:
        result = query(model, prompt + text_split.page_content)
        print(result.content)
        print("\n----------------\n\n")
    return

if __name__ == "__main__":
    app()

