# complete_music_library_generator.py
import pretty_midi
import os
import random

# ----------------------
# Folder Structure
# ----------------------
BASE_DIR = "Complete_MIDI_Library"
SCALES_DIR = os.path.join(BASE_DIR, "Scales")
CHORDS_DIR = os.path.join(BASE_DIR, "Chords")
ARPEGGIOS_DIR = os.path.join(BASE_DIR, "Arpeggios")
PROGRESSIONS_DIR = os.path.join(BASE_DIR, "Progressions")

for folder in [BASE_DIR, SCALES_DIR, CHORDS_DIR, ARPEGGIOS_DIR, PROGRESSIONS_DIR]:
    os.makedirs(folder, exist_ok=True)

ROOTS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for root in ROOTS:
    for main_folder in [SCALES_DIR, CHORDS_DIR, ARPEGGIOS_DIR, PROGRESSIONS_DIR]:
        os.makedirs(os.path.join(main_folder, root), exist_ok=True)

# ----------------------
# Music Theory Data
# ----------------------
NOTE_NUMS = {
    "C": 60, "C#": 61, "D": 62, "D#": 63,
    "E": 64, "F": 65, "F#": 66, "G": 67,
    "G#": 68, "A": 69, "A#": 70, "B": 71
}

CHORD_FORMULAS = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "augmented": [0, 4, 8],
    "major7": [0, 4, 7, 11],
    "minor7": [0, 3, 7, 10],
    "dominant7": [0, 4, 7, 10],
    "major9": [0, 4, 7, 11, 14],
    "minor9": [0, 3, 7, 10, 14],
    "dominant9": [0, 4, 7, 10, 14]
}

SCALE_INTERVALS = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10]
}

# ----------------------
# Utility Functions
# ----------------------
def build_notes(root, intervals):
    root_midi = NOTE_NUMS[root]
    return [root_midi + i for i in intervals]

def invert_chord(notes, inversion=0):
    n = notes.copy()
    for _ in range(inversion):
        n[0] += 12
        n = n[1:] + [n[0]]
    return sorted(n)

def write_midi(notes, filename, quarter_length=1):
    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)
    time = 0
    for n in notes:
        piano.notes.append(pretty_midi.Note(100, n, time, time + quarter_length))
        time += quarter_length
    pm.instruments.append(piano)
    pm.write(filename)

# ----------------------
# Generation Functions
# ----------------------
def generate_scales(octaves=2):
    for root in ROOTS:
        root_folder = os.path.join(SCALES_DIR, root)
        for scale_name, intervals in SCALE_INTERVALS.items():
            notes = build_notes(root, intervals)
            filename = os.path.join(root_folder, f"{scale_name}.mid")
            write_midi(notes * octaves, filename)
            print(f"Saved scale: {filename}")

def generate_chords_and_arpeggios(bars=16):
    for root in ROOTS:
        root_chord_folder = os.path.join(CHORDS_DIR, root)
        root_arp_folder = os.path.join(ARPEGGIOS_DIR, root)
        for chord_name, formula in CHORD_FORMULAS.items():
            notes = build_notes(root, formula)
            # Save chord
            chord_file = os.path.join(root_chord_folder, f"{chord_name}.mid")
            write_midi(notes, chord_file)
            # Generate arpeggio
            inversions = [invert_chord(notes, i) for i in range(len(notes))]
            arpeggio_notes = []
            total_notes = bars * 4
            idx = 0
            while idx < total_notes:
                for inv in inversions:
                    for n in inv:
                        if idx >= total_notes:
                            break
                        arpeggio_notes.append(n)
                        idx += 1
            arp_file = os.path.join(root_arp_folder, f"{chord_name}_arpeggio.mid")
            write_midi(arpeggio_notes, arp_file)
            print(f"Saved chord & arpeggio: {chord_name} ({root})")

def generate_example_progressions(bars_per_chord=4):
    example_progressions = [
        ["C", "F", "G", "C"],
        ["Am", "Dm", "G", "C"],
        ["C", "Am", "F", "G"]
    ]
    for root in ROOTS:
        root_folder = os.path.join(PROGRESSIONS_DIR, root)
        for i, prog in enumerate(example_progressions):
            notes = []
            for chord_root in prog:
                chord_type = random.choice(list(CHORD_FORMULAS.keys()))
                chord_notes = build_notes(chord_root[0], CHORD_FORMULAS[chord_type])
                for n in chord_notes:
                    notes.append(n)
            filename = os.path.join(root_folder, f"progression_{i+1}.mid")
            write_midi(notes, filename, quarter_length=bars_per_chord)
            print(f"Saved progression: {filename}")

# ----------------------
# Generate Full Library
# ----------------------
generate_scales()
generate_chords_and_arpeggios()
generate_example_progressions()
print("Complete MIDI practice library generated in organized folders.")
