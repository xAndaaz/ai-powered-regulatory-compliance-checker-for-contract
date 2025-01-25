from typing import List
import pandas as pd
from pydantic import BaseModel, Field
from app.services.llm_factory import LLMFactory
from langfuse.decorators import observe

from app.config.settings import get_settings  # Import the get_settings function
#initialize get_setting for langfuse 
settings = get_settings()
langfuse = settings.langfuse.get_client()

class SynthesizedResponse(BaseModel):
    thought_process: List[str] = Field(
        description="List of thoughts that the AI assistant had while synthesizing the answer"
    )
    answer: str = Field(description="The synthesized answer to the user's question")
    enough_context: bool = Field(
        description="Whether the assistant has enough context to answer the question"
    )


class Synthesizer:
    SYSTEM_PROMPT = """
    ### Context:
    Given the text from a legal contract extracted from a PDF, evaluate the document with the following priorities:

    1. Understanding Content:
       - Grasp the core intent and structure of the contract.
       - Identify key elements such as parties involved, obligations, and terms.

    2. Regulatory Knowledge:
       - Pre-incorporate understanding of relevant regulatory frameworks, including but not limited to major international and national regulations like GDPR, CCPA, HIPAA, FCPA, etc.
       - Consider jurisdiction-specific compliance requirements explicitly stated or inferred from the contract (e.g., EU, USA, UK).

    3. Analysis for Compliance:
       - Assess each section of the contract for adherence to the identified standards.
       - Highlight any clauses or statements that potentially violate or fail to meet regulatory requirements.
       - Detect and flag missing elements that are critical for full compliance.

    4. Outcome Summary:
       - Produce a concise report detailing each compliance issue found, organized by category (e.g., data protection, financial disclosures, etc.).
       - Provide suggestions for remediation actions or additional review required by a legal professional.
       - Point out ambiguous terms or unclear language that could lead to compliance risks.

    5. Autonomous Action:
       - Initiate analysis and reporting without requiring additional input or context.
       - Assume no preexisting queries are provided by the user; derive all necessary insights from the text itself.

    ### Prompt:
    "Analyze the provided contract text extracted from a PDF for compliance with relevant regulations. Review and identify any sections or clauses that may not comply with applicable laws and standards. Prepare a detailed report highlighting potential compliance issues, suggest necessary amendments, and identify sections requiring further legal scrutiny. Incorporate understanding of regulations such as GDPR, CCPA, HIPAA, FCPA, reflecting the probable jurisdiction involved. Herein is the contract text for analysis: [Insert Extracted Contract Text]."

    """

    @staticmethod
    def generate_response(question: str, context: pd.DataFrame) -> SynthesizedResponse:
        """Generates a synthesized response based on the question and context.

        Args:
            question: The user's question.
            context: The relevant context retrieved from the knowledge base.

        Returns:
            A SynthesizedResponse containing thought process and answer.
        """
        context_str = Synthesizer.dataframe_to_json(  # Call the method using the Synthesizer class
            context, columns_to_keep=['id', 'content', 'embedding', 'distance', 'Filename', 'Exclusivity','Renewal Term', 'Agreement Date', 'Effective Date', 'Expiration Date','Post-Termination Services', 'Notice Period To Terminate Renewal']
        )

        messages = [
            {"role": "system", "content": Synthesizer.SYSTEM_PROMPT},
            {"role": "user", "content": f"# User question:\n{question}"},
            {
                "role": "assistant",
                "content": f"# Retrieved information:\n{context_str}",
            },
        ]

        llm = LLMFactory("openai")
        return llm.create_completion(
            response_model=SynthesizedResponse,
            messages=messages,
        )

    @staticmethod
    def dataframe_to_json(
        context: pd.DataFrame,
        columns_to_keep: List[str],
    ) -> str:
        """
        Convert the context DataFrame to a JSON string.

        Args:
            context (pd.DataFrame): The context DataFrame.
            columns_to_keep (List[str]): The columns to include in the output.

        Returns:
            str: A JSON string representation of the selected columns.
        """
        return context[columns_to_keep].to_json(orient="records", indent=2)