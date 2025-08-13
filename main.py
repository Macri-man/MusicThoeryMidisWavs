# midi_chords_arpeggios.py
import pretty_midi
import os

# Output folder
OUTPUT_DIR = "midi_chords_arpeggios"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define basic triads (C major to B major)
CHORDS = {
    "C": ["C", "E", "G"],
    "D": ["D", "F#", "A"],
    "E": ["E", "G#", "B"],
    "F": ["F", "A", "C"],
    "G": ["G", "B", "D"],
    "A": ["A", "C#", "E"],
    "B": ["B", "D#", "F#"]
}

# MIDI note numbers for C4 = 60
NOTE_NUMS = {
    "C": 60,
    "C#": 61,
    "D": 62,
    "D#": 63,
    "E": 64,
    "F": 65,
    "F#": 66,
    "G": 67,
    "G#": 68,
    "A": 69,
    "A#": 70,
    "B": 71
}

def chord_to_midi_notes(chord_notes, start_octave=4):
    return [NOTE_NUMS[note] + (start_octave - 4) * 12 for note in chord_notes]

def invert_chord(midi_notes, inversion=0):
    """Return chord inversion, moving lowest note up an octave per inversion"""
    notes = midi_notes.copy()
    for _ in range(inversion):
        notes[0] += 12
        notes = notes[1:] + [notes[0]]
    return sorted(notes)

def create_arpeggio_midi(chord_name, chord_notes, beats_per_bar=4):
    """Create a single MIDI file with all inversions as 4-bar arpeggios"""
    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)  # Acoustic grand piano

    midi_notes = chord_to_midi_notes(chord_notes)
    time = 0  # start time in seconds

    for inv in range(len(chord_notes)):
        inverted = invert_chord(midi_notes, inversion=inv)
        for note_number in inverted:
            note = pretty_midi.Note(
                velocity=100,
                pitch=note_number,
                start=time,
                end=time + beats_per_bar  # 1 bar per inversion
            )
            piano.notes.append(note)
        time += beats_per_bar  # move to next bar

    pm.instruments.append(piano)
    filename = f"{chord_name}_arpeggio.mid"
    pm.write(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved {filename}")

# Generate MIDI files for all chords
for name, notes in CHORDS.items():
    create_arpeggio_midi(name, notes)

print("All MIDI arpeggios created in", OUTPUT_DIR)
