"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Personal brand website schemas

class Contactmessage(BaseModel):
    """
    Contact messages from the website
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender's name")
    email: EmailStr = Field(..., description="Sender's email")
    subject: Optional[str] = Field(None, description="Message subject")
    message: str = Field(..., min_length=1, max_length=5000, description="Message body")

class Project(BaseModel):
    """
    Portfolio projects to showcase on site
    Collection name: "project"
    """
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Short description")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tech or keywords")
    url: Optional[str] = Field(None, description="Live link")
    repo: Optional[str] = Field(None, description="Repository link")
    image: Optional[str] = Field(None, description="Image URL")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
