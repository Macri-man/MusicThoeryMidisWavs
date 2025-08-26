# musictheory/config.py
# ============================
# Core theory data, mappings, and genre presets
# ============================

# MIDI root note mapping (C4 = 60)
ROOTS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_NUMS = {
    "C": 60, "C#": 61, "Db": 61, "D": 62, "D#": 63, "Eb": 63,
    "E": 64, "F": 65, "F#": 66, "Gb": 66, "G": 67, "G#": 68,
    "Ab": 68, "A": 69, "A#": 70, "Bb": 70, "B": 71
}

# Chord formulas (intervals in semitones)
CHORD_FORMULAS = {
    "major":[0,4,7], "minor":[0,3,7], "dominant7":[0,4,7,10],
    "minor7":[0,3,7,10], "major7":[0,4,7,11],
    "augmented":[0,4,8], "diminished":[0,3,6],
    "half_diminished7":[0,3,6,10], "diminished7":[0,3,6,9],
    "sus2":[0,2,7], "sus4":[0,5,7],
    "major6":[0,4,7,9], "minor6":[0,3,7,9],
    "9":[0,4,7,10,14], "minor9":[0,3,7,10,14], "major9":[0,4,7,11,14],
    "13":[0,4,7,10,14,17,21]
}

# Scale intervals
SCALE_INTERVALS = {
    "major":[0,2,4,5,7,9,11], 
    "minor":[0,2,3,5,7,8,10],
    "harmonic_minor":[0,2,3,5,7,8,11],
    "melodic_minor":[0,2,3,5,7,9,11],
    "pentatonic_major":[0,2,4,7,9], 
    "pentatonic_minor":[0,3,5,7,10],
    "whole_tone":[0,2,4,6,8,10]
}

