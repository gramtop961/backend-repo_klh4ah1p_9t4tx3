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
    email: EmailStr = Field(..., description="Email address")
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

# Mousepad-specific product schema
class Mousepad(BaseModel):
    """
    Premium mousepads (90x40 cm)
    Collection name: "mousepad"
    """
    design: str = Field(..., description="Design name")
    price: float = Field(..., ge=0, description="Price in USD")
    description: str = Field(..., description="Short marketing description")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    in_stock: bool = Field(True, description="Availability")
    stock_qty: int = Field(0, ge=0, description="Units available")
    material: str = Field("Micro-weave cloth", description="Surface material")
    base: str = Field("Non-slip rubber", description="Base material")
    thickness_mm: float = Field(4.0, description="Thickness in mm")
    width_cm: float = Field(90.0, description="Width in cm")
    height_cm: float = Field(40.0, description="Height in cm")

class OrderItem(BaseModel):
    mousepad_id: str = Field(..., description="Referenced mousepad _id as string")
    quantity: int = Field(1, ge=1)
    unit_price: float = Field(..., ge=0)

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    customer_name: str = Field(...)
    customer_email: EmailStr = Field(...)
    shipping_address: str = Field(...)
    items: List[OrderItem] = Field(...)
    total: float = Field(..., ge=0)
    notes: Optional[str] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
