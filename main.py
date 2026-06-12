from dotenv import load_dotenv
import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI()

# ---------------------------
# Gemini Model
# ---------------------------

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

# ---------------------------
# Middleware
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------------------
# Static + Templates
# ---------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

# ---------------------------
# Request Models
# ---------------------------

class ProductRequest(BaseModel):
    budget: int
    category: str

class ChatRequest(BaseModel):
    query: str

# ---------------------------
# Home Page
# ---------------------------

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
       
    )

# ---------------------------
# Product Recommendation
# ---------------------------

@app.post("/recommend")
async def recommend(data: ProductRequest):

    prompt = f"""
    Recommend 5 products.

    Category: {data.category}
    Budget: {data.budget}

    Return:
    Product Name
    Price
    Description
    """

    response = llm.invoke(prompt)

    return {
        "recommendation": response.content
    }

# ---------------------------
# Chat Endpoint
# ---------------------------

@app.post("/chat")
async def chat(data: ChatRequest):

    prompt = ChatPromptTemplate.from_template("""
    You are an expert product recommendation assistant.

    User Query:
    {query}

    Provide:
    1. Best product recommendations
    2. Why they are recommended
    3. Pros and cons
    4. Budget considerations
    """)

    chain = prompt | llm

    response = chain.invoke({
        "query": data.query
    })
    return {'response':response.content}