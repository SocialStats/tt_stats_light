import argparse
import pandas as pd
import pickle


def compute_stats(videos_info, user_info):
    avg_plays_per_video = videos_info["stats_play_count"].mean()
    avg_comments_per_video = videos_info["stats_comment_count"].mean()
    avg_shares_per_video = videos_info["stats_share_count"].mean()
    views_per_subs_avg = (videos_info["stats_play_count"] / user_info["stats_follower_count"]).mean()
    all_likes_per_subs = user_info["stats_heart_count"] / user_info["stats_follower_count"]
    # avg likes per video
    total_plays = videos_info["stats_play_count"].sum()
    total_comments = videos_info["stats_comment_count"].sum()
    date_of_last_video = videos_info["create_time"].max()
    avg_date_diff = videos_info["create_time"].diff().abs().mean()
    # top_popular_videos_by_plays = videos_info.sort_values("stats_play_count", ascending=False)[:1]
    # top_popular_videos_by_comments = videos_info.sort_values("stats_comment_count", ascending=False)[:1]
    # top_popular_videos_by_shares = videos_info.sort_values("stats_share_count", ascending=False)[:1]
    most_frequent_music_title = videos_info["music_title"].value_counts()[:1].to_dict()
    # most popular music track by one video plays
    top_music_title_by_video_plays = videos_info.sort_values("stats_play_count", ascending=False).iloc[0]["music_title"]
    # most popular music track by videos cumsum plays
    # top_music_by_cumsum_plays = videos_info.groupby("music_title")["stats_play_count"].sum().sort_values(ascending=False)[:1]
    most_common_tag = videos_info["tags"].str.split().explode().value_counts()[:1].to_dict()
    # total duration video time
    total_dur_vid_time = videos_info["video_duration"].sum()
    avg_dur_vid_time = videos_info["video_duration"].mean()
    result = {
        "avg_plays_per_video": avg_plays_per_video,
        "avg_comments_per_video": avg_comments_per_video,
        "avg_shares_per_video": avg_shares_per_video,
        "total_plays": total_plays,
        "total_comments": total_comments,
        "date_of_last_video": date_of_last_video,
        "avg_date_diff": avg_date_diff,
        # "top_popular_videos_by_plays": top_popular_videos_by_plays,
        # "top_popular_videos_by_comments": top_popular_videos_by_comments,
        # "top_popular_videos_by_shares": top_popular_videos_by_shares,
        "most_frequent_music_title": most_frequent_music_title,
        "top_music_title_by_video_plays": top_music_title_by_video_plays,
        # "top_music_by_cumsum_plays": top_music_by_cumsum_plays,
        "most_common_tag": most_common_tag,
        "total_dur_vid_time": total_dur_vid_time,
        "avg_dur_vid_time": avg_dur_vid_time,
        "views_per_subs_avg": views_per_subs_avg,
        "all_likes_per_subs": all_likes_per_subs,
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Compute stats by user")
    parser.add_argument("path_to_raw_data", help="Path to raw data")
    args = parser.parse_args()
    raw_data = pickle.load(open(args.path_to_raw_data, "rb"))
    user, videos = raw_data
    # user = pd.Series(user)
    videos = pd.DataFrame(videos)
    stats = compute_stats(videos, user)
