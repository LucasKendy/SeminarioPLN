# -*- coding: utf-8 -*-
"""Cópia de SeminarioPLN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Q9VqlPz7LRLoUbqqah_zMUcD6a1bYYGT
"""

# --quiet suprime o output de texto, para manter o notebook mais legível
!pip install --quiet 'crewai==0.28.8'
!pip install --quiet 'crewai_tools==0.1.6'
!pip install --quiet 'langchain-community'
!pip install --quiet 'duckduckgo-search>=6.1.7'

from crewai_tools import FileReadTool, ScrapeWebsiteTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Cria a ferramenta a ser usada para buscar na internet
search_tool = DuckDuckGoSearchRun()
# Cria a ferramenta a ser usada para obter mais informações sobre um site em específico
scrape_tool = ScrapeWebsiteTool()

from crewai import Agent, Task, Crew
import os

os.environ['OPENAI_API_KEY'] = ''
os.environ['OPENAI_MODEL_NAME'] = 'gpt3.5-turbo'

gpt35 = ChatOpenAI(
  temperature=0.7,
  model_name="gpt-3.5-turbo",
)

# Cria um agente que vai buscar e reunir informações empresariais sobre a empresa a ser coberta.
# Define seu objetivo e backstory tal que possa atender à tarefa. O mesmo vai também ser feito para todos os outros agentes.
company_research_agent = Agent(
    role="Company Research Agent",
    goal="Gather detailed information about the target company, including their business, products, services, and market position.",
    backstory=(
        "Tasked with collecting comprehensive data about potential clients to inform the sales pitch."
    ),
    allow_delegation=True,
    verbose=True,
    llm=gpt35
)

# Define a tarefa esperada do agente, incluindo detalhamento sobre qual o output esperado.
# O mesmo vai também ser feito para todos os outros agentes.
company_research_task = Task(
    description=(
        "Collect comprehensive data about {company_name} from their website ({company_website}) and other sources. "
        "Include details about their business, products, services, and market position."
    ),
    expected_output=(
        "Detailed report on {company_name}'s business, products, services, and market position."
    ),
    agent=company_research_agent,
    tools=[search_tool, scrape_tool]
)

# Cria um agente que vai analisar com detalhe o website da empresa, buscand por melhoras possíveis.
website_analysis_agent = Agent(
    role="Website Analysis Agent",
    goal="Analyze the target company's website for areas of improvement, including design, performance, and user experience.",
    backstory=(
        "Focuses on identifying specific issues and opportunities for enhancement on the client's website."
    ),
    allow_delegation=True,
    verbose=True,
    llm=gpt35
)

# Define a tarefa esperada do agente, incluindo detalhamento sobre qual o output esperado.
website_analysis_task = Task(
    description=(
        "Analyze {company_name}'s website ({company_website}) to identify areas of improvement in design, performance, and user experience."
    ),
    expected_output=(
        "Detailed analysis report highlighting areas of improvement for {company_name}'s website, including design, performance, and user experience."
    ),
    agent=website_analysis_agent,
    tools=[scrape_tool, search_tool]
)

# Cria um agente que vai analisar o conteúdo do site, de um ponto de vista de marketing, buscando formas de melhorar engajamento e conversão.
content_strategy_agent = Agent(
    role="Content Strategy Agent",
    goal="Develop content strategies and identify how improved content can drive engagement and conversions.",
    backstory=(
        "Specializes in creating a compelling narrative and strategy for content improvements on the client's website."
    ),
    allow_delegation=True,
    verbose=True,
    llm=gpt35
)

# Define a tarefa esperada do agente, incluindo detalhamento sobre qual o output esperado.
content_strategy_task = Task(
    description=(
        "Develop a content strategy for {company_name}'s website ({company_website}) to enhance user engagement and conversion rates."
    ),
    expected_output=(
        "Comprehensive content strategy for {company_name}'s website, including recommendations for content improvements."
    ),
    agent=content_strategy_agent,
    tools=[search_tool, scrape_tool]
)

# Cria um agente que vai gerar um sales pitch ("discurso de vendas") usando as pesquisas dos outros agentes.
# Tem o intuito de convencer a companhia alvo que seu website precisa ser modificado com a nossa companhia "Code With Prince",
#  com base no que foi encontrado pelos demais agentes.
sales_pitch_agent = Agent(
    role="Sales Pitch Agent",
    goal="Create a personalized and persuasive sales pitch to convince the target company to have their website modified by 'Code With Prince'.",
    backstory=(
        "Combines research, analysis, and content strategy to craft a compelling sales pitch."
    ),
    allow_delegation=False,
    verbose=True,
    llm=gpt35
)

# Define a tarefa esperada do agente, incluindo detalhamento sobre qual o output esperado.
sales_pitch_task = Task(
    description=(
        "Combine the research, analysis, and content strategy to create a personalized and persuasive sales pitch for {company_name} "
        "to convince them to have their website modified by 'Code With Prince'."
    ),
    expected_output=(
        "Customized sales pitch for {company_name}, highlighting the benefits of having their website modified by 'Code With Prince'."
    ),
    agent=sales_pitch_agent,
    tools=[search_tool, scrape_tool]
)

# Inicializa a Crew (representa o grupo de agente, quais as tasks deles e como devem colaborar).
crew = Crew(
    agents=[
        company_research_agent,
        website_analysis_agent,
        content_strategy_agent,
        sales_pitch_agent
    ],
    tasks=[
        company_research_task,
        website_analysis_task,
        content_strategy_task,
        sales_pitch_task
    ],
    verbose=2,
    memory=True,
    cache=True,
    llm=gpt35
)

# Define a companhia alvo a ser analisada, e o seu site.
inputs = {
    "company_name": "CrewAI",
    "company_website": "https://crewai.com"
}

# Começa o trabalho da Crew.
result = crew.kickoff(inputs=inputs)

# Usa Markdown para mostrar a resposta gerada.
from IPython.display import Markdown

# Armazena o resultado em um arquivo.
with open("result.md", "w") as file:
    file.write(result)

Markdown(result)