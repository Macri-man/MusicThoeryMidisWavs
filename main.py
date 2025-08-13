# midi_scales_and_arpeggios.py
import pretty_midi
import os

# Folders
SCALE_DIR = "midi_scales"
ARPEGGIO_DIR = "midi_arpeggios"
os.makedirs(SCALE_DIR, exist_ok=True)
os.makedirs(ARPEGGIO_DIR, exist_ok=True)

# Note numbers for C4 = 60
NOTE_NUMS = {
    "C": 60, "C#": 61, "D": 62, "D#": 63,
    "E": 64, "F": 65, "F#": 66, "G": 67,
    "G#": 68, "A": 69, "A#": 70, "B": 71
}

# Major scale intervals (Ionian)
MAJOR_INTERVALS = [0, 2, 4, 5, 7, 9, 11]

def build_scale(root_note, intervals):
    """Return MIDI notes for a scale starting at root"""
    root_midi = NOTE_NUMS[root_note]
    return [root_midi + i for i in intervals]

def create_scale_midi(scale_name, notes, beats_per_note=1, octaves=1):
    """Create MIDI file for the scale"""
    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)
    time = 0
    for _ in range(octaves):
        for n in notes:
            note = pretty_midi.Note(
                velocity=100, pitch=n, start=time, end=time + beats_per_note
            )
            piano.notes.append(note)
            time += beats_per_note
    pm.instruments.append(piano)
    pm.write(os.path.join(SCALE_DIR, f"{scale_name}.mid"))
    print(f"Saved scale: {scale_name}.mid")

def create_arpeggio_midi(scale_name, notes, bars=16):
    """Create arpeggio MIDI file with triads from scale"""
    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)
    time = 0
    beats_per_bar = 4
    triads = []
    for i in range(len(notes) - 2):
        triads.append([notes[i], notes[i+1], notes[i+2]])
    note_index = 0
    total_notes = bars * beats_per_bar
    while note_index < total_notes:
        for triad in triads:
            for n in triad:
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
    pm.write(os.path.join(ARPEGGIO_DIR, f"{scale_name}_arpeggio.mid"))
    print(f"Saved arpeggio: {scale_name}_arpeggio.mid")

# Generate all modes of C major
ROOTS = ["C", "D", "E", "F", "G", "A", "B"]
for i, root in enumerate(ROOTS):
    # Mode intervals (rotate major scale)
    intervals = MAJOR_INTERVALS[i:] + [x + 12 for x in MAJOR_INTERVALS[:i]]
    scale_notes = build_scale(root, intervals)
    mode_name = f"{root}_mode"
    create_scale_midi(mode_name, scale_notes, beats_per_note=1, octaves=1)
    create_arpeggio_midi(mode_name, scale_notes, bars=16)

print("All modes and arpeggios created in folders:", SCALE_DIR, ARPEGGIO_DIR)
