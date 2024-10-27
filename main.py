from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from idea import IDEA

# Ваш клас IDEA з попереднього коду тут...

app = FastAPI()

origins = [
    "https://idea-cipher-gallkq4pj-taras-projects-adb37d18.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель для запиту шифрування
class EncryptionRequest(BaseModel):
    key: str  # Ключ у hex форматі
    plain: str  # Plaintext у ASCII

# Модель для запиту дешифрування
class DecryptionRequest(BaseModel):
    key: str  # Ключ у hex форматі
    ciphertext: str  # Ciphertext у hex форматі

@app.post("/encrypt")
async def encrypt(data: EncryptionRequest):
    try:
        # Перетворення ключа з hex у int
        key = int(data.key, 16)
        my_IDEA = IDEA(key)

        # Перетворення plaintext з ASCII в int
        plain = int.from_bytes(data.plain.encode("ASCII"), 'big')
        encrypted = my_IDEA.encrypt_string(plain)

        # Повернення зашифрованого тексту у hex форматі
        return {"encrypted": hex(encrypted)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/decrypt")
async def decrypt(data: DecryptionRequest):
    try:
        # Convert key from hex to int
        key = int(data.key, 16)
        my_IDEA = IDEA(key)

        # Convert ciphertext from hex to int
        encrypted = int(data.ciphertext, 16)

        # Decrypt and get the plaintext text
        decrypted_text = my_IDEA.decrypt_string(encrypted)

        return {"decrypted_text": decrypted_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
