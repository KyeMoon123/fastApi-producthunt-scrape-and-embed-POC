from __future__ import annotations

from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    profileImage: str


class Node(BaseModel):
    id: str
    body: str
    createdAt: str
    user: User


class Edge(BaseModel):
    node: Node


class Comments(BaseModel):
    edges: List[Edge]


class Post(BaseModel):
    id: str
    description: str
    commentsCount: int
    comments: Comments


class Data(BaseModel):
    post: Post


class ProductHuntPostResponse(BaseModel):
    data: Data