MODES = {
    "ionian":     SCALE_INTERVALS["major"],  # major scale
    "dorian":     [0, 2, 3, 5, 7, 9, 10],
    "phrygian":   [0, 1, 3, 5, 7, 8, 10],
    "lydian":     [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "aeolian":    SCALE_INTERVALS["minor"],  # natural minor
    "locrian":    [0, 1, 3, 5, 6, 8, 10],
}

# Rhythm patterns (durations in beats)
RHYTHM_PATTERNS = {
    "straight": [1,1,1,1],            # 4 quarters
    "syncopated": [0.75,0.25,1,1],    # push
    "triplet": [2/3,2/3,2/3],         # triplet feel
    "swing": [0.66,0.34,0.66,0.34],   # swung 8ths
}

# Roman numerals → diatonic degrees (for major key by default)
ROMAN_TO_CHORD = {
    "I":(0,"major"), "ii":(2,"minor"), "iii":(4,"minor"),
    "IV":(5,"major"), "V":(7,"major"), "vi":(9,"minor"),
    "vii°":(11,"diminished"),
    # modal / borrowed
    "i":(0,"minor"), "bIII":(3,"major"), "bVII":(10,"major"),
    "III":(4,"major"), "VI":(9,"major"), "VII":(11,"major")
}

# Common progressions (by genre)
PROGRESSIONS = {
    "jazz_ii-V-I": ["ii","V","I"],
    "jazz_iii-VI-ii-V": ["iii","VI","ii","V"],
    "jazz_turnaround": ["I","vi","ii","V"],

    "pop_I-V-vi-IV": ["I","V","vi","IV"],
    "pop_vi-IV-I-V": ["vi","IV","I","V"],
    "pop_IV-I-V-vi": ["IV","I","V","vi"],

    "blues_I-IV-V": ["I","IV","V","I"],
    "blues_quick_change": ["I","IV","I","V","IV","I"],

    "funk_i-bVII-IV": ["i","bVII","IV"],
    "funk_I-bIII-IV": ["I","bIII","IV"],

    "edm_vi-IV-I-V": ["vi","IV","I","V"],
    "edm_I-V-vi-IV": ["I","V","vi","IV"],

    "latin_I-IV-V-IV": ["I","IV","V","IV"],
    "latin_ii-V-I": ["ii","V","I"],

    "orch_I-V-vi-iii-IV-I-IV-V": ["I","V","vi","iii","IV","I","IV","V"],
    "orch_vi-IV-I-V": ["vi","IV","I","V"],
}

# Genre collections
GENRES = {
    "Jazz": ["jazz_ii-V-I","jazz_iii-VI-ii-V","jazz_turnaround"],
    "Pop": ["pop_I-V-vi-IV","pop_vi-IV-I-V","pop_IV-I-V-vi"],
    "Blues": ["blues_I-IV-V","blues_quick_change"],
    "Funk": ["funk_i-bVII-IV","funk_I-bIII-IV"],
    "EDM": ["edm_vi-IV-I-V","edm_I-V-vi-IV"],
    "Latin": ["latin_I-IV-V-IV","latin_ii-V-I"],
    "Orchestral": ["orch_I-V-vi-iii-IV-I-IV-V","orch_vi-IV-I-V"],
}

# General MIDI drum map
DRUMS = {"kick":36,"snare":38,"closed_hat":42,"open_hat":46,"ride":51,"crash":49}

# Drum grooves (per genre)
DRUM_GROOVES = {
    "pop": [
        ("kick",0.0),("kick",1.5),
        ("snare",1.0),("snare",3.0),
        *[("closed_hat",x*0.5) for x in range(8)]
    ],
    "rock": [
        ("kick",0.0),("kick",2.0),
        ("snare",1.0),("snare",3.0),
        *[("closed_hat",x*0.5) for x in range(8)]
    ],
    "jazz": [
        ("ride",0.0),("ride",1.0),("ride",2.0),("ride",3.0),
        ("ride",0.5),("ride",2.5),("snare",2.0),
        ("kick",0.0),("kick",2.0)
    ],
    "funk": [
        ("kick",0.0),("kick",1.5),("kick",2.5),
        ("snare",1.0),("snare",2.0),("snare",3.0),
        *[("closed_hat",i*0.25) for i in range(16)]
    ],
    "edm": [
        ("kick",0.0),("kick",1.0),("kick",2.0),("kick",3.0),
        *[("closed_hat",x*0.5+0.25) for x in range(8)],
        ("snare",1.0),("snare",3.0)
    ],
    "latin": [
        ("kick",0.0),("kick",2.0),
        ("snare",2.5),
        ("closed_hat",1.0),("closed_hat",1.5),("closed_hat",3.0),("closed_hat",3.5),
        ("ride",0.0),("ride",2.0)
    ],
    "orchestral": [
        ("kick",0.0),("kick",2.0),
        ("snare",3.0),("crash",0.0)
    ]
}

# Bass patterns (interval offsets from chord root per beat)
BASS_PATTERNS = {
    "pop":[0,0,0,0],
    "rock":[0,7,0,7],
    "jazz":[0,4,7,11],  # R-3-5-7
    "funk":[0,7,0,5],
    "edm":[0,0,0,0],
    "latin":[0,7,5,7],
    "orchestral":[0,0,7,0],
}

# Song structures by genre
SONG_STRUCTURES = {
    "pop": ["intro","verse","chorus","verse","chorus","bridge","chorus","outro"],
    "jazz": ["intro","head","solo","head","outro"],
    "blues": ["intro","chorus","chorus","solo","chorus","outro"]
}

# Section default chord progressions
SECTION_PROGS = {
    "intro":["I","V","vi","IV"],
    "verse":["I","V","vi","IV"],
    "chorus":["vi","IV","I","V"],
    "bridge":["IV","V","iii","vi"],
    "head":["ii","V","I","I"],
    "solo":["ii","V","I","I"],
    "chorus_blues":["I","I","I","I","IV","IV","I","I","V","IV","I","V"],
    "outro":["I","I","I","I"]
}

# Genre → default instruments (General MIDI program numbers)
GENRE_INSTRUMENTS = {
    "pop": {"piano":0, "bass":33, "melody":81},   # Acoustic Piano, Electric Bass, Synth Lead
    "jazz": {"piano":0, "bass":32, "melody":65},  # Piano, Acoustic Bass, Alto Sax
    "blues": {"piano":0, "bass":34, "melody":24}, # Piano, Fingered Bass, Nylon Guitar
    "funk": {"piano":4, "bass":33, "melody":81},  # Electric Piano, Bass, Synth
    "edm": {"piano":81, "bass":38, "melody":82},  # Synths
    "latin": {"piano":0, "bass":33, "melody":73}, # Piano, Bass, Flute
    "orchestral": {"piano":48, "bass":43, "melody":40}, # Strings, Contrabass, Violin
}
