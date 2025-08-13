# midi_chords_arpeggios_quarters.py
import pretty_midi
import os

# Output folder
OUTPUT_DIR = "midi_chords_arpeggios_quarters"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Basic triads
CHORDS = {
    "C": ["C", "E", "G"],
    "D": ["D", "F#", "A"],
    "E": ["E", "G#", "B"],
    "F": ["F", "A", "C"],
    "G": ["G", "B", "D"],
    "A": ["A", "C#", "E"],
    "B": ["B", "D#", "F#"]
}

NOTE_NUMS = {
    "C": 60, "C#": 61, "D": 62, "D#": 63,
    "E": 64, "F": 65, "F#": 66, "G": 67,
    "G#": 68, "A": 69, "A#": 70, "B": 71
}

def chord_to_midi_notes(chord_notes, start_octave=4):
    return [NOTE_NUMS[n] + (start_octave - 4) * 12 for n in chord_notes]

def invert_chord(midi_notes, inversion=0):
    """Return chord inversion, moving lowest note up an octave per inversion"""
    notes = midi_notes.copy()
    for _ in range(inversion):
        notes[0] += 12
        notes = notes[1:] + [notes[0]]
    return sorted(notes)

def create_arpeggio_midi_quarters(chord_name, chord_notes, bars=16, beats_per_bar=4):
    """Create a single MIDI file with quarter-note arpeggio cycles"""
    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)

    midi_notes = chord_to_midi_notes(chord_notes)
    time = 0.0  # start time in beats

    inversions = [invert_chord(midi_notes, inv) for inv in range(len(chord_notes))]
    total_notes = bars * beats_per_bar
    note_index = 0

    # Cycle through inversions
    while note_index < total_notes:
        for inv in inversions:
            for note_number in inv:
                if note_index >= total_notes:
                    break
                note = pretty_midi.Note(
                    velocity=100,
                    pitch=note_number,
                    start=time,
                    end=time + 1  # quarter note
                )
                piano.notes.append(note)
                time += 1
                note_index += 1
            if note_index >= total_notes:
                break

    pm.instruments.append(piano)
    filename = f"{chord_name}_arpeggio_quarters.mid"
    pm.write(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved {filename}")

# Generate for all chords
for name, notes in CHORDS.items():
    create_arpeggio_midi_quarters(name, notes)

print("All MIDI arpeggios (quarter notes, 16 bars) created in", OUTPUT_DIR)
