# musictheory/config.py
# ============================
# Core theory data, mappings, and genre presets
# ============================

# ----------------------------
# NOTES & ROOTS
# ----------------------------
ROOTS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_NUMS = {
    "C":60,"C#":61,"Db":61,"D":62,"D#":63,"Eb":63,
    "E":64,"F":65,"F#":66,"Gb":66,"G":67,"G#":68,
    "Ab":68,"A":69,"A#":70,"Bb":70,"B":71
}

# ----------------------------
# CHORD FORMULAS
# ----------------------------
CHORD_FORMULAS = {
    "major":[0,4,7], "minor":[0,3,7],
    "dominant7":[0,4,7,10], "minor7":[0,3,7,10], "major7":[0,4,7,11],
    "augmented":[0,4,8], "diminished":[0,3,6],
    "half_diminished7":[0,3,6,10], "diminished7":[0,3,6,9],
    "sus2":[0,2,7], "sus4":[0,5,7],
    "major6":[0,4,7,9], "minor6":[0,3,7,9],
    "9":[0,4,7,10,14], "minor9":[0,3,7,10,14], "major9":[0,4,7,11,14],
    "11":[0,4,7,10,14,17], "13":[0,4,7,10,14,17,21],
    "add9":[0,4,7,14], "minor_add9":[0,3,7,14],
    "power":[0,7]  # 5th chords
}

# ----------------------------
# SCALE INTERVALS
# ----------------------------
SCALE_INTERVALS = {
    "major":[0,2,4,5,7,9,11],
    "minor":[0,2,3,5,7,8,10],
    "harmonic_minor":[0,2,3,5,7,8,11],
    "melodic_minor":[0,2,3,5,7,9,11],
    "pentatonic_major":[0,2,4,7,9],
    "pentatonic_minor":[0,3,5,7,10],
    "whole_tone":[0,2,4,6,8,10],
    "chromatic":list(range(12)),
    "blues":[0,3,5,6,7,10],
    "neapolitan_minor":[0,1,3,5,7,8,11],
    "hungarian_minor":[0,2,3,6,7,8,11],
}

# ----------------------------
# MODES
# ----------------------------
MODES = {
    "ionian": SCALE_INTERVALS["major"],
    "dorian": [0,2,3,5,7,9,10],
    "phrygian": [0,1,3,5,7,8,10],
    "lydian": [0,2,4,6,7,9,11],
    "mixolydian": [0,2,4,5,7,9,10],
    "aeolian": SCALE_INTERVALS["minor"],
    "locrian": [0,1,3,5,6,8,10],
}

# ----------------------------
# RHYTHM PATTERNS
# ----------------------------
RHYTHM_PATTERNS = {
    "straight":[1,1,1,1],
    "syncopated":[0.75,0.25,1,1],
    "triplet":[2/3,2/3,2/3],
    "swing":[0.66,0.34,0.66,0.34],
    "clave_3-2":[1,0.5,0.5,1,1],   # Latin clave
    "clave_2-3":[0.5,1,0.5,1,1],
    "polyrhythm_3_over_4":[1/3,1/3,1/3,0.5,0.5,0.5,0.5],
}

# ----------------------------
# HARMONIC PROGRESSIONS
# ----------------------------
ROMAN_TO_CHORD = {
    "I":(0,"major"), "ii":(2,"minor"), "iii":(4,"minor"),
    "IV":(5,"major"), "V":(7,"major"), "vi":(9,"minor"),
    "vii°":(11,"diminished"),
    "i":(0,"minor"), "bIII":(3,"major"), "bVII":(10,"major"),
    "III":(4,"major"), "VI":(9,"major"), "VII":(11,"major"),
}

PROGRESSIONS = {
    "jazz_ii-V-I":["ii","V","I"],
    "jazz_turnaround":["I","vi","ii","V"],
    "pop_axis":["I","V","vi","IV"],
    "blues_12bar":["I","I","I","I","IV","IV","I","I","V","IV","I","V"],
    "circle_of_fifths":["I","IV","vii°","iii","vi","ii","V","I"],
    "funk_jam":["i","bVII","IV","i"],
    "latin_salsa":["I","IV","V","IV"],
    "edm_drop":["vi","IV","I","V"],
    "film_epic":["I","V","vi","iii","IV","I","IV","V"],
}

