from typing import List, Union

from beanie import PydanticObjectId

from models.admin import Admin
from models.student import Student
from models.audio import Predictions

admin_collection = Admin
student_collection = Student
preductions_collection = Predictions



async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


async def retrieve_students() -> List[Student]:
    students = await student_collection.all().to_list()
    return students

async def add_predictions(new_pred: Predictions) -> Predictions:
    preduction = await new_pred.create()
    return preduction

async def retrieve_predictions() -> List[Predictions]:
    predictions = await preductions_collection.all().to_list()
    return predictions

async def retrieve_prediction(id: PydanticObjectId) -> Predictions:
    prediction = await preductions_collection.get(id)
    if prediction:
        return prediction
    
async def delete_prediction(id: PydanticObjectId) -> bool:
    prediction = await preductions_collection.get(id)
    if prediction:
        await prediction.delete()
        return True



async def add_student(new_student: Student) -> Student:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> Student:
    student = await student_collection.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await student_collection.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    student = await student_collection.get(id)
    if student:
        await student.update(update_query)
        return student
    return False
