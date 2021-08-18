from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from response_models import *

def get_router(model):
    router = APIRouter()
    @router.get("/", response_description="Records retrieved")
    async def get():
        records = await model.list()
        # print('rec')
        # print(records)
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
    async def post(record: model.insertModelClass = Body(...)):
        record = jsonable_encoder(record)
        new_record = await model.insert(record)
        return ResponseModel(new_record, "Added successfully.")


    @router.delete("/{id}", response_description="Data deleted from the database")
    async def delete(id: str):
        deleted = await model.delete(id)
        return ResponseModel("Record with ID: {} removed".format(id), "Record deleted successfully") \
            if deleted \
            else ErrorResponseModel("An error occured", 404, "Student with id {0} doesn't exist".format(id))


    @router.put("/{id}")
    async def update(id: str, req: model.updateModelClass = Body(...)):
        updated = await model.update(id, req.dict())
        return ResponseModel("Record with ID: {} name update is successful".format(id),
                             "Record updated successfully") \
            if updated \
            else ErrorResponseModel("An error occurred", 404, "There was an error updating the record.".format(id))

    return router