GENRES = {
    "Jazz":["jazz_ii-V-I","jazz_turnaround"],
    "Pop":["pop_axis"],
    "Blues":["blues_12bar"],
    "Funk":["funk_jam"],
    "EDM":["edm_drop"],
    "Latin":["latin_salsa"],
    "Orchestral":["film_epic"],
}

# ----------------------------
# DRUMS
# ----------------------------
DRUMS = {
    "kick":36,"snare":38,"closed_hat":42,"open_hat":46,
    "ride":51,"crash":49,"tom_low":45,"tom_mid":47,"tom_high":50,
    "clap":39,"rim":37,"cowbell":56,"conga":64,"bongo":60
}

DRUM_GROOVES = {
    "pop":[("kick",0.0),("snare",1.0),("snare",3.0),
           *[("closed_hat",x*0.5) for x in range(8)]],
    "rock":[("kick",0.0),("kick",2.0),("snare",1.0),("snare",3.0),
            *[("closed_hat",x*0.5) for x in range(8)]],
    "jazz":[("ride",i) for i in [0.0,0.5,1.0,2.0,2.5,3.0]],
    "funk":[("kick",0.0),("snare",1.0),("snare",2.5),
            *[("closed_hat",i*0.25) for i in range(16)]],
    "edm":[("kick",i) for i in [0,1,2,3]],
    "latin":[("conga",0.5),("cowbell",1.0),("bongo",2.5)],
    "orchestral":[("kick",0.0),("snare",3.0),("crash",0.0)],
}

# ----------------------------
# BASS PATTERNS
# ----------------------------
BASS_PATTERNS = {
    "pop":[0,0,0,0],
    "rock":[0,7,0,7],
    "jazz":[0,4,7,11],   # R-3-5-7
    "funk":[0,7,0,5],
    "edm":[0,0,0,0],
    "latin":[0,7,5,7],
    "orchestral":[0,0,7,0],
    "walking":[0,2,4,5], # stepwise
}

# ----------------------------
# SONG STRUCTURES
# ----------------------------
SONG_STRUCTURES = {
    "pop":["intro","verse","chorus","verse","chorus","bridge","chorus","outro"],
    "jazz":["intro","head","solo","head","outro"],
    "blues":["intro","chorus","chorus","solo","chorus","outro"],
    "edm":["intro","build","drop","break","drop","outro"],
    "film":["intro","theme","variation","climax","resolution"],
}

SECTION_PROGS = {
    "intro":["I","V","vi","IV"],
    "verse":["I","V","vi","IV"],
    "chorus":["vi","IV","I","V"],
    "bridge":["IV","V","iii","vi"],
    "drop":["vi","IV","I","V"],
    "build":["I","ii","IV","V"],
    "outro":["I","I","I","I"]
}

# ----------------------------
# INSTRUMENTS
# ----------------------------
GENRE_INSTRUMENTS = {
    "pop":{"piano":0,"bass":33,"melody":81},
    "rock":{"guitar":29,"bass":34,"drums":0},
    "jazz":{"piano":0,"bass":32,"melody":65},
    "blues":{"guitar":26,"bass":34,"melody":27},
    "funk":{"epiano":4,"bass":33,"melody":81},
    "edm":{"lead":81,"bass":38,"pad":89},
    "latin":{"piano":0,"bass":33,"melody":73,"perc":12},
    "orchestral":{"strings":48,"bass":43,"melody":40,"brass":61,"woodwinds":73},
    "film":{"strings":48,"brass":61,"choir":52,"perc":117},
}

# ============================
# EXPRESSIVE PLAYING LAYERS
# ============================

# Articulation styles (velocity multipliers and note length multipliers)
ARTICULATIONS = {
    "legato": {"length":1.1, "velocity":1.0},   # smooth, connected
    "staccato": {"length":0.5, "velocity":0.9}, # short, detached
    "accent": {"length":1.0, "velocity":1.3},   # strong emphasis
    "tenuto": {"length":1.0, "velocity":1.1},   # held, slightly emphasized
    "ghost": {"length":0.7, "velocity":0.5},    # soft/hidden note
    "marcato": {"length":0.9, "velocity":1.4},  # sharp attack
    "swell": {"length":1.5, "velocity":[0.6,0.8,1.2]}, # gradual crescendo
}

