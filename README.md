<h1 align="center">AI Powered Regulatory Compliance Platform</h1>
<p align="center">Automated AI-powered legal contract analysis for regulatory adherence.</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

## 📖 Table of Contents
- [⭐ Overview](#-overview)
- [🛠️ Tech Stack & Architecture](#️-tech-stack--architecture)
- [✨ Prerequisites](#-Prerequisites)
- [🚀 Steps](#steps)
- [🔧 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

## ⭐ Overview

AI Powered Regulatory Compliance Checker is an innovative open-source project designed to revolutionize regulatory compliance checking for legal contracts by leveraging advanced AI and semantic search capabilities.

> **The Problem:** Manually reviewing legal contracts for regulatory compliance is a labor-intensive, time-consuming, and error-prone process. It demands extensive legal expertise and can lead to significant delays, increased operational costs, and potential non-compliance risks due to human oversight.

**The Solution:** This project provides an elegant solution by automating the contract analysis workflow. It intelligently extracts relevant information, performs semantic comparisons against regulatory guidelines, and generates comprehensive "suitability reports" that highlight compliance or non-compliance areas, significantly reducing manual effort and enhancing accuracy.

**Inferred Architecture:**
This project is primarily a Python-based application, featuring a robust web API (built with FastAPI) for interaction. At its core, it integrates Large Language Models (LLMs) for intelligent text synthesis and analysis, complemented by a vector database (PostgreSQL with Timescale Vector) for efficient semantic search and retrieval-augmented generation (RAG). The application is containerized using Docker and Docker Compose for easy deployment and management. A critical component of its design is the deep integration with Langfuse, an open-source LLM observability platform, used for prompt management, tracing LLM interactions, and monitoring performance. The system is designed to ingest legal documents, process them, query relevant regulations, and generate detailed, human-readable compliance reports.

## 🛠️ Tech Stack & Architecture

| Technology                  | Purpose                                        | Why it was Chosen                                                                      |
| :-------------------------- | :--------------------------------------------- | :------------------------------------------------------------------------------------- |
| **Python**                  | Primary programming language                   | Versatility, rich ecosystem for AI/ML, and strong community support.                   |
| **FastAPI**                 | Web API Framework                              | High performance, async support, automatic API documentation (Swagger UI/ReDoc).     |
| **PostgreSQL + Timescale Vector** | Relational & Vector Database                   | Robust, scalable, excellent for structured data, and efficient similarity search with `pgvector` or `timescaledb-toolkit`. |
| **Langfuse**                | LLM Observability & Prompt Management          | Comprehensive tracking, monitoring, and optimization of LLM applications.            |
| **Pandas**                  | Data manipulation & analysis                   | Powerful and flexible for handling tabular data, essential for preprocessing and post-processing. |
| **OpenAI, Hugging Face, Groq** | Large Language Models (LLMs)                   | Access to state-of-the-art generative AI capabilities for text understanding and synthesis. |
| **Docker & Docker Compose** | Containerization & Orchestration               | Ensures consistent development and production environments, simplifies deployment.    |
| **PDF Extraction Library**  | Extracts text from PDF documents (Inferred)    | Enables processing of unstructured text from legal documents.                          |

## ✨Prerequisites

- Docker
- Python 3.12+
- OpenAI API key
- PostgreSQL GUI client

## 🚀Steps

1. Set up Docker environment
2. Connect to the database using a PostgreSQL GUI client (I use TablePlus)
3. Create a Python script to insert document chunks as vectors using OpenAI embeddings
4. Create a Python function to perform similarity search

## Detailed Instructions

### 1. Set up Docker environment

Create a `docker-compose.yml` file with the following content:

```yaml
services:
  timescaledb:
    image: timescale/timescaledb-ha:pg16
    container_name: timescaledb
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - timescaledb_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  timescaledb_data:
```

Run the Docker container:

```bash
docker compose up -d
```

### 2. Connect to the database using a PostgreSQL GUI client

- Open client
- Create a new connection with the following details:
  - Host: localhost
  - Port: 5433
  - User: postgres
  - Password: password
  - Database: postgres

### 3. Create a Python script to insert document chunks as vectors

See `insert_vectors.py` for the implementation. This script uses OpenAI's `text-embedding-3-small` model to generate embeddings.

### 4. Create a Python function to perform similarity search

See `similarity_search.py` for the implementation. This script also uses OpenAI's `text-embedding-3-small` model for query embedding.

## 🔧Usage

1. Create a copy of `example.env` and rename it to `.env`
2. Open `.env` and fill in your OpenAI API key. Leave the database settings as is
3. Run the Docker container
4. Install the required Python packages using `pip install -r requirements.txt`
5. Execute `insert_vectors.py` to populate the database with your dataset
6. Play with `similarity_search.py` to perform similarity searches or use app/main.py


## Key Features

- **AI-Driven Analysis**: Uses openAI to generate embeddings and perform similarity searches on stored contract data.
- **Comprehensive Reporting**: Provides a compliance score out of 100, highlights strengths and weaknesses, and explains the evaluation process.
- **Efficient Storage**: Stores embeddings, summaries, and metadata of 150+ contracts in Dockerized PostgreSQL for fast and reliable retrieval.
- **User-Friendly Interface**: Built with Streamlit, offering an intuitive experience for uploading contracts (PDF) and viewing detailed reports.
- **Cosine Similarity**: Utilized for similarity searches to compare uploaded contracts with existing data.

## Technology Stack

- **Frontend**: FAST API keys
- **Machine Learning**: openAI(3.5 turbo, 4o-mini) for embeddings and analysis
- **Backend**: Dockerized PostgreSQL
- **Similarity Search**: Cosine similarity algorithm
- **Programming Language**: Python

## How It Works

1. **Upload a Contract**: Users can upload contracts in PDF format.
2. **AI Analysis**: Legiscan runs a similarity search on stored embeddings to analyze the uploaded contract.
3. **Detailed Report**: The tool generates a report with:
   - A compliance score out of 100
   - Strengths and weaknesses of the contract
   - An explanation of the analysis process

## Installation

Follow these steps to set up compliance checker on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/legiscan.git
   cd legiscan
   ```

2. **Set Up the Environment**:
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run Docker**:
   - Ensure Docker is installed and running on your machine.
   - Start the PostgreSQL container:
     ```bash
     docker-compose up
     ```

4. **Start the Application**:
   ```bash
   uvicorn api.main:app --reload
   ```

5. **Access the App**:
   - Open your browser and go to `http://127.0.0.1:8000/docs`.

## Usage

- Upload a contract in PDF format.
- Wait for the analysis to complete.
- Download the detailed compliance report.

## Contribution

We welcome contributions! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or feedback, please reach out at andaazmoun@gmail.com
