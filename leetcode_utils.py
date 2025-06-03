import re
import requests
from typing import Dict, Optional

def extract_username_from_url(url: str) -> Optional[str]:
    patterns = [
        r'leetcode\.com/u/([^/\s]+)',
        r'leetcode\.com/([^/\s]+)/?$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url.strip().rstrip('/'))
        if match:
            return match.group(1)
    return None

def get_leetcode_stats(username: str) -> Optional[Dict]:
    try:
        query = """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                submitStats: submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
                tagProblemCounts {
                    advanced {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    intermediate {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    fundamental {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                }
                profile {
                    realName
                    aboutMe
                    userAvatar
                    location
                    skillTags
                    websites
                }
            }
        }
        """
        variables = {"username": username}
        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com/',
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.post(
            'https://leetcode.com/graphql',
            json={'query': query, 'variables': variables},
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and data['data'].get('matchedUser'):
                return data['data']['matchedUser']
        return None
    except Exception as e:
        return None

def get_topic_insights(topic_data: Dict) -> Dict:
    insights = {
        'total_categories': 0,
        'most_solved_topic': None,
        'total_unique_topics': 0,
        'strongest_category': None
    }
    all_topics = []
    category_totals = {}
    for category, topics in topic_data.items():
        if topics:
            insights['total_categories'] += 1
            category_total = 0
            for topic in topics:
                problems_solved = topic.get('problemsSolved', 0)
                if problems_solved > 0:
                    all_topics.append({
                        'name': topic.get('tagName', ''),
                        'count': problems_solved,
                        'category': category
                    })
                    category_total += problems_solved
            category_totals[category] = category_total
    if all_topics:
        most_solved = max(all_topics, key=lambda x: x['count'])
        insights['most_solved_topic'] = most_solved
        insights['total_unique_topics'] = len(all_topics)
        if category_totals:
            strongest_cat = max(category_totals.items(), key=lambda x: x[1])
            insights['strongest_category'] = strongest_cat
    return insights
