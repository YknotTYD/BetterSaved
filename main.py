##streamlit_reddit_saved_filtering

import streamlit as st
from st_pages import hide_pages
import requests
import io
from PIL import Image
import reddit_saved_filtering as rsf

center_style="'display: block;margin-left: auto;margin-right: auto'"

def load_image(url):
    st.markdown(f"<img src={url} width=50% style={center_style}>",unsafe_allow_html=True)

def load_video(url):
    st.markdown(f"<video width=50% controls autoplay style={center_style}><source type='video/mp4' src='{url}'></video>",
                unsafe_allow_html=True)

def display_post(post):

    url=post.url
    if post.media:
        url=post.media["reddit_video"]["fallback_url"].rstrip("?source=fallback")

    print(url)

    st.markdown(f"<h3>u/{post.author} in r/{post.subreddit}: {post.title}</h3>",unsafe_allow_html=True)

    if url.endswith((".png",".jpeg",".gif")):
        load_image(url)
        return(None)

    if url.endswith((".mp4",)):
        load_video(url)

st.set_page_config(initial_sidebar_state="collapsed")

hide_pages(["main"])

st.sidebar.link_button("Github Repo","https://www.youtube.com/watch?v=dQw4w9WgXcQ")
st.title("Under 1 600 recipes to choose from.")

for i in range(2):
    text=st.text("")

if "logged_in" not in st.session_state:

    with st.form(key="login_form"):

        st.title("Enter both")

        username_input=st.text_input(label="Username",value="",max_chars=256)
        password_input=st.text_input(label="Password",value="",max_chars=256,type="password")

        submit_button=st.form_submit_button("Log In")

        if submit_button and username_input and password_input:

            with st.spinner("Trying to log into your account."):
                login=rsf.login(username=username_input,password=password_input)
            st.text(("✔️ ","❌ ")[login["failed"]]+login["message"])

            if not login["failed"]:

                with st.spinner("Loading saved posts."):
                    saved_load=rsf.load_saved(limit=None)
                st.text("✔️ Successfully loaded saved posts.")

                st.session_state.logged_in=True
                st.session_state.username=username_input
                st.session_state.password=password_input

                print("logged_in" in st.session_state)

                with st.spinner("Redirecting."):
                    st.experimental_rerun()

else:

    st.text(f"Logged in as u/{st.session_state.username}.")

    with st.form(key="filters"):

        filters={"in": {"subreddit": st.text_input(label="In sub name."),
                        "title": st.text_input(label="In title."),
                        "author": st.text_input(label="In author name.")}}

        button=st.form_submit_button(label="Search.")

        if button:

            print(filters)

            for post in rsf.get_saved(filters):

                display_post(post)

for i in range(13):
    text=st.text("")

st.text("© YknotTYD 2024")