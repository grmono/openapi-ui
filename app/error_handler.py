from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from fastapi import HTTPException, Header

################################################################################
# Error Handler
################################################################################


def abort(error, msg=None):
	if error == 401:
		raise HTTPException(
			status_code=HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Basic"})

	elif error == 403:
		raise HTTPException(
			status_code=403,
			detail="Unothorized",
			headers={"WWW-Authenticate": "Basic"})

	elif not msg and error:
		raise HTTPException(
			status_code=error,
			detail="Internal Server Error",
			headers={"WWW-Authenticate": "Basic"})

	elif msg and error:
		raise HTTPException(
			status_code=error,
			detail=msg,
			headers={"WWW-Authenticate": "Basic"})


def upload_check(file_context):
	file_destination = Path(destination)
	try:
		# Writes file to destination while validating file size
		real_file_size = 0
		with file_destination.open("wb") as buffer:
			for chunk in upload_file.file:
				real_file_size += len(chunk)
				if real_file_size > max_fize_size:
					raise Exception("Too large")
				buffer.write(chunk)
	except HTTPException as e:
		os.unlink(file_destination)
		abort(413, str(e))
	finally:
		upload_file.file.close()
