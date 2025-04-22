Review 0
========

AI-assisted rassessment of project proposals and technical documentation using local LLMs

Table of Contents
-----------------

- [Introduction](#introduction)

- [Requirements](#requirements)

- [Features](#features)

- [Installation](#installation)

- [Usage](#usage)

    - [Reviewer mode](#reviewer-mode)

    - [Reviser mode](#reviser-mode)

- [Examples](#examples)

    - [Technical review](#technical-review)

    - [Language revision](#language-revision)

- [TODO](#todo)

- [Related work](#related-work)

- [License](#license)

Introduction
------------

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

The code was tested using various Ollama models (such as mistral, openchat, gemma3, etc.) on a MacBook Air M1 chip with 8GB RAM. The default num_ctx parameter set to 4096 to enable runs without the need of swap memory usage.

> _Disclaimer: It is important to note that the output produced by the LLMs is not always correct and should be fact-checked by the user._


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
- Language revision (potential grammer and spelling issues)
- _(under development)_ Customizable prompts 


Installation
------------

To install the code as a python package run the following inside the directory containing the repository:

`python -m pip install .`

See usage below to run it on the command line. To use the functions inside the python:

```python
from review0 import llm
model = llm.load_model(model_name="mistral", temperature=1, num_predict = 512, num_ctx=2048)
result = llm.query(model, "What is the answer to the life and universe?")
print(result.content)
```


Usage
-----

### Reviewer mode 

**Technical review of the content based on the criteria provided**

> See `python main.py review --help` for usage information.
 

`python main.py review --model-name <llm_model(default:mistral)> --temperature <llm_temperature(default:0.7)> --num_ctx <llm_context_window_size(default:4096)> <path_to_content_file(pdf)> <path_to_criteria_file_in(txt)>`


### Reviser mode 

**Language revision to highlight issues and suggest corrections** 


> See `python main.py revise --help` for usage information.

`python main.py revise --model-name <llm_model(default:mistral)> --temperature <llm_temperature(default:1)> --num_ctx <llm_context_window_size(default:4096)> <path_to_content_file(pdf)>`


Examples
--------

### Technical review 

The following can be used to analyze test.pdf using the report criteria (under data folder) with default parameters (model, temprature, and context window size):

`python main.py ../../data/test.pdf ../../data/criteria_report.txt`

This would produce a summary based on the abstract (i.e., highlight text) followed by an assessment of provided in the criteria file. An excerpt from the output for the example file is as follows.

```
    **Technical Summary:**

    - The study investigates the gene expression of peripheral immune cells in five pediatric patients with Pediatric Acute-onset Neuropsychiatric Syndrome (PANS) using single-cell RNA sequencing.
    - The study compares the pre- and post-treatment immune profiles of these patients with open-label intravenous immunoglobulin (IVIg) therapy, and four neurotypical controls.
    - The research aims to understand the potential epigenetic and immune dysregulation in PANS and suggests that IVIg may play a critical role in its treatment.

    ...

    **Challenges:**

    - The small sample size may limit the generalizability of the findings to a larger population of PANS patients.
    - The study's reliance on self-reported data for some symptoms (e.g., eating restriction, developmental regression) could introduce bias.
    - The lack of long-term follow-up data makes it difficult to assess the lasting effects of IVIg therapy on PANS patients.

    ...

    **Weaknesses:**

    - The lack of a control group that did not receive IVIg therapy makes it difficult to definitively attribute any observed changes to the treatment itself.
    - The study's cross-sectional design limits its ability to establish causality between the observed immune changes and PANS symptoms.
    - The use of preprints as the primary source of information may limit the credibility of the findings until they are peer-reviewed and published in a scientific journal.

    ...

    ----------------


    Question:  Main contribution of the report
    The main contribution of the report focuses on the analysis of gene expression in Neutrophils, B cells, T cells, Monocytes, and NK cells before and after IVIg treatment in PANS (Pediatric Autoimmune Neuropsychiatric Syndromes) patients. The study highlights five upregulated GO pathways in neutrophils, including immune response to bacterium, regulation of cytokine production, and neutrophil chemotaxis, as well as three downregulated ribosomal/translation pathways. The findings suggest that IVIg treatment may alter the immune response in PANS patients by modulating these specific pathways ([doi:10.1101/2025.03.27.25324808](https://doi.org/10.1101/2025.03.27.25324808)).

    ----------------

    Question:  Novelty of the scientific approach

    ...
```

### Language revision 

The following can be used to analyze test.pdf with default parameters (model, temprature, and context window size):

`python main.py revise ../../data/test.pdf`

This would produce a list of potential issues for the chunks of the text. An excerpt from the output for the example file is as follows.

````
    ...

    1. "PANS event occurred age 1.8–13 years" should be "The PANS event occurred between the ages of 1.8 and 13."
    2. "62 (n=5), developmental regression (n=4)" should be "(n=5) for eating restriction, developmental regression (n=4)."
    3. "In 65 PANS pre-IVIg compared to neurotypical controls" should be "Compared to neurotypical controls, in the pre-IVIg stage of PANS,"
    4. "In PANS pre-IVIg compared to controls, ribosomal pathways were upregulated in neutrophils and CD8 T cells, but downregulated in NK cells" should be "Ribosomal pathways were upregulated in neutrophils and CD8 T cells, and downregulated in NK cells in PANS pre-IVIg compared to controls."
    5. "Post-IVIg, the previously downregulated immune pathways were upregulated in most cell types" should be "After IVIg, the previously downregulated immune pathways were upregulated in most cell types."
    6. "histone modification pathways (histone methyltransferase, chromatin)" should be "histone modification pathways, specifically histone methyltransferase and chromatin."
    7. "We propose PANS is an epigenetic immune-brain disorder with cellular epigenetic, ribosomal, and immune dysregulation" should be "We propose that PANS is an epigenetic immune-brain disorder characterized by cellular epigenetic, ribosomal, and immune dysregulation."
    8. "Therefore, epigenetic and immune-modulating therapies, such as IVIg, may have a critical role in treating this disabling disorder" should be "Thus, epigenetic and immune-modulating therapies, including IVIg, could play a crucial role in managing this debilitating condition."
    9. "Introduction" should be capitalized to "Introduction".
    10. "Paediatric acute-onset neuropsychiatric syndrome (PANS)" should be "Pediatric Acute-Onset Neuro
    
    ----------------
    ...
````


TODO
----
- Extract model params (temp, num_ctx) / prompts as config files (yaml)
- Generate documentation from docstrings
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