# Humanization ranges (to avoid robotic feel)
HUMANIZATION = {
    "timing_jitter": 0.02,   # up to ±2% offset in rhythm
    "velocity_jitter": 0.05, # up to ±5% change in dynamics
    "swing_strength": 0.15   # push-pull feel for swing
}

# Dynamics levels (MIDI velocity ranges)
DYNAMICS = {
    "pp": (30,45),  # pianissimo
    "p":  (46,60),  # piano
    "mp": (61,75),  # mezzo-piano
    "mf": (76,90),  # mezzo-forte
    "f":  (91,105), # forte
    "ff": (106,120),# fortissimo
    "fff":(121,127) # maximum
}

# Orchestration layers (per genre / style)
ORCHESTRATION = {
    "orchestral": {
        "strings":["violins","violas","cellos","basses"],
        "brass":["trumpets","horns","trombones","tuba"],
        "woodwinds":["flutes","clarinets","oboes","bassoons"],
        "percussion":["timpani","cymbals","snare"]
    },
    "jazz_bigband": {
        "saxes":["alto sax","tenor sax","baritone sax"],
        "brass":["trumpets","trombones"],
        "rhythm":["piano","bass","drums","guitar"]
    },
    "edm_layers": {
        "lead":["supersaw","plucked synth"],
        "bass":["sub","growl"],
        "pads":["strings pad","choir pad"],
        "fx":["risers","impacts"]
    }
}

# Ornamentation (extra notes between chords/melody)
ORNAMENTS = {
    "grace": {"offset":-0.1, "length":0.2}, # short before note
    "mordent": {"pattern":[0,-1,0]},        # note → below → note
    "trill": {"pattern":[0,1,0,1,0]},       # fast alternation
    "turn": {"pattern":[1,0,-1,0]},         # above → note → below → note
    "slide": {"pattern":"gliss"},           # continuous slide
}

# Instrument articulations (per instrument family)
INSTRUMENT_TECHNIQUES = {
    "strings": ["pizzicato","legato","spiccato","tremolo"],
    "brass": ["staccato","legato","sforzando","mute"],
    "woodwinds": ["flutter","slur","staccato","breathy"],
    "guitar": ["palm_mute","slide","bend","harmonics"],
    "drums": ["rimshot","roll","flam","ghost"],
    "synth": ["filter_sweep","lfo_vibrato","arp","glide"]
}



# ============================
# GENRE PERFORMANCE PROFILES
# ============================

GENRE_EXPRESSIONS = {
    "pop": {
        "articulations": ["legato","accent"],
        "dynamics": "mf",
        "swing": False,
        "humanization": {"timing_jitter":0.01,"velocity_jitter":0.03},
        "ornaments": []
    },
    "rock": {
        "articulations": ["staccato","accent"],
        "dynamics": "f",
        "swing": False,
        "humanization": {"timing_jitter":0.02,"velocity_jitter":0.05},
        "ornaments": ["slide","grace"]
    },
    "jazz": {
        "articulations": ["swing","ghost","accent"],
        "dynamics": "mp",
        "swing": True,
        "humanization": {"timing_jitter":0.03,"velocity_jitter":0.07},
        "ornaments": ["grace","mordent","trill"]
    },
    "blues": {
        "articulations": ["slide","ghost","accent"],
        "dynamics": "mf",
        "swing": True,
        "humanization": {"timing_jitter":0.025,"velocity_jitter":0.06},
        "ornaments": ["bend","grace"]
    },
    "funk": {
        "articulations": ["staccato","accent","ghost"],
        "dynamics": "mf",
        "swing": True,
        "humanization": {"timing_jitter":0.02,"velocity_jitter":0.08},
        "ornaments": ["grace","mordent"]
    },
    "edm": {
        "articulations": ["staccato","accent"],
        "dynamics": "ff",
        "swing": False,
        "humanization": {"timing_jitter":0.005,"velocity_jitter":0.02},
        "ornaments": ["filter_sweep","arp"]
    },
    "latin": {
        "articulations": ["accent","legato"],
        "dynamics": "f",
        "swing": False,
        "humanization": {"timing_jitter":0.02,"velocity_jitter":0.05},
        "ornaments": ["grace","trill","turn"]
    },
    "orchestral": {
        "articulations": ["legato","tenuto","marcato"],
        "dynamics": "mf",
        "swing": False,
        "humanization": {"timing_jitter":0.015,"velocity_jitter":0.04},
        "ornaments": ["trill","turn","swell"]
    },
    "film": {
        "articulations": ["legato","swell","marcato"],
        "dynamics": "f",
        "swing": False,
        "humanization": {"timing_jitter":0.02,"velocity_jitter":0.05},
        "ornaments": ["swell","trill","gliss"]
    }
}

