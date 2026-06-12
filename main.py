import os
import json

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi import Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# -----------------------------
# Load ENV
# -----------------------------

load_dotenv()

# -----------------------------
# FastAPI
# -----------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# -----------------------------
# Static Files
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

# -----------------------------
# GPT
# -----------------------------

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv(
        "OPENAI_API_KEY"
    ),
    temperature=0.7
)

# -----------------------------
# Load Products
# -----------------------------

with open(
    "data/products.json",
    "r",
    encoding="utf-8"
) as f:

    PRODUCTS = json.load(f)

# -----------------------------
# Pydantic Models
# -----------------------------

class ProductRequest(BaseModel):

    budget: int
    category: str


class ChatRequest(BaseModel):

    query: str

# -----------------------------
# Home
# -----------------------------

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html"
        
    )

# -----------------------------
# Recommend
# -----------------------------

@app.post("/recommend")
async def recommend(
    data: ProductRequest
):

    matched_products = [

        product

        for product in PRODUCTS

        if (
            product["category"].lower()
            ==
            data.category.lower()
        )

        and

        (
            product["price"]
            <=
            data.budget
        )
    ]

    matched_products = (
        matched_products[:8]
    )

    if not matched_products:

        return {
            "response":
            "No products found.",
            "products":[]
        }

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert product recommendation assistant.

        Category:
        {category}

        Budget:
        {budget}

        Products:
        {products}

        Explain why these products are good choices.
        Keep answer under 120 words.
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "category":
            data.category,

            "budget":
            data.budget,

            "products":
            matched_products
        }
    )

    return {

        "response":
        response.content,

        "products":
        matched_products
    }

# -----------------------------
# Chat
# -----------------------------

@app.post("/chat")
async def chat(
    data: ChatRequest
):

    prompt = ChatPromptTemplate.from_template(
        """
        You are SmartShop AI.

        User Query:
        {query}

        Recommend products
        and provide helpful
        shopping advice.
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "query":
            data.query
        }
    )

    return {

        "response":
        response.content,

        "products":
        PRODUCTS[:8]
    }