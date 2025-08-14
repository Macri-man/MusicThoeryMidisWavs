import os

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

# ----------------------
# Create Folder Structure
# ----------------------
os.makedirs(BASE_DIR, exist_ok=True)

# Main folders
for f in FOLDERS:
    folder_path = os.path.join(BASE_DIR, f)
    os.makedirs(folder_path, exist_ok=True)

# Scales → each scale name → each root → modes + arpeggios
for scale_name in SCALE_INTERVALS:
    scale_path = os.path.join(BASE_DIR, "Scales", scale_name)
    os.makedirs(scale_path, exist_ok=True)

    for root in ROOTS:
        root_path = os.path.join(scale_path, root)
        os.makedirs(root_path, exist_ok=True)

        # Modes inside each root
        mode_folder = os.path.join(root_path, "Modes")
        os.makedirs(mode_folder, exist_ok=True)
        for mode_name in SCALE_INTERVALS:
            os.makedirs(os.path.join(mode_folder, mode_name), exist_ok=True)

        # Arpeggios inside each root
        arp_folder = os.path.join(root_path, "Arpeggios")
        os.makedirs(arp_folder, exist_ok=True)

# Chords → each chord → each inversion
for chord_name in CHORD_FORMULAS:
    chord_path = os.path.join(BASE_DIR, "Chords", chord_name)
    os.makedirs(chord_path, exist_ok=True)

    for inversion_num in range(len(CHORD_FORMULAS[chord_name])):
        os.makedirs(os.path.join(chord_path, f"Inversion_{inversion_num}"), exist_ok=True)

print("MIDI Library folder structure created successfully!")
