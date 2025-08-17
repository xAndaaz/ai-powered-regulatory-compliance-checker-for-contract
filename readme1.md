<h1 align="center">xAndaaz AI: Regulatory Compliance Platform</h1>
<p align="center">Automated AI-powered legal contract analysis for regulatory adherence.</p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge">
  <img alt="Issues" src="https://img.shields.io/badge/Issues-0%20Open-blue?style=for-the-badge">
  <img alt="Contributions" src="https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>
<!--
  **Note:** These are static placeholder badges. Replace them with your project's actual badges.
  You can generate your own at https://shields.io
-->

## 📖 Table of Contents
- [⭐ Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack & Architecture](#️-tech-stack--architecture)
- [🚀 Getting Started](#-getting-started)
- [🔧 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

## ⭐ Overview

xAndaaz AI is an innovative open-source project designed to revolutionize regulatory compliance checking for legal contracts by leveraging advanced AI and semantic search capabilities.

> **The Problem:** Manually reviewing legal contracts for regulatory compliance is a labor-intensive, time-consuming, and error-prone process. It demands extensive legal expertise and can lead to significant delays, increased operational costs, and potential non-compliance risks due to human oversight.

**The Solution:** xAndaaz AI provides an elegant solution by automating the contract analysis workflow. It intelligently extracts relevant information, performs semantic comparisons against regulatory guidelines, and generates comprehensive "suitability reports" that highlight compliance or non-compliance areas, significantly reducing manual effort and enhancing accuracy.

**Inferred Architecture:**
This project is primarily a Python-based application, featuring a robust web API (likely built with FastAPI) for interaction. At its core, it integrates Large Language Models (LLMs) for intelligent text synthesis and analysis, complemented by a vector database (PostgreSQL with Timescale Vector) for efficient semantic search and retrieval-augmented generation (RAG). The application is containerized using Docker and Docker Compose for easy deployment and management. A critical component of its design is the deep integration with Langfuse, an open-source LLM observability platform, used for prompt management, tracing LLM interactions, and monitoring performance. The system is designed to ingest legal documents, process them, query relevant regulations, and generate detailed, human-readable compliance reports.

## ✨ Key Features

-   **AI-Powered Contract Analysis:** Leverages sophisticated Large Language Models to deeply understand and analyze legal contract text against established regulatory frameworks.
-   **Intelligent Document Processing (IDP):** Extracts text from various PDF documents, cleans it, and structures it into a machine-readable format optimized for subsequent AI analysis.
-   **Semantic Search & Retrieval-Augmented Generation (RAG):** Utilizes a dedicated vector store (Timescale Vector) to perform highly accurate semantic searches, retrieving the most relevant regulatory context to inform LLM responses and compliance checks.
-   **Comprehensive LLM Observability with Langfuse:** Integrates Langfuse for end-to-end tracing of LLM calls, detailed prompt management, performance monitoring, and robust evaluation capabilities, ensuring transparent and improvable AI operations.
-   **Automated Suitability Report Generation:** Automatically produces detailed, actionable PDF reports outlining the compliance status of contracts, clearly identifying clauses and sections that require attention or indicate non-compliance.
-   **Extensible LLM Provider Support:** Designed with an LLM factory pattern, allowing seamless integration and switching between various leading LLM providers, including OpenAI, Hugging Face models, and Groq, based on performance or cost requirements.
-   **Regulatory Data Management:** Includes scripts and utilities (`for_exactlaw.py`, `fords.py`) to prepare and manage legal and regulatory datasets for effective compliance checking.

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

## 🚀 Getting Started

To get xAndaaz AI up and running on your local machine, follow these steps:

### Prerequisites

Make sure you have the following installed:

*   **Python 3.9+**
*   **Docker Desktop** (includes Docker Engine and Docker Compose)
*   **Git**

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-org/xAndaaz-ai-powered-regulatory-compliance-checker-for-contract-9cbee5b.git
    cd xAndaaz-ai-powered-regulatory-compliance-checker-for-contract-9cbee5b
    ```

2.  **Set Up Environment Variables:**
    Create a `.env` file in the root directory by copying `app/example.env` and filling in the necessary API keys and database credentials. This will primarily include your OpenAI/Hugging Face/Groq API keys and Langfuse connection details.
    ```bash
    cp app/example.env .env
    # Open .env and populate variables
    ```

3.  **Start Database and Langfuse Services:**
    Navigate to the `docker` directory and use Docker Compose to spin up the necessary services (PostgreSQL, Timescale Vector, Langfuse backend, etc.).
    ```bash
    cd docker
    docker-compose up -d
    cd .. # Go back to the project root
    ```

4.  **Install Python Dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

5.  **Run Database Migrations (for Langfuse & Project DB):**
    The `docker/langfuse/packages/shared/prisma` directory contains migrations for the database schema.
    ```bash
    # You might need to install Prisma CLI globally or use npx
    npm install -g prisma # If not already installed
    cd docker/langfuse/packages/shared/
    npx prisma migrate dev --name init # Run migrations for Langfuse
    cd ../../../.. # Go back to the project root
    ```
    *Note: Specific migration commands for your project's `app/database` would go here, if not handled automatically.*

6.  **Ingest Initial Data (Optional, but recommended for testing):**
    Run the script to insert sample legal documents or regulatory data into the vector store.
    ```bash
    python app/insert_vectors.py
    ```

## 🔧 Usage

Once the services are running and dependencies are installed, you can start the xAndaaz AI API and interact with it.

1.  **Start the API Server:**
    From the project root directory:
    ```bash
    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be accessible at `http://localhost:8000`. You can view the automatically generated API documentation at `http://localhost:8000/docs`.

2.  **Analyze a Contract:**
    You can send a PDF contract for analysis. Replace `path/to/your/contract.pdf` with the actual path to your file.
    ```bash
    curl -X POST "http://localhost:8000/analyze-contract" \
         -H "accept: application/json" \
         -H "Content-Type: multipart/form-data" \
         -F "file=@path/to/your/contract.pdf;type=application/pdf"
    ```
    The API will process the document and return an analysis, including a path to the generated suitability report in the `output_reports/` directory.

3.  **Explore Langfuse UI:**
    If Langfuse is running via Docker Compose, you can access its UI (usually on `http://localhost:3000` or `http://localhost:langfuse:3000` depending on your Docker setup) to monitor LLM traces, manage prompts, and analyze evaluations.

## 🤝 Contributing

We welcome contributions to xAndaaz AI! Whether it's bug reports, feature requests, code contributions, or documentation improvements, your help is highly valued.

1.  **Fork the repository.**
2.  **Create your feature branch:** `git checkout -b feature/AmazingFeature`
3.  **Commit your changes:** `git commit -m 'Add some AmazingFeature'`
4.  **Push to the branch:** `git push origin feature/AmazingFeature`
5.  **Open a Pull Request.**

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