# ============================
# TEMPO RANGES (by genre)
# ============================
GENRE_TEMPOS = {
    "pop": (90,120),
    "rock": (100,140),
    "jazz": (60,160),
    "blues": (70,110),
    "funk": (90,120),
    "edm": (120,140),
    "latin": (90,130),
    "orchestral": (60,100),
    "film": (60,120),
}

# ============================
# AUTOMATIC DYNAMICS CURVES
# ============================
DYNAMIC_CURVES = {
    "crescendo":[0.6,0.7,0.85,1.0],
    "diminuendo":[1.0,0.85,0.7,0.6],
    "swell":[0.6,0.9,1.1,0.9],
    "pulse":[0.8,1.0,0.8,1.0]
}

# ============================
# GENRE → DEFAULT LAYERS
# (structure + instruments + expressions)
# ============================
GENRE_DEFAULTS = {
    "pop": {
        "structure": SONG_STRUCTURES["pop"],
        "instruments": GENRE_INSTRUMENTS["pop"],
        "expressions": GENRE_EXPRESSIONS["pop"]
    },
    "jazz": {
        "structure": SONG_STRUCTURES["jazz"],
        "instruments": GENRE_INSTRUMENTS["jazz"],
        "expressions": GENRE_EXPRESSIONS["jazz"]
    },
    "blues": {
        "structure": SONG_STRUCTURES["blues"],
        "instruments": GENRE_INSTRUMENTS["blues"],
        "expressions": GENRE_EXPRESSIONS["blues"]
    },
    "funk": {
        "structure": SONG_STRUCTURES["pop"],  # similar verse/chorus
        "instruments": GENRE_INSTRUMENTS["funk"],
        "expressions": GENRE_EXPRESSIONS["funk"]
    },
    "edm": {
        "structure": SONG_STRUCTURES["edm"],
        "instruments": GENRE_INSTRUMENTS["edm"],
        "expressions": GENRE_EXPRESSIONS["edm"]
    },
    "latin": {
        "structure": SONG_STRUCTURES["pop"], # verse/chorus with percussive breaks
        "instruments": GENRE_INSTRUMENTS["latin"],
        "expressions": GENRE_EXPRESSIONS["latin"]
    },
    "orchestral": {
        "structure": SONG_STRUCTURES["film"],
        "instruments": GENRE_INSTRUMENTS["orchestral"],
        "expressions": GENRE_EXPRESSIONS["orchestral"]
    },
    "film": {
        "structure": SONG_STRUCTURES["film"],
        "instruments": GENRE_INSTRUMENTS["film"],
        "expressions": GENRE_EXPRESSIONS["film"]
    }
}


# ============================
# MODULATION & KEY CHANGE PRESETS
# ============================

# Common modulation types
MODULATIONS = {
    "relative_minor": {"from":"major","to":"minor","shift":-3},   # C major → A minor
    "relative_major": {"from":"minor","to":"major","shift":+3},   # A minor → C major
    "parallel_minor": {"from":"major","to":"minor","shift":0},    # C major → C minor
    "parallel_major": {"from":"minor","to":"major","shift":0},    # C minor → C major
    "dominant_pivot": {"from":"any","to":"any","shift":+7},       # tonic → V of new key
    "subdominant_pivot": {"from":"any","to":"any","shift":+5},    # tonic → IV of new key
    "chromatic_mediant": {"from":"any","to":"any","shift":+4},    # C → E major/minor
    "tritone_sub": {"from":"jazz","to":"jazz","shift":+6},        # Jazz V7 → bII7
    "picardy_third": {"from":"minor","to":"major","shift":0},     # minor → major final chord
    "key_lift": {"from":"pop","to":"pop","shift":+2},             # + whole step for excitement
    "film_dramatic": {"from":"minor","to":"major","shift":+3},    # minor → relative major → up whole step
}

