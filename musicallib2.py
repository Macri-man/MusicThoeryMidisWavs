import os
import random
import pretty_midi

BASE_DIR = "MIDILib2_Library"

# ----------------------
# Music Theory Data
# ----------------------
NOTE_NUMS = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
    "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71
}

CHORD_FORMULAS = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "dominant7": [0, 4, 7, 10],
    "minor7": [0, 3, 7, 10],
    "major7": [0, 4, 7, 11],
    "augmented": [0, 4, 8],
    "diminished": [0, 3, 6],
    "half_dim7": [0, 3, 6, 10],
    "dim7": [0, 3, 6, 9],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "major6": [0, 4, 7, 9],
    "minor6": [0, 3, 7, 9],
    "9": [0, 4, 7, 10, 14],
    "minor9": [0, 3, 7, 10, 14],
    "maj9": [0, 4, 7, 11, 14],
    "13": [0, 4, 7, 10, 14, 17, 21]
}

SCALE_INTERVALS = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11]
}

RHYTHM_PATTERNS = {
    "straight": [1, 1, 1, 1],
    "syncopated": [0.75, 0.25, 1, 1],
    "triplet": [2/3, 2/3, 2/3],
    "swing": [0.66, 0.34, 0.66, 0.34]
}

VELOCITY_PATTERNS = {
    "soft": [60],
    "medium": [90],
    "hard": [120],
    "random": [60, 80, 100, 120]
}

# Common progressions (Roman numerals)
PROGRESSIONS = {
    "pop": ["I", "V", "vi", "IV"],
    "jazz_ii_V_I": ["ii", "V", "I"],
    "blues": ["I", "IV", "V", "I"],
    "minor_pop": ["i", "VI", "III", "VII"]
}

# Roman numeral mapping
ROMAN_TO_CHORD = {
    "I": (0, "major"),
    "ii": (2, "minor"),
    "iii": (4, "minor"),
    "IV": (5, "major"),
    "V": (7, "major"),
    "vi": (9, "minor"),
    "vii°": (11, "diminished"),
    "i": (0, "minor"),
    "III": (3, "major"),
    "VI": (8, "major"),
    "VII": (10, "major")
}

# ----------------------
# Helper
# ----------------------
def create_named_midi(track_data, filename):
    """Create MIDI with multiple tracks, each having its own name."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pm = pretty_midi.PrettyMIDI()
    for name, notes in track_data:
        inst = pretty_midi.Instrument(
            program=pretty_midi.instrument_name_to_program("Acoustic Grand Piano"),
            name=name
        )
        for pitch, start, end, velocity in notes:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=pitch, start=start, end=end
            ))
        pm.instruments.append(inst)
    pm.write(filename)

# ----------------------
# Generate Scales + Modes + Arpeggios
# ----------------------
for scale_name, intervals in SCALE_INTERVALS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        # Scale
        notes = [(root_midi + i, 0, 1, 100) for i in intervals]
        create_named_midi(
            [(f"{root_name}_{scale_name}_scale", [(n, 0, 1, 100) for n in [p for p,_,_,_ in notes]])],
            os.path.join(BASE_DIR, "Scales", scale_name, root_name, f"{root_name}_{scale_name}.mid")
        )

        # Modes
        for mode_name, mode_int in SCALE_INTERVALS.items():
            notes = [(root_midi + i, 0, 1, 100) for i in mode_int]
            create_named_midi(
                [(f"{root_name}_{mode_name}_mode", [(n, 0, 1, 100) for n in [p for p,_,_,_ in notes]])],
                os.path.join(BASE_DIR, "Scales", scale_name, root_name, "Modes", mode_name, f"{root_name}_{mode_name}.mid")
            )

        # Arpeggios
        arp_notes = intervals[::2]
        create_named_midi(
            [(f"{root_name}_{scale_name}_arpeggio", [(root_midi + i, i*0.5, (i+1)*0.5, 100) for i in arp_notes])],
            os.path.join(BASE_DIR, "Scales", scale_name, root_name, "Arpeggios", f"{root_name}_{scale_name}_arpeggio.mid")
        )

# ----------------------
# Generate Chords
# ----------------------
for chord_name, intervals in CHORD_FORMULAS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        notes = [(root_midi + i, 0, 2, 100) for i in intervals]
        create_named_midi(
            [(f"{root_name}_{chord_name}_chord", [(n, 0, 2, 100) for n in [p for p,_,_,_ in notes]])],
            os.path.join(BASE_DIR, "Chords", chord_name, f"{root_name}_{chord_name}.mid")
        )

# ----------------------
# Generate Progressions
# ----------------------
for prog_name, roman_seq in PROGRESSIONS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        track_data = []
        time = 0.0
        for roman in roman_seq:
            interval, chord_type = ROMAN_TO_CHORD[roman]
            chord_notes = [root_midi + interval + n for n in CHORD_FORMULAS[chord_type]]
            track_data.append(
                (f"{root_name}_{roman}_{chord_type}",
                 [(n, time, time+1, 100) for n in chord_notes])
            )
            time += 1
        create_named_midi(
            track_data,
            os.path.join(BASE_DIR, "Progressions", prog_name, root_name, f"{root_name}_{prog_name}.mid")
        )

print("✅ MIDI Library with track labels generated!")
