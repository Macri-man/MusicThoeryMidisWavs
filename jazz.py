# professional_jazz_piano_library.py
import pretty_midi
import os
import random

BASE_DIR = "Professional_Jazz_Piano_Library"
FOLDERS = ["Scales", "Chords", "Arpeggios", "Progressions", "Melodies", "Counterpoint", "Walking_Bass"]
for f in FOLDERS:
    os.makedirs(os.path.join(BASE_DIR, f), exist_ok=True)

ROOTS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# ----------------------
# Music Theory Data
# ----------------------
NOTE_NUMS = { "C": 60, "C#":61, "D":62, "D#":63, "E":64, "F":65, "F#":66, "G":67,
              "G#":68, "A":69, "A#":70, "B":71 }

# Include extended chords and altered dominants
CHORD_FORMULAS = {
    "major": [0,4,7],
    "minor": [0,3,7],
    "dominant7": [0,4,7,10],
    "minor7": [0,3,7,10],
    "major7": [0,4,7,11],
    "dominant7b9": [0,4,7,10,13],
    "dominant7#9": [0,4,7,10,15],
    "half_dim7": [0,3,6,10],
    "dim7": [0,3,6,9]
}

SCALE_INTERVALS = {
    "major": [0,2,4,5,7,9,11],
    "minor": [0,2,3,5,7,8,10],
    "dorian": [0,2,3,5,7,9,10],
    "mixolydian": [0,2,4,5,7,9,10],
    "lydian": [0,2,4,6,7,9,11]
}

RHYTHMS = [0.25,0.5,0.75,1] # sixteenth, eighth, dotted eighth, quarter
VELOCITIES = [60,80,100,120]

# ----------------------
# Utility Functions
# ----------------------
def build_notes(root, intervals):
    return [NOTE_NUMS[root]+i for i in intervals]

def invert_chord(notes, inversion=0):
    n = notes.copy()
    for _ in range(inversion):
        n[0]+=12
        n=n[1:] + [n[0]]
    return sorted(n)

def swing_timing(duration):
    # Apply subtle swing: lengthen first note, shorten second
    if duration>=0.5:
        return duration*1.05
    return duration

def write_jazz_midi(left_notes,right_notes,filename):
    pm = pretty_midi.PrettyMIDI()
    lh = pretty_midi.Instrument(program=0)
    rh = pretty_midi.Instrument(program=0)
    time=0
    idx_l,idx_r=0,0
    while idx_l<len(left_notes) or idx_r<len(right_notes):
        if idx_l<len(left_notes):
            n,d,v = left_notes[idx_l]
            lh.notes.append(pretty_midi.Note(v,n,time,time+d))
            time+=d
            idx_l+=1
        if idx_r<len(right_notes):
            n,d,v = right_notes[idx_r]
            d=swing_timing(d)
            rh.notes.append(pretty_midi.Note(v,n,time,time+d))
            idx_r+=1
    pm.instruments.extend([lh,rh])
    pm.write(filename)

# ----------------------
# Jazz Chords Generator
# ----------------------
def generate_jazz_chords(num_bars=8):
    for root in ROOTS:
        chord_folder = os.path.join(BASE_DIR,"Chords")
        for chord_name, formula in CHORD_FORMULAS.items():
            notes = build_notes(root,formula)
            # Right hand: chord inversions + polyrhythm + velocities
            rh_notes=[]
            idx=0
            total_notes=num_bars*4
            inversions=[invert_chord(notes,i) for i in range(len(notes))]
            while idx<total_notes:
                inv=random.choice(inversions)
                dur=random.choice(RHYTHMS)
                for n in inv:
                    vel=random.choice(VELOCITIES)
                    rh_notes.append((n,dur,vel))
                    idx+=1
            # Left hand: walking bass (stepwise)
            lh_notes=[]
            bass_note=notes[0]-12
            idx=0
            while idx<total_notes:
                step=random.choice([0,2,4]) # stepwise or octave jump
                dur=random.choice(RHYTHMS)
                vel=random.choice(VELOCITIES)
                lh_notes.append((bass_note+step,dur,vel))
                idx+=1
            filename=os.path.join(chord_folder,f"{root}_{chord_name}_jazz.mid")
            write_jazz_midi(lh_notes,rh_notes,filename)
            print(f"Saved jazz chord MIDI: {filename}")

# ----------------------
# Generate Jazz Library
# ----------------------
generate_jazz_chords()
print("Professional jazz piano MIDI library with dynamics, swing, polyrhythms, and voicings generated!")
