from common.config import *

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(
		"server:app",
		host=APP_HOST,
		port=int(APP_PORT),
		reload=APP_RELOAD,
		root_path=API_ROOT_PATH,
		debug=APP_DEBUG,
		log_level=LOG_LEVEL,
		workers=4)
