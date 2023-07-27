from fastapi import FastAPI, HTTPException
from model import DBsiswa
from body import DBsiswaResponse, MetaData, DBsiswaData
from tortoise_config import init_db

app = FastAPI()

# Inisialisasi Tortoise ORM
@app.on_event("startup")
async def startup_event():
    init_db(app)

# Fungsi CRUD
async def create_siswa(nama: str, hobi: str) -> DBsiswaResponse:
    siswa = await DBsiswa.create(nama=nama, hobi=hobi)
    data_response = DBsiswaData(id=siswa.id, nama=siswa.nama, hobi=siswa.hobi)
    return DBsiswaResponse(meta=MetaData(code=200, message="created"), response=[data_response])

async def get_all_siswa() -> DBsiswaResponse:
    all_siswa = await DBsiswa.all()
    response_data = [DBsiswaData(id=siswa.id, nama=siswa.nama, hobi=siswa.hobi) for siswa in all_siswa]
    return DBsiswaResponse(meta=MetaData(code=200, message="success"), response=response_data)

async def update_siswa(siswa_id: int, nama: str, hobi: str) -> DBsiswaResponse:
    siswa = await DBsiswa.filter(id=siswa_id).first()
    if not siswa:
        raise HTTPException(status_code=404, detail="Siswa not found")

    await DBsiswa.filter(id=siswa_id).update(nama=nama, hobi=hobi)
    updated_siswa = await DBsiswa.filter(id=siswa_id).first()
    data_response = DBsiswaData(id=updated_siswa.id, nama=updated_siswa.nama, hobi=updated_siswa.hobi)
    return DBsiswaResponse(meta=MetaData(code=201, message="updated"), response=[data_response])

async def delete_siswa(siswa_id: int) -> DBsiswaResponse:
    siswa = await DBsiswa.filter(id=siswa_id).first()
    if not siswa:
        raise HTTPException(status_code=404, detail="Siswa not found")

    await DBsiswa.filter(id=siswa_id).delete()
    data_response = DBsiswaData(id=siswa.id, nama=siswa.nama, hobi=siswa.hobi)
    return DBsiswaResponse(meta=MetaData(code=204, message="deleted"), response=[data_response])

# Endpoint untuk CRUD
@app.post("/create_siswa/", response_model=DBsiswaResponse)
async def create_siswa_endpoint(nama: str, hobi: str):
    return await create_siswa(nama, hobi)

@app.get("/siswa/", response_model=DBsiswaResponse)
async def get_all_siswa_endpoint():
    return await get_all_siswa()

@app.put("/siswa/{siswa_id}", response_model=DBsiswaResponse)
async def update_siswa_endpoint(siswa_id: int, nama: str, hobi: str):
    return await update_siswa(siswa_id, nama, hobi)

@app.delete("/siswa/{siswa_id}", response_model=DBsiswaResponse)
async def delete_siswa_endpoint(siswa_id: int):
    return await delete_siswa(siswa_id)