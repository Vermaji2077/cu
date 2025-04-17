import streamlit as st
import requests

# TMDb API Key
API_KEY = "91c1dd1c7e0a4c4e8b26e6ae56b8622e"

st.set_page_config(page_title="🎬 Movie Info & Recommendations", layout="wide")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: #f0f0f0;
            font-family: 'Arial', sans-serif;
        }
        .stTextInput > div > div > input {
            background-color: #292929;
            color: #00eaff;
            border-radius: 10px;
            border: 2px solid #00eaff;
            font-size: 24px; /* Further increased font size */
            padding: 12px;
        }
        .stButton > button {
            background-color: #ff007f;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #ff007f;
        }
        .stButton > button:hover {
            background-color: #d4006a;
            border: 2px solid #d4006a;
        }
        .stImage img {
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 238, 255, 0.7);
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #ff007f;
        }
        .subheader {
            font-size: 30px;
            font-weight: bold;
            color: #00eaff;
        }
        .movie-details {
            font-size: 18px;
            font-weight: normal;
            color: #f0f0f0;
        }
        .review-author {
            font-size: 18px;
            font-weight: bold;
            color: #ffcc00;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Function to get movie details
def get_cast_details(cast_id):
    """Fetch detailed information about a cast member from TMDb."""
    url = f"https://api.themoviedb.org/3/person/{cast_id}?api_key={API_KEY}"
    details = requests.get(url).json()
    
    return {
        "name": details.get("name"),
        "profile": f"https://image.tmdb.org/t/p/w300{details['profile_path']}" if details.get("profile_path") else "https://via.placeholder.com/150?text=No+Image",
        "biography": details.get("biography", "No biography available."),
        "birthday": details.get("birthday", "N/A"),
        "place_of_birth": details.get("place_of_birth", "N/A"),
        "known_for": details.get("known_for_department", "N/A"),
    }

def get_movie_data(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    res = requests.get(url).json()
    
    if not res["results"]:
        return None

    movie = res["results"][0]
    
    # Get movie metadata
    metadata_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={API_KEY}"
    metadata = requests.get(metadata_url).json()
    
    # Get movie cast
    cast_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key={API_KEY}"
    cast = requests.get(cast_url).json().get("cast", [])[:10]
    
    # Get reviews
    reviews_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/reviews?api_key={API_KEY}"
    reviews = requests.get(reviews_url).json().get("results", [])[:5]
    
    # Get recommendations
    rec_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/recommendations?api_key={API_KEY}"
    recommendations = requests.get(rec_url).json().get("results", [])[:5]
    
    return {
        "id": movie["id"],
        "title": movie["title"],
        "overview": movie["overview"],
        "release_date": movie["release_date"],
        "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
        "backdrop": f"https://image.tmdb.org/t/p/original{movie['backdrop_path']}" if movie.get("backdrop_path") else None,
        "budget": metadata.get("budget", 0),
        "revenue": metadata.get("revenue", 0),
        "cast": cast,
        "reviews": reviews,
        "recommendations": recommendations
    }

# Streamlit UI
st.title("🎬 Movie Recommendation System")

# User input
movie_name = st.text_input("Enter a movie name", "")

if st.button("Get Movie Details"):
    if movie_name:
        st.session_state["current_movie"] = get_movie_data(movie_name)

# Fetch and display movie details
if "current_movie" in st.session_state and st.session_state["current_movie"]:
    movie_data = st.session_state["current_movie"]

    st.subheader(movie_data["title"])
    if movie_data["backdrop"]:
        st.image(movie_data["backdrop"], use_container_width=True)

    st.write(f"**Overview:** {movie_data['overview']}")
    st.write(f"**Release Date:** {movie_data['release_date']}")
    st.write(f"**Budget:** ${movie_data['budget']:,.0f}")
    st.write(f"**Revenue:** ${movie_data['revenue']:,.0f}")

    # Show Cast
    # Show Cast
    st.subheader("🎭 Cast")
    if movie_data["cast"]:  # Ensure cast exists
        cast_cols = st.columns(5)  # Display 5 cast members per row
        for i, member in enumerate(movie_data["cast"]):
            with cast_cols[i % 5]:  # Distribute cast members across columns
                profile_img = f"https://image.tmdb.org/t/p/w200{member['profile_path']}" if member.get("profile_path") else "https://via.placeholder.com/100?text=No+Image"
                st.image(profile_img, width=100)
                if st.button(member["name"], key=f"cast_{member['id']}"):  # Clickable name
                    st.session_state["selected_cast"] = get_cast_details(member["id"])  # Store details
                    st.rerun()
    else:
        st.write("No cast information available.")
# Display cast details when clicked
    # Display cast details when clicked
    if "selected_cast" in st.session_state:
        cast_member = st.session_state["selected_cast"]
        
        st.subheader(f"🎭 {cast_member['name']}")
        
        # Display profile image
        st.image(cast_member["profile"], width=150)
        
        # Display biography and other details
        st.write(f"**Known For:** {cast_member['known_for']}")
        st.write(f"**Birthday:** {cast_member['birthday']}")
        st.write(f"**Place of Birth:** {cast_member['place_of_birth']}")
        
        # Biography (Expandable)
        with st.expander("📜 Biography"):
            st.write(cast_member["biography"])



    # Show Reviews
    # Show Reviews
    st.subheader("📝 Reviews")
    if movie_data["reviews"]:  # Ensure reviews exist
        for review in movie_data["reviews"]:
            st.write(f"**{review['author']}**: {review['content'][:300]}...")  # Show 300 characters
            with st.expander("Read more"):  # Expand for full review
                st.write(review['content'])
    else:
        st.write("No reviews available for this movie.")


    # Show Recommendations (Clickable and Row-based)
    st.subheader("📌 Recommended Movies")
    rec_movies = movie_data["recommendations"]

    if rec_movies:
        rec_cols = st.columns(5)  # Display 5 recommendations per row
        for i, rec in enumerate(rec_movies):
            with rec_cols[i % 5]:
                rec_poster = f"https://image.tmdb.org/t/p/w200{rec['poster_path']}" if rec.get("poster_path") else None
                if rec_poster:
                    st.image(rec_poster, width=100)
                if st.button(rec["title"], key=f"rec_{rec['id']}"):
                    st.session_state["current_movie"] = get_movie_data(rec["title"])
                    st.rerun()  # Refresh page to show new movie data
