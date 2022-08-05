import os

from fastapi import APIRouter
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from .. import db

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

# aws auth
REGION = os.environ.get("REGION")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
SERVICE = os.environ.get("SERVICE", "es")
auth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION, SERVICE)

# opensearch
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

def get_client():
    """
        get es connect client
    """
    es = OpenSearch(
            hosts=[{"host": HOST, "port": PORT}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
    return es

@router.post("/{username}")
def create_index(username: str):
    """
        회원가입 시에 index 테이블을 생성
    """
    settings = {
                "index": {
                    "analysis": {
                        "tokenizer": {
                            "seunjeon": {
                                "type": "seunjeon_tokenizer",
                            }
                        },
                        "analyzer": {
                            "korean": {
                                "type": "custom",
                                "tokenizer": "seunjeon"
                            }
                        }
                    }
                }
            }

    mappings = {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "korean"
            }
        }
    }
    with get_client() as es:
        if not es.indices.exists(index=username):
            es.indices.create(index=username, body={"settings":settings, "mappings":mappings})
        
            # insert plans
            docs = []
            for plan in db.get_plans(username):
                docs.append({"index": {"_index": username, "_id": plan["title"]}})
                docs.append({"title": plan["title"]})

            es.bulk(body=docs)

    return dict(status=200)

@router.get("/{username}/{title}")
def search_title(username: str, title: str):
    """
        title과 유사한 titles 반환
    """
    with get_client() as es:
        results = es.search(index=username, body={"query": {"match": {"title": title}}})

        titles = []
        for obj in results["hits"]["hits"]:
            titles.append(obj["_source"]["title"])

    return dict(status=200, cands=titles)

@router.post("/{username}/{title}")
def register_title(username, title):
    """
        title 등록
    """
    with get_client() as es:
        es.index(index=username, id=title, body={"title": title})

    return dict(status=200)