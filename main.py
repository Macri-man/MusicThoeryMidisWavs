# midi_chords_inversions_arpeggios.py
import pretty_midi
import os

# Folders
CHORD_DIR = "midi_chords"
ARPEGGIO_DIR = "midi_arpeggios"
os.makedirs(CHORD_DIR, exist_ok=True)
os.makedirs(ARPEGGIO_DIR, exist_ok=True)

# Notes
NOTE_NUMS = {
    "C": 60, "C#": 61, "D": 62, "D#": 63,
    "E": 64, "F": 65, "F#": 66, "G": 67,
    "G#": 68, "A": 69, "A#": 70, "B": 71
}

# Chord formulas in semitones
CHORD_TYPES = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "augmented": [0, 4, 8]
}

ROOTS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def build_chord(root, formula):
    root_midi = NOTE_NUMS[root]
    return [root_midi + interval for interval in formula]

def invert_chord(notes, inversion=0):
    """Move the lowest note(s) up an octave for inversion"""
    n = notes.copy()
    for _ in range(inversion):
        n[0] += 12
        n = n[1:] + [n[0]]
    return sorted(n)

def create_chord_midi(root, chord_type, notes):
    """Single file with all inversions as 16-bar arpeggio"""
    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)
    time = 0
    beats_per_bar = 4
    total_bars = 16
    total_notes = beats_per_bar * total_bars
    note_index = 0

    # Prepare all inversions
    inversions = [invert_chord(notes, i) for i in range(len(notes))]

    # Cycle through inversions
    while note_index < total_notes:
        for inv in inversions:
            for n in inv:
                if note_index >= total_notes:
                    break
                note = pretty_midi.Note(
                    velocity=100, pitch=n, start=time, end=time + 1
                )
                piano.notes.append(note)
                time += 1
                note_index += 1
            if note_index >= total_notes:
                break

    pm.instruments.append(piano)
    filename = f"{root}_{chord_type}.mid"
    pm.write(os.path.join(ARPEGGIO_DIR, filename))
    print(f"Saved {filename}")

# Generate all chords
for root in ROOTS:
    for ctype, formula in CHORD_TYPES.items():
        notes = build_chord(root, formula)
        create_chord_midi(root, ctype, notes)

print("All chord arpeggios with inversions created in", ARPEGGIO_DIR)
