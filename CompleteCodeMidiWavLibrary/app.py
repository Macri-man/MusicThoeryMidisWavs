import streamlit as st
import os
from musictheory.arranger import generate_song
from musictheory.config import NOTE_NUMS, GENRES

st.title("🎶 Simple Music Theory MIDI Generator")

root = st.selectbox("Choose root note:", list(NOTE_NUMS.keys()))
genre = st.selectbox("Choose genre:", list(GENRES.keys()))
if st.button("Generate Song"):
    out_file = f"{root}_{genre}.mid"
    generate_song(NOTE_NUMS[root], genre.lower(), out_file)
    st.success(f"Generated {out_file}")
    with open(out_file, "rb") as f:
        st.download_button("Download MIDI", f, file_name=out_file)
