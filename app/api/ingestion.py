from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models.document import Document
from pydantic import BaseModel
import boto3
import os
import json

router = APIRouter()

# AWS Bedrock Client
aws_region = os.getenv("AWS_REGION", "ap-south-1")
bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)

# Pydantic model for request validation
class DocumentIngestionRequest(BaseModel):
    title: str
    content: str

# Generate embeddings using AWS Bedrock and MistralAI
def generate_embedding_with_bedrock(content: str, model_id: str):
    try:
        payload = {
            "prompt": content,
            "max_tokens": 100,
            "temperature": 0.75,
            "top_p": 1.0
        }

        payload_json = json.dumps(payload)
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=payload_json,
        )

        # Read the response
        result = json.loads(response["body"].read())
        outputs = result.get("outputs", [])
        if not outputs:
            raise ValueError("No outputs found in Bedrock response.")

        # Extract and validate text
        text = outputs[0].get("text", "").strip()
        if not text:
            raise ValueError("No text content found in Bedrock response.")

        # Ensure text contains expected format (optional check based on your embedding requirements)
        if not isinstance(text, str):
            raise ValueError("Invalid format for text in Bedrock response.")

        # Debugging: Log the generated text
        print(f"Generated text from Bedrock: {text}")

        # Convert text to bytes as a placeholder for embeddings (adjust logic if embeddings differ)
        embedding = text
        return embedding
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings: {e}")

# API Endpoint
@router.post("/")
async def ingest_document(data: DocumentIngestionRequest, db_context=Depends(get_db)):
    async with db_context as db:
        model_id = "mistral.mistral-7b-instruct-v0:2"  # Change as needed

        try:
            # Generate embeddings using Bedrock
            embedding = generate_embedding_with_bedrock(data.content, model_id)
            # if not isinstance(embedding, bytes):
            #     raise ValueError("Embedding must be of type bytes")
            
            # Store document in the database
            document = Document(title=data.title, content=data.content, embedding=json.dumps(embedding))
            
            db.add(document)
            await db.commit()


            return {"message": "Document ingested successfully", "id": document.id}

        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail="Failed to generate embeddings.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unexpected error occurred.")
