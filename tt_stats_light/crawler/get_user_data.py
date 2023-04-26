import argparse
from typing import Any, Dict, List, Tuple
import pickle
from tiktokapipy.api import TikTokAPI, User, Video
from tt_stats_light.constants import BASE_DATA_DIR
from tqdm import tqdm
from loguru import logger

logger.add("logs/get_user_data.log", level="INFO")


def get_user_info(user: User) -> Dict[str, Any]:
    cols = ["unique_id", "id", "nickname", "sec_uid", "private_account", "verified"]
    result = {}
    stats = {"stats_" + key: value for key, value in dict(user.stats).items()}
    all_info = {col: dict(user).get(col) for col in cols}
    result.update(stats)
    result.update(all_info)
    return result


def get_videos_info(videos) -> List[Dict[str, Any]]:
    result_data = []
    for video in videos:
        result_by_video = {}
        result_by_video["id"] = video.id
        result_by_video["create_time"] = video.create_time
        result_by_video["description"] = video.desc

        for key, value in dict(video.video).items():
            result_by_video["video_" + key] = value
        for key, value in dict(video.music).items():
            result_by_video["music_" + key] = value
        for key, value in dict(video.stats).items():
            result_by_video["stats_" + key] = value

        hashtags = []
        for hashtag in video.challenges:
            hashtags.append(hashtag.title)
        result_by_video["hashtags"] = " ".join(sorted(hashtags))

        tags = []
        for tag in video.tags.light_models:
            tags.append(tag.title)
        result_by_video["tags"] = " ".join(sorted(tags))
        result_data.append(result_by_video)

    return result_data


def get_videos(videos_iterator, n_videos: int) -> List[Video]:
    videos: List[Video] = []
    try:
        for video in tqdm(videos_iterator, total=n_videos):
            videos.append(video)
    except Exception as error:  # noqa W0718
        print(error)
    return videos


def context_flow(user_tag: str, **qwargs) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    logger.info("Start crawling and open browser")
    with TikTokAPI(
        **qwargs,
    ) as api:
        logger.info("Browser is opened")
        user = api.user(
            user_tag,
            video_limit=100,
            scroll_down_time=0
            # qwargs.get("scroll_down_time")
        )
        # iterator = user.videos
        logger.info("Start downloading videos info")
        user_videos = get_videos(user.videos, user.stats.video_count)
        user_info = get_user_info(user)
        videos_info = get_videos_info(user_videos)
        logger.info("All videos info is downloaded")
    return user_info, videos_info


def get_data(user_tag: str, **qwargs) -> Tuple:
    user_info, videos_info = context_flow(user_tag, **qwargs)
    return user_info, videos_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Get user data from TikTok")
    parser.add_argument("user_name", help="User name")
    args = parser.parse_args()
    # proxy = {"server": "http://51.222.155.142:80"}
    user_data = get_data(
        args.user_name,
        # proxy=proxy,
        # scroll_down_time=100,
        navigation_retries=5,
        navigation_timeout=0,
        data_dump_file=BASE_DATA_DIR / "raw/",
        # navigator_type="Chromium",
    )
    with open(BASE_DATA_DIR / "raw/" / "user_data.pkl", "wb") as file:
        pickle.dump(user_data, file)
