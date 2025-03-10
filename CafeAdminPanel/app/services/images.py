import os
from datetime import datetime
import shutil
from pathlib import Path

from fastapi import File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse


class ImagesService:
    @staticmethod
    def upload_image(file: UploadFile = File(...)):
        try:
            upload_dir = Path(f"{os.getcwd()}/static/images/temp_uploaded_files")
            upload_dir.mkdir(exist_ok=True)

            filename = f"pubnamemainimage_{datetime.utcnow().strftime('%m_%d_%Y, %H_%M_%S')}_{file.filename}"

            file_path = upload_dir / filename

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return {"filepath": file_path, "filename": filename}
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"ERR: {err}"
            )

    @staticmethod
    def delete_tmp_image_from_local_dir(file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file_path} has been deleted.")
            else:
                print(f"The file {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

