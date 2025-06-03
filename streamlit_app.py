import streamlit as st
import requests

def fetch_data_from_api(profile_url: str):
    try:
        response = requests.get("http://localhost:8000/stats/", params={"profile_url": profile_url}, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"API call failed: {str(e)}")
    return None

def main():
    st.set_page_config(page_title="LeetCode Stats", layout="wide")
    st.title("🧮 LeetCode Profile Stats")
    profile_url = st.text_input("LeetCode Profile URL")

    if st.button("Get Stats"):
        data = fetch_data_from_api(profile_url)
        if data:
            st.json(data)  # Replace with display_stats if needed

if __name__ == "__main__":
    main()
