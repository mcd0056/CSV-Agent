from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import RedirectResponse
from agent import execute_agent
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from tempfile import NamedTemporaryFile
import shutil

load_dotenv()

app = FastAPI()

# Add CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the static path to the directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# on start delete the temp directory and create a new one
@app.on_event("startup")
async def startup_event():
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

        
class QueryRequest(BaseModel):
    message: str  


@app.get("/")
async def redirect_root():
    return RedirectResponse("static/index.html")

@app.post("/chat/")
async def invoke_chain(request: QueryRequest):
    try:
        response = execute_agent(request.message)  # This line is crucial
        return JSONResponse(content={"response": response})
    
    except Exception as e:
        return JSONResponse(content={"response": str(e)})
    

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # Generate a temporary file
        with NamedTemporaryFile(delete=False, suffix=".csv", dir="temp") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
