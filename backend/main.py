from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from model import get_embedding

import os
from shutil import copyfile

from utils import Util

INDEX_NAME = "updated-birds-dev"

es = Util.get_connection()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "./uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, image.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())

    # create an embedding of the uploaded image
    query_embedding = get_embedding(file_location)

    field_key = "image_embedding"

    knn = {
        "field": field_key,
        "k": 5,
        "num_candidates": 100,
        "query_vector": query_embedding,
        "boost": 100,
    }

    # The fields to retrieve from the matching documents
    fields = ["name", "scientific_name", "image_path", "description"]

    results = {}
    try:
        resp = es.search(index=INDEX_NAME, body={"knn": knn, "_source": fields}, size=3)
        # Return the search results
        print(resp)
        results = resp
    except Exception as e:
        print(f"An error occurred: {e}")
        results = {"error": e}

    # assemble an array for the response
    response = []
    for hit in results["hits"]["hits"]:
        hit["_source"]["score"] = hit["_score"]
        response.append(hit["_source"])

    # return the response as "similar images" json, and send 200 status code
    print("returning response")
    return {"similar_images": response}
