__all__ = "app"

from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before startup

    yield
    # before shutdown


app = FastAPI(lifespan=lifespan)


@app.websocket("/video/upload")
async def websocket_receive_video(websocket: WebSocket):
    await websocket.accept()
    try:
        with open(
            "received_video.mp4", "wb"
        ) as video_file:  # Открываем файл для записи
            while True:
                try:
                    data = await websocket.receive_bytes()
                    video_file.write(data)  # Записываем данные в файл
                except WebSocketDisconnect:
                    print("Client disconnected")
                    break
    except Exception as e:
        print(f"An error occurred: {e}")


@app.websocket("/video/receive")
async def websocket_send_video(websocket: WebSocket):
    cnt = 0
    await websocket.accept()
    while True:
        break
        # Здесь вы будете отправлять обработанные данные видео обратно клиенту
        # Это может быть асинхронное получение данных из очереди или хранилища как угодно
    try:
        with open(
            "received_video.mp4", "rb"
        ) as video_file:  # Открываем видеофайл для чтения
            while True:
                # data = video_file.read()
                data = video_file.read(4096)  # Читаем порцию данных
                if not data:
                    break  # Если данные закончились, выходим из цикла
                await websocket.send_bytes(data)  # Отправляем порцию данных клиенту
                cnt += 4096
                print(cnt)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
