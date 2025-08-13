# rhythmic_piano_midi_generator.py
import pretty_midi
import os
import random

# ----------------------
# Folder Structure
# ----------------------
BASE_DIR = "Rhythmic_Piano_MIDI"
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

RHYTHM_VALUES = [0.5, 1, 1.5, 2]  # eighth, quarter, dotted, half notes

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

def write_two_hand_midi(left_notes, right_notes, filename):
    pm = pretty_midi.PrettyMIDI()
    left = pretty_midi.Instrument(program=0)
    right = pretty_midi.Instrument(program=0)
    
    time = 0
    idx_left, idx_right = 0, 0
    while idx_left < len(left_notes) or idx_right < len(right_notes):
        if idx_left < len(left_notes):
            note, duration = left_notes[idx_left]
            left.notes.append(pretty_midi.Note(90, note, time, time + duration))
            time += duration
            idx_left += 1
        if idx_right < len(right_notes):
            note, duration = right_notes[idx_right]
            right.notes.append(pretty_midi.Note(100, note, time, time + duration))
            idx_right += 1
    pm.instruments.extend([left, right])
    pm.write(filename)

# ----------------------
# Generation Functions
# ----------------------
def generate_rhythmic_chords_arpeggios(bars=16):
    for root in ROOTS:
        chord_folder = os.path.join(CHORDS_DIR, root)
        arp_folder = os.path.join(ARPEGGIOS_DIR, root)
        for chord_name, formula in CHORD_FORMULAS.items():
            notes = build_notes(root, formula)
            
            # Chord notes (right hand) with rhythms
            right_notes = []
            total_quarters = bars * 4
            idx = 0
            while idx < total_quarters:
                duration = random.choice(RHYTHM_VALUES)
                for n in notes:
                    right_notes.append((n, duration))
                    idx += duration
            
            # Left hand root/bass notes
            left_notes = []
            idx = 0
            while idx < total_quarters:
                duration = random.choice(RHYTHM_VALUES)
                left_notes.append((notes[0]-12, duration))  # one octave below
                idx += duration
            
            # Write MIDI
            filename = os.path.join(chord_folder, f"{chord_name}_two_hand.mid")
            write_two_hand_midi(left_notes, right_notes, filename)
            print(f"Saved two-hand chord MIDI: {chord_name} ({root})")

# ----------------------
# Generate Everything
# ----------------------
generate_rhythmic_chords_arpeggios()
print("Two-hand rhythmic MIDI files generated in organized folders.")
