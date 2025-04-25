import streamlit as st
import pickle as pkl
import pandas as pd

st.title("Movie Recommandation System")
st.subheader("Get reccomandation on the basis of your favorite movies!")
st.write("This app uses collaborative filtering model to recommend movies.")

ds = pd.read_csv("cleaned_data.csv")
similarity = pkl.load(open("similarity.pkl", "rb"))


def get_movie_index(name):
    movie_ds_index = -1
    for i in ds.index:
        if ds.loc[i, "title"].lower() == name.lower():
            movie_ds_index = i
            break
    return movie_ds_index



def get_movie_name(index):
    return ds.loc[index, "title"]



def get_movie_link(index):
    if "homepage" in ds.columns:
        return ds.loc[index, "homepage"]
    return "#"



def get_recommendation(name):
    mindex = get_movie_index(name)
    if mindex == -1:
        return []

    r_movies = []
    similarity_indexes = list(enumerate(similarity[mindex]))
    similarity_indexes = sorted(similarity_indexes, key=lambda x: x[1], reverse=True)
    
    for count in range(1, 6):
        index = similarity_indexes[count][0]
        title = get_movie_name(index)
        link = get_movie_link(index)
        r_movies.append((title, link))
    return r_movies

selected_movies = st.selectbox("Select Movies :", sorted(ds["title"]))

if st.button("Recommend Movies"):
    st.write("Recommended Movies: ")
    recommendations = get_recommendation(selected_movies)
    for title, homepage in recommendations:
        st.markdown(f"🔗 [{title}]({homepage})")
