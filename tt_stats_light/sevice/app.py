from fastapi import FastAPI
from tt_stats_light.crawler.get_user_data import get_data
from tt_stats_light.data.compute_stats import compute_stats

app = FastAPI()


@app.get("/get_stats_by_user/{user_name}")
def get_stats_by_user(user_name):
    pass
