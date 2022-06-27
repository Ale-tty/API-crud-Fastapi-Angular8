from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_person,
    delete_person,
    retrieve_person,
    retrieve_people,
    update_person,
)
from server.models.person import (
    ErrorResponseModel,
    ResponseModel,
    PersonSchema,
    UpdatePersonModel,
)


router = APIRouter()

'''
@router.post('/people')
async def add_person_data(person: personSchema = Body(...)):
    id = people_collection.insert_one(dict(person)).inserted_id
    return serializeDict(people_collection.find_one({"_id": ObjectId(id)}))


@router.get('/people')
async def find_all_people():
    return serializeList(people_collection.find())


@router.get('/people/{id}')
async def find_one_person(id):
    return serializeDict(people_collection.find_one({"_id": ObjectId(id)}))


@router.put('/people/{id}')
async def update_person(id, person: People):
    people_collection.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(person)
    })
    return serializeDict(people_collection.find_one({"_id": ObjectId(id)}))


@router.delete('/people/{id}')
async def delete_person(id: str):
    return serializeDict(people_collection.find_one_and_delete({"_id": ObjectId(id)}))
'''


@router.post("/", response_description="Person data added into the database")
async def add_person_data(person: PersonSchema = Body(...)):
    person = jsonable_encoder(person)
    new_person = await add_person(person)
    return ResponseModel(new_person, "Person added successfully.")


@router.get("/", response_description="People retrieved")
async def get_persons():
    people = await retrieve_people()
    if people:
        return ResponseModel(people, "People data retrieved successfully")
    return ResponseModel(people, "Empty list returned")


@router.get("/{id}", response_description="Person data retrieved")
async def get_person_data(id):
    person = await retrieve_person(id)
    if person:
        return ResponseModel(person, "Person data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "person doesn't exist.")


@router.put("/{id}")
async def update_person_data(id: str, req: UpdatePersonModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_person = await update_person(id, req)
    if updated_person:
        return ResponseModel(
            "Person with ID: {} name update is successful".format(id),
            "Person name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the person data.",
    )


@router.delete("/{id}", response_description="Person data deleted from the database")
async def delete_person_data(id: str):
    deleted_person = await delete_person(id)
    if deleted_person:
        return ResponseModel(
            "Person with ID: {} removed".format(
                id), "Person deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Person with id {0} doesn't exist".format(id)
    )
