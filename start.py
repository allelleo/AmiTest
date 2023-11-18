import uvicorn

from server.app import app

if __name__ == '__main__':
    uvicorn.run(app, host='192.168.45.10')
