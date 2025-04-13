Review 0
========

AI-assisted rassessment of project proposals and technical documentation using local LLMs

Summary
-------
This project aims to support review of grant proposals and scientific articles using LLMs  
putting an emphasis on using local resources such as quantized Ollama models. It does not aim to replace 
the reviewer but help her/him by providing an overview and highlighting potential strengths and weaknesses.
By not sharing the data with external services, it also aims to protect the confidentiality policies 
typically imposed by institutions and also provides an environmentally friendly alternative to more resources
demanding models hosted on the cloud.

Given a PDF file and list of questions, the code will parse the PDF file, extract the text, split it into chunks,
generate a vectorstore and then use a local LLM to answer the questions in a concise manner referring to the 
original source whenever possible in a RAG setting. A list of default questions are provided to assess
a project proposal (i.e., novelty, need, feasibility, IP, value proposition, competition, impact, etc.) and
a technical report (i.e., logical flow, methodological soundness, reporting of statistical tests and associated metrics, 
availability of data supporting claims etc.).

The code was tested using various Ollama models (such as mistral, openchat, gemma3, etc.) on a MacBook Air M1 chip with 8GB RAM.

_Disclaimer: It is important to note that the output produced by the LLMs is not always correct and should be fact-checked by the user._

Requirements
------------
- Python 3.8 or higher
- [Langchain](https://python.langchain.com/) and [langchain-ollama](https://python.langchain.com/docs/integrations/chat/ollama/)
- [Numpy](https://numpy.org/)
- [Pypdf](https://pypi.org/project/pypdf/)
- [Typer](https://typer.tiangolo.com/)
- [Ollama](https://ollama.com/)
- At least one model from ollama for QA task and "nomic-embed-text" model for creating embeddings from the text (to create the document store for RAG)

To install the requirements & dependencies, the use of an virtual environment manager (such as [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html) or [conda/miniconda](/docs/getting-started/miniconda/main#should-i-install-miniconda-or-anaconda-distribution)) is recommended. 

On Mac OS [homebrew](https://brew.sh/) package manager can be used to install dependencies.  
```shell
$ brew install ollama
$ brew services start ollama
$ ollama pull mistral
```


Features
--------
- PDF parsing
- Text chunking
- Vectorstore generation
- Local LLMs of choice (through Ollama)
- Question answering using RAG (retrieval-augmented generation)
- Default questions & prompts for project proposals and technical reports
- _(under development)_ Customizable prompts 

Usage
-----
`python main.py --model-name <llm_model(default:mistral)> --temperature <llm_temperature(default:0.7)> <path_to_content_file(pdf)> <path_to_criteria_file_in(txt)>`

Example code to analyze test.pdf using the report criteria (under data folder) with default parameters (model and temprature)
`python main.py ../../data/test.pdf ../../data/criteria_report.txt`

TODO
----
- Extract params / prompts as config files (yaml)
- Generate docs
- Add more tests and tox for different python versions
- Consider supporting PDF parse figures & checkboxes
- Consider supporting for additional (non-PDF) formats


Related work
------------
- [LLM4SR: A Survey on Large Language Models for Scientific Research](https://github.com/du-nlp-lab/LLM4SR?tab=readme-ov-file#llms-for-peer-reviewing)
- [What Can Natural Language Processing Do for Peer Review?](https://arxiv.org/html/2405.06563v1)
- [AgentReview: Exploring Peer Review Dynamics with LLM Agents](https://arxiv.org/abs/2406.12708v2)
- [AgentRxiv: Towards Collaborative Autonomous Research](https://agentrxiv.github.io/)
- [The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](https://arxiv.org/abs/2408.06292)
- [Reviewer2: Optimizing Review Generation Through Prompt Generation](https://arxiv.org/abs/2402.10886)


License
-------
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.