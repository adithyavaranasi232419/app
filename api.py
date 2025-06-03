from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from leetcode_utils import extract_username_from_url, get_leetcode_stats, get_topic_insights

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stats/")
def fetch_stats(profile_url: str = Query(...)):
    username = extract_username_from_url(profile_url)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid LeetCode URL format")
    user_data = get_leetcode_stats(username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found or profile is private")
    insights = get_topic_insights(user_data.get("tagProblemCounts", {}))
    return {"username": username, "user_data": user_data, "insights": insights}
