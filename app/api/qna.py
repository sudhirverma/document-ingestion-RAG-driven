from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # Import AsyncSession
from app.services.retrieval import retrieve_relevant_documents
from app.db import get_db
from pydantic import BaseModel
from contextlib import asynccontextmanager
import boto3
import os
import json

router = APIRouter()

# AWS Bedrock Client
aws_region = os.getenv("AWS_REGION", "us-east-1")
bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)

# Pydantic model for request validation
class QuestionRequest(BaseModel):
    question: str

# Helper function to generate an answer using AWS Bedrock and MistralAI
def generate_answer_with_bedrock(question: str, context: str, model_id: str):
    try:
        # Combine question and context into a prompt
        prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
        
        payload = {
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.75,
            "top_p": 1.0
        }

        payload_json = json.dumps(payload)
        
        # Invoke AWS Bedrock with Mistral model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=payload_json,
        )
        
        result = json.loads(response["body"].read())
        # Extract answer from the "outputs" list
        outputs = result.get("outputs", [])
        if not outputs:
            raise ValueError("No outputs found in Bedrock response.")

        answer = outputs[0].get("text", "").strip()
        if not answer:
            raise ValueError("No answer text found in Bedrock response.")

        # Check for truncation
        stop_reason = outputs[0].get("stop_reason", None)
        if stop_reason == "length":
            print("Warning: The answer was truncated due to length.")
        
        return answer
    except Exception as e:
        raise RuntimeError(f"Error generating answer: {e}")


# API Endpoint
@router.post("/")
async def answer_question(data: QuestionRequest, db_context=Depends(get_db)):
    async with db_context as db:  # Explicitly unwrap the context manager
        model_id = "mistral.mistral-7b-instruct-v0:2"  # Change based on your preference

        try:
            # Retrieve relevant documents
            relevant_docs = await retrieve_relevant_documents(data.question, db)
            if not relevant_docs:
                raise HTTPException(status_code=404, detail="No relevant documents found.")

            # Combine retrieved documents into context
            context = "\n".join([doc.page_content for doc in relevant_docs])

            # Generate answer using Bedrock and MistralAI
            answer = generate_answer_with_bedrock(data.question, context, model_id)
            return {"question": data.question, "answer": answer}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
