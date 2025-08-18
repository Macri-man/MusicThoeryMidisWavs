import os
import random
import pretty_midi

BASE_DIR = "MIDILib_Library"

# ----------------------
# Roots & Note Numbers
# ----------------------
ROOTS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NUMS = {note: 60 + i for i, note in enumerate(ROOTS)}

# ----------------------
# Chords
# ----------------------
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

# ----------------------
# Scales & Modes
# ----------------------
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

# ----------------------
# Progressions
# ----------------------
PROGRESSIONS = {
    "pop_I_V_vi_IV": ["I", "V", "vi", "IV"],
    "blues_I_IV_V": ["I", "IV", "V"],
    "jazz_ii_V_I": ["ii", "V", "I"]
}
ROMAN_TO_CHORD = {
    "I": (0, "major"),
    "ii": (2, "minor"),
    "iii": (4, "minor"),
    "IV": (5, "major"),
    "V": (7, "major"),
    "vi": (9, "minor"),
    "vii°": (11, "diminished")
}

# ----------------------
# Rhythm & Velocity
# ----------------------
VELOCITIES = [60, 80, 100, 120]
VELOCITY_PATTERNS = {
    "soft": [60, 70, 65, 75],
    "medium": [80, 90, 85, 95],
    "loud": [100, 110, 105, 115],
    "random": VELOCITIES
}
RHYTHM_PATTERNS = {
    "straight": [1],
    "swing": [0.66, 0.34],
    "arpeggio": [0.5]
}

# ----------------------
# Helpers
# ----------------------
def chord_inversions(formula):
    return [formula[i:] + [n + 12 for n in formula[:i]] for i in range(len(formula))]

def create_midi(notes, filename, durations=None, velocity=100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program("Acoustic Grand Piano"))
    time = 0.0
    if durations is None:
        durations = [1] * len(notes)
    for i, note in enumerate(notes):
        inst.notes.append(pretty_midi.Note(
            velocity=velocity,
            pitch=note,
            start=time,
            end=time + durations[i % len(durations)]
        ))
        time += durations[i % len(durations)]
    pm.instruments.append(inst)
    pm.write(filename)

# ----------------------
# Generate Scales + Modes + Arpeggios
# ----------------------
for scale_name, intervals in SCALE_INTERVALS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        # Scale
        scale_notes = [root_midi + i for i in intervals]
        create_midi(scale_notes, os.path.join(BASE_DIR, "Scales", scale_name, root_name, f"{root_name}_{scale_name}.mid"))

        # Modes
        for mode_name, mode_intervals in SCALE_INTERVALS.items():
            mode_notes = [root_midi + i for i in mode_intervals]
            create_midi(mode_notes, os.path.join(BASE_DIR, "Scales", scale_name, root_name, "Modes", mode_name, f"{root_name}_{mode_name}.mid"))

        # Arpeggio
        arp_notes = scale_notes[::2]
        create_midi(arp_notes, os.path.join(BASE_DIR, "Scales", scale_name, root_name, "Arpeggios", f"{root_name}_{scale_name}_arp.mid"))

# ----------------------
# Generate Chords + Inversions
# ----------------------
for chord_name, intervals in CHORD_FORMULAS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        inversions = chord_inversions(intervals)
        for inv_num, inv_formula in enumerate(inversions):
            inv_notes = [root_midi + n for n in inv_formula]
            create_midi(inv_notes, os.path.join(BASE_DIR, "Chords", chord_name, f"Inversion_{inv_num}", f"{root_name}_{chord_name}_inv{inv_num}.mid"))

# ----------------------
# Generate Progressions (Full Sequences)
# ----------------------
for prog_name, roman_seq in PROGRESSIONS.items():
    for root_name, root_midi in NOTE_NUMS.items():
        for rhythm_name, rhythm_durations in RHYTHM_PATTERNS.items():
            for vel_pattern, vel_values in VELOCITY_PATTERNS.items():
                filename = os.path.join(BASE_DIR, "Progressions", prog_name, root_name, f"{root_name}_{prog_name}_{rhythm_name}_{vel_pattern}.mid")
                os.makedirs(os.path.dirname(filename), exist_ok=True)

                pm = pretty_midi.PrettyMIDI()
                inst = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program("Acoustic Grand Piano"))
                time = 0.0

                for roman in roman_seq:
                    interval, chord_type = ROMAN_TO_CHORD[roman]
                    chord_notes = [root_midi + interval + n for n in CHORD_FORMULAS[chord_type]]

                    if rhythm_name == "arpeggio":
                        note_length = 0.5
                        for i, note in enumerate(chord_notes):
                            vel = random.choice(vel_values) if vel_pattern == "random" else vel_values[i % len(vel_values)]
                            inst.notes.append(pretty_midi.Note(velocity=vel, pitch=note, start=time + i * note_length, end=time + (i + 1) * note_length))
                        time += note_length * len(chord_notes)
                    else:
                        duration = sum(rhythm_durations)
                        for i, note in enumerate(chord_notes):
                            vel = random.choice(vel_values) if vel_pattern == "random" else vel_values[i % len(vel_values)]
                            inst.notes.append(pretty_midi.Note(velocity=vel, pitch=note, start=time, end=time + duration))
                        time += duration

                pm.instruments.append(inst)
                pm.write(filename)

print("✅ All MIDI files generated in", BASE_DIR)
