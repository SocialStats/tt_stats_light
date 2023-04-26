from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tt_stats_light.crawler.get_user_data import get_data
from tt_stats_light.data.compute_stats import prepare_input_data, compute_stats

app = FastAPI()


@app.get("/get_stats_by_user/{user_name}")
def get_stats_by_user(user_name):
    user_info, videos_info = get_data(user_name)
    user_info, videos_info = prepare_input_data(user_info, videos_info)
    stats = compute_stats(videos_info, user_info)
    json_compatible_item_data = jsonable_encoder(stats)
    return JSONResponse(content=json_compatible_item_data)
