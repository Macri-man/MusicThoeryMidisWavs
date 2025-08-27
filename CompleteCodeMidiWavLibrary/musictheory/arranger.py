import random, os
from .config import *
from .utils import create_named_midi
from .theory import roman_to_midi_progression

def drum_track_for_genre(genre, bars, velocity=90):
    groove = DRUM_GROOVES.get(genre, DRUM_GROOVES["pop"])
    notes = []
    for bar in range(bars):
        for name, pos in groove:
            pitch = DRUMS[name]
            start = bar*4.0 + pos
            notes.append((pitch, start, start+0.1, velocity))
    return notes

def bass_track_for_genre(chords_by_bar, genre, base_vel=88):
    pattern = BASS_PATTERNS.get(genre, BASS_PATTERNS["pop"])
    notes, time = [], 0.0
    for chord in chords_by_bar:
        root = min(chord) - 12
        for interval in pattern:
            pitch = root + interval
            notes.append((pitch, time, time+1.0, base_vel))
            time += 1.0
    return notes

def generate_melody(chords_by_bar, scale_intervals, root_midi):
    melody, time = [], 0.0
    scale_notes = [root_midi+i for i in scale_intervals]
    for chord in chords_by_bar:
        chord_tone = random.choice(chord[:3])
        melody.append((chord_tone, time, time+0.5, 102)); time+=0.5
        melody.append((random.choice(scale_notes), time, time+0.5, 96)); time+=0.5
        for _ in range(2):
            melody.append((random.choice(scale_notes), time, time+0.5, 94)); time+=0.5
    return melody

def generate_song(root_midi, genre, filename):
    structure = SONG_STRUCTURES.get(genre, SONG_STRUCTURES["pop"])
    midi_tracks, current_time = [], 0.0
    scale = SCALE_INTERVALS["major"]

    for section in structure:
        roman_prog = SECTION_PROGS.get(section, SECTION_PROGS["verse"])
        chords = roman_to_midi_progression(roman_prog, root_midi)

        piano = [(n, t+current_time, t+1+current_time, 90) for t,n in enumerate(chords[0])]
        bass  = [(n, t+current_time, t+1+current_time, 80) for t,n in enumerate(chords[0])]
        drums = drum_track_for_genre(genre, len(chords))
        melody = generate_melody(chords, scale, root_midi)

        midi_tracks.extend([
            (f"{section}_piano", piano, False),
            (f"{section}_bass", bass, False),
            (f"{section}_drums", drums, True),
            (f"{section}_melody", melody, False),
        ])
        current_time += len(chords)

    create_named_midi(midi_tracks, filename)
    print(f"🎼 Song created: {filename}")


# arrangement.py
# This file contains a function to generate MIDI files for each genre configuration
# defined in config.py, with each file saved in a genre-specific subfolder for
# organization. It assumes config.py is in the same directory and imports the
# necessary dictionaries. The script generates basic MIDI arrangements including
# chords, a simple melody, bass, and drums based on the genre defaults, using
# midiutil for MIDI generation.

# Note: To run this, ensure midiutil is installed (pip install midiutil).
# The generated MIDI files will be saved in genre-specific subfolders under
# the specified output directory.

import os
from midiutil import MIDIFile
from config import (GENRE_DEFAULTS, GENRES, PROGRESSIONS, ROMAN_TO_CHORD,
                    CHORD_FORMULAS, SCALE_INTERVALS, DRUM_GROOVES,
                    BASS_PATTERNS, DRUMS, GENRE_TEMPOS, ROOTS, NOTE_NUMS,
                    SONG_STRUCTURES, SECTION_PROGS, GENRE_INSTRUMENTS)

