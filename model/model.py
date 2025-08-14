from typing import NamedTuple
from pydantic import BaseModel, Field

class Novelsinfo(NamedTuple):
    """章节信息"""
    title: str
    url: str
    type: str

class NovelInfo(BaseModel):
    """小说主要信息
    """
    title: str = Field(..., description="小说标题")
    author: str = Field(..., description="作者")
    type: str = Field(..., description="类别")
    status: str = Field(..., description="是否连载")
    intro: str = Field(..., description="简介")
    index_url: str = Field(..., description="小说首页")
    wordsount: str = Field(..., description="字数")
    last_update: str = Field(..., description="最后更新时间")

