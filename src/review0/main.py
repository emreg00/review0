"""Main module."""
from utils import pdf_to_text, get_criteria
from llm import load_model, query, load_vectorstore, get_qarag_prompt

import typer
from rich.console import Console
from typing_extensions import Annotated

app = typer.Typer()
console = Console()

@app.command()
def main(content_file: Annotated[str, typer.Argument(help="Path to file containing the content to be reviewed")], criteria_file: Annotated[str, typer.Argument(help="Path to file containing the review criteria")], model_name: str = "mistral", temperature: float = 0.7):
    """Console script for review0."""
    console.print("Review0: The baseline review tool")
    #model_name = "mistral" # "gemma3" "openchat"
    #temperature = 0.8 # 1 #0.1
    #content_file = "../../data/test2.pdf"
    # Parse PDF
    text, text_highlight = pdf_to_text(content_file, [("Abstract", "Introduction")]) 
    #print(text, "\n----------------\n")
    print(text_highlight, "\n----------------\n")
    # Get summary from the highlight using LLM
    if text_highlight != "":
        prompt = "Generate bullet point technical summary and assess scientific and business merit for the following proposal. Include main the challenges, strengths, weaknesses and potential risks."
        model = load_model(model_name, temperature, num_predict = 1024, num_ctx=4096) 
        result = query(model, prompt + text_highlight)
    print(result.content)
    print("\n----------------\n\n")
    # Get list of questions
    #criteria_file = "../../data/criteria.txt"
    questions = get_criteria(criteria_file)
    # Get answers to questions using RAG
    vector_store = load_vectorstore("nomic-embed-text", [content_file], [text]) 
    for question in questions:
        print("Question:", question)
        prompt = get_qarag_prompt(model_name, vector_store, "What is the " + question) 
        answer = model.invoke(prompt)
        print(answer.content)
        print("\n----------------\n")
    return


if __name__ == "__main__":
    app()

