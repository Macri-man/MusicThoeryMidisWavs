import streamlit as st
import os
import tempfile
import time
from musictheory.arranger import generate_song
from musictheory.config import NOTE_NUMS, GENRES

st.title("🎶 Simple Music Theory MIDI Generator")

root = st.selectbox("Choose root note:", list(NOTE_NUMS.keys()))
genre = st.selectbox("Choose genre:", list(GENRES.keys()))

if st.button("Generate Song"):
    try:
        # Create a temporary output file
        timestamp = int(time.time())
        out_file = f"{root}_{genre}_{timestamp}.mid"
        temp_path = os.path.join(tempfile.gettempdir(), out_file)

        # Generate MIDI
        generate_song(NOTE_NUMS[root], genre.lower(), temp_path)

        st.success(f"Generated: {out_file}")

        with open(temp_path, "rb") as f:
            st.download_button(
                "⬇️ Download MIDI",
                f,
                file_name=out_file,
                mime="audio/midi"
            )

    except Exception as e:
        st.error(f"Error generating song: {e}")
