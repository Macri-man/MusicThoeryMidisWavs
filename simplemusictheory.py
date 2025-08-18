import os
import pretty_midi

BASE_DIR = "MIDI_Library"

# ----------------------
# Main Category Folders
# ----------------------
FOLDERS = ["Scales", "Chords", "Modes", "Arpeggios", "Progressions", "Melodies"]

# ----------------------
# Roots
# ----------------------
ROOTS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# ----------------------
# Music Theory Data
# ----------------------
NOTE_NUMS = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
    "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71
}

# Extended Chord Formulas
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

# All Major/Minor Modes + Exotic
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

# Rhythm & Velocity Variations
RHYTHM_PATTERNS = {
    "straight": [1, 1, 1, 1],
    "syncopated": [0.75, 0.25, 1, 1],
    "triplet": [2/3, 2/3, 2/3],
    "swing": [0.66, 0.34, 0.66, 0.34]
}
VELOCITIES = [60, 80, 100, 120]

# ----------------------
# Helper Functions
# ----------------------
def chord_inversions(formula):
    """Generate all inversions for a chord formula."""
    inversions = []
    for i in range(len(formula)):
        inv = formula[i:] + [n + 12 for n in formula[:i]]
        inversions.append(inv)
    return inversions

CHORD_INVERSIONS = {name: chord_inversions(intervals)
                    for name, intervals in CHORD_FORMULAS.items()}


def create_midi(notes, filename, rhythm_pattern="straight", velocity=100, instrument_name="Acoustic Grand Piano"):
    """Generate a MIDI file from a list of MIDI note numbers."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program(instrument_name))
    time = 0.0
    durations = RHYTHM_PATTERNS.get(rhythm_pattern, [1])  # fallback to quarter notes

    for i, note_num in enumerate(notes):
        duration = durations[i % len(durations)]
        note = pretty_midi.Note(velocity=velocity,
                                pitch=note_num,
                                start=time,
                                end=time + duration)
        instrument.notes.append(note)
        time += duration

    pm.instruments.append(instrument)
    pm.write(filename)

# ----------------------
# Generate Scales + Modes + Arpeggios
# ----------------------
for scale_name, intervals in SCALE_INTERVALS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        # Scale notes
        scale_notes = [root_midi + interval for interval in intervals]
        scale_folder = os.path.join(BASE_DIR, "Scales", scale_name, root_name)

        # Save scale MIDI
        create_midi(scale_notes, os.path.join(scale_folder, f"{root_name}_{scale_name}.mid"))

        # Modes
        mode_folder = os.path.join(scale_folder, "Modes")
        for mode_name, mode_intervals in SCALE_INTERVALS.items():
            mode_notes = [root_midi + interval for interval in mode_intervals]
            create_midi(mode_notes, os.path.join(mode_folder, mode_name, f"{root_name}_{mode_name}.mid"))

        # Arpeggios (root, 3rd, 5th, 7th)
        arp_folder = os.path.join(scale_folder, "Arpeggios")
        arp_notes = scale_notes[::2]  # simple skip-1 arpeggio
        create_midi(arp_notes, os.path.join(arp_folder, f"{root_name}_{scale_name}_arpeggio.mid"))

# ----------------------
# Generate Chords + Inversions
# ----------------------
for chord_name, intervals in CHORD_FORMULAS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        chord_path = os.path.join(BASE_DIR, "Chords", chord_name)

        inversions = chord_inversions(intervals)
        for inv_num, inv_formula in enumerate(inversions):
            inv_notes = [root_midi + n for n in inv_formula]
            inv_folder = os.path.join(chord_path, f"Inversion_{inv_num}")
            create_midi(inv_notes, os.path.join(inv_folder, f"{root_name}_{chord_name}_inv{inv_num}.mid"))

print("✅ All MIDI files generated and saved into the library!")