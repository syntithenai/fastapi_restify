from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from response_models import *
from typing import Optional, List
import json

def get_router(model):
    router = APIRouter()
    @router.get("/", response_description="Records retrieved")
    async def get(filter = None, limit = None, offset = None):
        if filter is not None:
            c = json.loads(filter)
            records = await model.find(c, limit, offset)
        else:
            records = await model.list(limit, offset)
        return ResponseModel(records, "Data retrieved successfully") \
            if len(records) > 0 \
            else ResponseModel(
            records, "Empty list returned")


    @router.get("/{id}", response_description="Data retrieved")
    async def get(id):
        record = await model.get(id)
        return ResponseModel(record, "Data retrieved successfully") \
            if record \
            else ErrorResponseModel("An error occured.", 404, "Record doesn't exist.")


    @router.post("/", response_description="Data added into the database")
    async def post(records: List[model.insertModelClass] = Body(...)):
        postedrecords = jsonable_encoder(records)
        new_records = []
        for record in postedrecords:
            new_record = await model.insert(record)
            new_records.append(new_record)
        return ResponseModel(new_records, "Added successfully.")


    @router.delete("/{id}", response_description="Data deleted from the database")
    async def delete(id: str):
        deleted = await model.delete(id)
        return ResponseModel("Record with ID: {} removed".format(id), "Record deleted successfully") \
            if deleted \
            else ErrorResponseModel("An error occured", 404, "Record with id {0} doesn't exist".format(id))


    @router.put("/")
    async def put(req: List[model.updateModelClass] = Body(...)):
        records = jsonable_encoder(req)
        new_records = []
        error = False
        for record in records:
            id = record.get('_id')
            if id:
                updated = await model.update(id, record)
                new_records.append(updated)
            else:
                error = True
        return ResponseModel("Records updated successfuly".format(new_records),
                             "Records updated successfully") \
            if not error \
            else ErrorResponseModel("An error occurred", 404, "There was an error updating the records.".format(records))

    @router.patch("/")
    async def patch(req: List[model.updateModelClass] = Body(...)):
        records = jsonable_encoder(req)
        new_records = []
        error = False
        for record in records:
            id = record.get('_id')
            if id:
                updated = await model.replace(id, record)
                new_records.append(updated)
            else:
                error = True
        return ResponseModel("Records replaced successful".format(new_records),
                             "Records replaced successfully") \
            if error \
            else ErrorResponseModel("An error occurred", 404, "There was an error replacing the records.".format(records))

    return router