def generate_midi_for_genres(output_dir='midi_arrangements'):
    """
    Generates a MIDI file for each genre in GENRE_DEFAULTS, saved in a subfolder
    named after the genre. Each MIDI file includes:
    - Song structure based on genre.
    - Chord progressions for sections.
    - Simple melody generated from the major scale.
    - Bass line using genre-specific patterns.
    - Drum groove looped throughout.
    - Instruments and tempo based on genre.
    - Basic expressions (velocity jitter for humanization).

    Args:
        output_dir (str): Base directory to save genre-specific subfolders and MIDI files.

    Returns:
        list: List of generated MIDI file paths.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generated_files = []

    for genre, data in GENRE_DEFAULTS.items():
        # Create genre-specific subfolder
        genre_dir = os.path.join(output_dir, genre.lower())
        if not os.path.exists(genre_dir):
            os.makedirs(genre_dir)

        # Setup MIDI file with multiple tracks
        num_tracks = 4  # Track 0: Chords, 1: Melody, 2: Bass, 3: Drums
        midi = MIDIFile(num_tracks, file_format=1)

        # Set tempo (random within genre range)
        import random
        tempo_min, tempo_max = GENRE_TEMPOS.get(genre.lower(), (80, 120))
        tempo = random.randint(tempo_min, tempo_max)
        time = 0.0
        for track in range(num_tracks):
            midi.addTempo(track, time, tempo)

        # Set instruments (using GM program numbers)
        instruments = GENRE_INSTRUMENTS.get(genre.lower(), {"piano": 0, "bass": 33, "melody": 81})
        chord_instrument = list(instruments.values())[0] if instruments else 0  # Piano default
        melody_instrument = instruments.get("melody", 81)  # Lead synth
        bass_instrument = instruments.get("bass", 33)  # Acoustic bass

        midi.addProgramChange(0, 0, time, chord_instrument)  # Chords track
        midi.addProgramChange(1, 1, time, melody_instrument)  # Melody track
        midi.addProgramChange(2, 2, time, bass_instrument)   # Bass track
        # Drums on channel 10 (standard MIDI percussion channel)
        midi.addProgramChange(3, 9, time, 0)  # Drums don't need program change

        # Choose key (random root)
        root_note = random.choice(ROOTS)
        root_midi = NOTE_NUMS[root_note]
        scale = [root_midi + i for i in SCALE_INTERVALS["major"]]  # Default to major scale

        # Get structure
        structure = data["structure"] or SONG_STRUCTURES.get(genre.lower(), ["verse", "chorus"])

        # Get drum groove
        drum_groove = DRUM_GROOVES.get(genre.lower(), DRUM_GROOVES["pop"])
        drum_cycle_length = max(pos for _, pos in drum_groove) + 1 if drum_groove else 4.0

        # Get bass pattern
        bass_pattern = BASS_PATTERNS.get(genre.lower(), [0, 0, 0, 0])

        # Expressions: humanization
        expressions = data["expressions"]
        velocity_jitter = expressions.get("humanization", {}).get("velocity_jitter", 0.05)
        base_velocity = 100  # mf default

        # Loop through song structure
        bar_duration = 4.0  # Assuming 4/4 time
        current_time = 0.0
        section_index = 0

        for section in structure:
            # Get progression for section (fallback to genre default)
            prog = SECTION_PROGS.get(section, PROGRESSIONS.get(GENRES[genre][0] if genre in GENRES else "pop_axis"))

            for roman in prog:
                # Get chord
                if roman in ROMAN_TO_CHORD:
                    shift, chord_type = ROMAN_TO_CHORD[roman]
                else:
                    continue  # Skip invalid

                chord_root = (root_midi + shift) % 12 + 48  # Middle range
                formula = CHORD_FORMULAS.get(chord_type, [0, 4, 7])
                chord_notes = [chord_root + interval for interval in formula]

                # Add chords (whole bar duration)
                for note in chord_notes:
                    vel = int(base_velocity * (1 + random.uniform(-velocity_jitter, velocity_jitter)))
                    midi.addNote(0, 0, note, current_time, bar_duration, vel)

                # Add bass (using pattern, quarter notes)
                bass_root = chord_root - 12  # Octave down
                for i, interval in enumerate(bass_pattern):
                    bass_note = bass_root + interval
                    bass_time = current_time + i
                    if bass_time < current_time + bar_duration:
                        vel = int(base_velocity * (1 + random.uniform(-velocity_jitter, velocity_jitter)))
                        midi.addNote(2, 2, bass_note, bass_time, 1.0, vel)

                # Add simple melody (random notes from scale, eighth notes)
                for i in range(8):  # 8 eighth notes per bar
                    melody_note = random.choice(scale) + 12  # Higher octave
                    melody_time = current_time + i * 0.5
                    duration = 0.5
                    vel = int(base_velocity * (1 + random.uniform(-velocity_jitter, velocity_jitter)))
                    midi.addNote(1, 1, melody_note, melody_time, duration, vel)

                # Add drums (loop groove over the bar)
                for drum_name, pos in drum_groove:
                    while pos < bar_duration:
                        drum_pitch = DRUMS.get(drum_name, 36)  # Default kick
                        drum_time = current_time + pos
                        vel = int(base_velocity * (1 + random.uniform(-velocity_jitter, velocity_jitter)))
                        midi.addNote(3, 9, drum_pitch, drum_time, 0.1, vel)  # Short duration for perc
                        pos += drum_cycle_length  # Loop if needed

                current_time += bar_duration

            section_index += 1

        # Write MIDI file to genre subfolder
        filename = f"{genre.lower()}_arrangement.mid"
        filepath = os.path.join(genre_dir, filename)
        with open(filepath, 'wb') as outf:
            midi.writeFile(outf)
        generated_files.append(filepath)

    return generated_files

# Example usage:
# if __name__ == "__main__":
#     files = generate_midi_for_genres()
#     print(f"Generated files: {files}")