# Example modulation chains by genre
GENRE_MODULATIONS = {
    "pop": [
        ["I","V","vi","IV"],    # main
        "key_lift",             # up a whole step
        ["I","V","vi","IV"]     # repeat in new key
    ],
    "jazz": [
        ["ii","V","I"],         # base
        "tritone_sub",          # ii → V (sub)
        ["ii","V","I"]          # resolution in new key
    ],
    "film": [
        ["i","VI","III","VII"], # dark intro
        "film_dramatic",        # modulation
        ["I","V","vi","IV"]     # brighter resolution
    ],
    "blues": [
        ["I","IV","I","V"],     # basic
        "parallel_minor",       # bluesy minor modulation
        ["i","bVII","IV","i"]
    ],
    "orchestral": [
        ["I","V","vi","iii"],   # theme
        "dominant_pivot",       # modulate to new tonic
        ["I","IV","V","I"]
    ]
}

# ============================
# CADENCES
# ============================
CADENCES = {
    "perfect":["V","I"],          # strong resolution
    "plagal":["IV","I"],          # church "Amen"
    "deceptive":["V","vi"],       # surprise
    "half":["I","V"],             # unresolved
    "phrygian":["iv","V"],        # minor, Spanish flavor
    "blues_turnaround":["I","vi","ii","V"], # 12-bar loop close
}

# ============================
# EXTENDED GENRE DEFAULTS (with modulation & cadences)
# ============================
for g in GENRE_DEFAULTS:
    GENRE_DEFAULTS[g]["modulations"] = GENRE_MODULATIONS.get(g, [])
    GENRE_DEFAULTS[g]["cadences"] = ["perfect","deceptive"] if g in ["pop","rock","edm"] else ["perfect","plagal"]


# ============================
# TEXTURE & DENSITY LAYERS
# ============================

# Arrangement density levels
TEXTURE_LEVELS = {
    "sparse": {
        "instruments": 1,        # solo / minimal
        "register_spread": 1,    # very narrow range
        "rhythmic_density": 0.3, # fewer notes
        "articulation": "legato",
        "dynamics": "p"
    },
    "light": {
        "instruments": 2-3,
        "register_spread": 2,
        "rhythmic_density": 0.5,
        "articulation": "tenuto",
        "dynamics": "mp"
    },
    "medium": {
        "instruments": 4-6,
        "register_spread": 3,
        "rhythmic_density": 0.7,
        "articulation": "mixed",
        "dynamics": "mf"
    },
    "thick": {
        "instruments": 6-10,
        "register_spread": 4,
        "rhythmic_density": 0.9,
        "articulation": "accent",
        "dynamics": "f"
    },
    "wall_of_sound": {
        "instruments": 10+,
        "register_spread": 5,   # huge (low bass to high strings/brass)
        "rhythmic_density": 1.0,
        "articulation": "marcato",
        "dynamics": "ff"
    }
}

# Genre → default texture curve (verse → chorus → bridge → climax)
GENRE_TEXTURE_CURVES = {
    "pop": ["sparse","light","medium","thick","wall_of_sound"],
    "rock": ["light","medium","thick","wall_of_sound"],
    "jazz": ["sparse","light","medium"], # jazz rarely goes wall-of-sound
    "edm": ["sparse","medium","wall_of_sound"], # build-up → drop
    "film": ["sparse","light","medium","thick","wall_of_sound"], # full arc
    "orchestral": ["light","medium","thick","wall_of_sound"],    # always layered
    "blues": ["sparse","light","medium"], # intimate texture
}

# Register spread presets (octave ranges for instruments)
REGISTER_SPREADS = {
    1: {"low":(60,72), "high":(60,72)},   # same octave
    2: {"low":(48,60), "high":(72,84)},   # ~2 octave split
    3: {"low":(36,60), "high":(72,96)},   # ~3-4 octaves
    4: {"low":(28,55), "high":(80,100)},  # very wide
    5: {"low":(21,48), "high":(84,108)},  # max orchestral span
}

# Rhythmic density meaning (probability of subdivision use)
RHYTHM_DENSITY = {
    0.3: {"allowed_subdivisions":["quarter","half"]},
    0.5: {"allowed_subdivisions":["quarter","eighth"]},
    0.7: {"allowed_subdivisions":["eighth","sixteenth"]},
    0.9: {"allowed_subdivisions":["eighth","sixteenth","triplets"]},
    1.0: {"allowed_subdivisions":["sixteenth","32nd","syncopation"]}
}