# simplemusictheory.py
# Fully integrated MIDI library + arranger
# deps: pip install pretty_midi mido

import os
import random
import pretty_midi

# =========================
# CONFIG & THEORY DATA
# =========================
BASE_DIR = "MIDITOTAL_Library"

ROOTS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_NUMS = {note: 60+i for i, note in enumerate(ROOTS)}  # C4 = 60

CHORD_FORMULAS = {
    "major":[0,4,7], "minor":[0,3,7], "dominant7":[0,4,7,10],
    "minor7":[0,3,7,10], "major7":[0,4,7,11],
    "augmented":[0,4,8], "diminished":[0,3,6],
    "half_dim7":[0,3,6,10], "dim7":[0,3,6,9],
    "sus2":[0,2,7], "sus4":[0,5,7],
    "major6":[0,4,7,9], "minor6":[0,3,7,9],
    "9":[0,4,7,10,14], "minor9":[0,3,7,10,14], "maj9":[0,4,7,11,14],
    "13":[0,4,7,10,14,17,21]
}

SCALE_INTERVALS = {
    "major":[0,2,4,5,7,9,11], "minor":[0,2,3,5,7,8,10],
    "dorian":[0,2,3,5,7,9,10], "phrygian":[0,1,3,5,7,8,10],
    "lydian":[0,2,4,6,7,9,11], "mixolydian":[0,2,4,5,7,9,10],
    "locrian":[0,1,3,5,6,8,10], "harmonic_minor":[0,2,3,5,7,8,11],
    "melodic_minor":[0,2,3,5,7,9,11],
    # a few extras
    "pentatonic_major":[0,2,4,7,9], "pentatonic_minor":[0,3,5,7,10],
    "whole_tone":[0,2,4,6,8,10]
}

# Rhythms used by grooves/progressions
RHYTHM_PATTERNS = {
    "straight": [1,1,1,1],            # 4 quarters
    "syncopated": [0.75,0.25,1,1],    # push
    "triplet": [2/3,2/3,2/3],         # triplet feel
    "swing": [0.66,0.34,0.66,0.34],   # swung 8ths
}

# Roman-numeral to diatonic degree + chord quality (major key default)
ROMAN_TO_CHORD = {
    "I":(0,"major"), "ii":(2,"minor"), "iii":(4,"minor"),
    "IV":(5,"major"), "V":(7,"major"), "vi":(9,"minor"),
    "vii°":(11,"diminished"),
    # borrowed / modal common ones
    "i":(0,"minor"), "bIII":(3,"major"), "bVII":(10,"major"),
    "III":(4,"major"), "VI":(9,"major"), "VII":(11,"major")
}

# Genre → progression templates
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

# Genre collections (for foldering)
GENRES = {
    "Jazz": ["jazz_ii-V-I","jazz_iii-VI-ii-V","jazz_turnaround"],
    "Pop": ["pop_I-V-vi-IV","pop_vi-IV-I-V","pop_IV-I-V-vi"],
    "Blues": ["blues_I-IV-V","blues_quick_change"],
    "Funk": ["funk_i-bVII-IV","funk_I-bIII-IV"],
    "EDM": ["edm_vi-IV-I-V","edm_I-V-vi-IV"],
    "Latin": ["latin_I-IV-V-IV","latin_ii-V-I"],
    "Orchestral": ["orch_I-V-vi-iii-IV-I-IV-V","orch_vi-IV-I-V"],
}

# Drum map (GM)
DRUMS = {"kick":36,"snare":38,"closed_hat":42,"open_hat":46,"ride":51,"crash":49}

# Genre drum grooves: list of (drum_name, beat_position) per 4/4 bar
DRUM_GROOVES = {
    "pop": [
        ("kick",0.0),("kick",1.5),
        ("snare",1.0),("snare",3.0),
        *[("closed_hat",x*0.5) for x in range(8)]  # 8ths
    ],
    "rock": [
        ("kick",0.0),("kick",2.0),
        ("snare",1.0),("snare",3.0),
        *[("closed_hat",x*0.5) for x in range(8)]
    ],
    "jazz": [
        ("ride",0.0),("ride",1.0),("ride",2.0),("ride",3.0),
        ("ride",0.5),("ride",2.5), ("snare",2.0), ("kick",0.0),("kick",2.0)
    ],
    "funk": [
        ("kick",0.0),("kick",1.5),("kick",2.5),
        ("snare",1.0),("snare",2.0),("snare",3.0),
        *[("closed_hat",i*0.25) for i in range(16)]  # 16ths
    ],
    "edm": [
        ("kick",0.0),("kick",1.0),("kick",2.0),("kick",3.0),
        *[("closed_hat",x*0.5+0.25) for x in range(8)], # off 8ths
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

# Bass patterns: semitone offsets from chord root on each beat in a bar
BASS_PATTERNS = {
    "pop":[0,0,0,0],
    "rock":[0,7,0,7],
    "jazz":[0,4,7,11],     # R-3-5-7 (walking)
    "funk":[0,7,0,5],
    "edm":[0,0,0,0],
    "latin":[0,7,5,7],
    "orchestral":[0,0,7,0],
}

# Song structure templates
SONG_STRUCTURES = {
    "pop": ["intro","verse","chorus","verse","chorus","bridge","chorus","outro"],
    "jazz": ["intro","head","solo","head","outro"],
    "blues": ["intro","chorus","chorus","solo","chorus","outro"]
}

# Section → default progression (fallbacks)
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

# =========================
# UTILS & HELPERS
# =========================
def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def chord_inversions(formula):
    return [formula[i:] + [n+12 for n in formula[:i]] for i in range(len(formula))]

# Humanization
SWING_AMOUNT = 0.58       # 0.5 straight → >0.5 swings off-beats later
TIMING_JITTER = 0.01      # seconds jitter
VELOCITY_JITTER = 6       # +/- velocity

def humanize_notes(notes, swing=True):
    out = []
    for pitch, start, end, vel in notes:
        # swing off-8ths
        if swing:
            # treat positions in beats; swing 8th off-beats
            eighth_pos = (start*2) % 2
            if 0.9 < eighth_pos < 1.1:
                shift = (SWING_AMOUNT - 0.5) * 0.25  # proportion of beat
                start += shift
                end += shift
        # jitter
        jitter_s = random.uniform(-TIMING_JITTER, TIMING_JITTER)
        jitter_e = random.uniform(-TIMING_JITTER, TIMING_JITTER)
        start = max(0.0, start + jitter_s)
        end = max(start + 0.01, end + jitter_e)
        # vel var
        vel = max(1, min(127, vel + random.randint(-VELOCITY_JITTER, VELOCITY_JITTER)))
        out.append((pitch, start, end, vel))
    return out

def create_named_midi(track_data, filename):
    """track_data = [(name, [(pitch,start,end,vel), ...], is_drum_bool), ...]"""
    ensure_dir(os.path.dirname(filename))
    pm = pretty_midi.PrettyMIDI()
    for name, notes, is_drum in track_data:
        program = 0  # Acoustic Grand Piano default
        inst = pretty_midi.Instrument(program=program, name=name, is_drum=is_drum)
        hn = humanize_notes(notes, swing=True)
        for pitch, start, end, vel in hn:
            inst.notes.append(pretty_midi.Note(velocity=vel, pitch=pitch, start=start, end=end))
        pm.instruments.append(inst)
    pm.write(filename)

def roman_to_midi_progression(roman_seq, root_midi, key_mode="major"):
    """Return list of chord note lists (block) per bar in MIDI pitches."""
    out = []
    for rn in roman_seq:
        if rn not in ROMAN_TO_CHORD:
            # fallback: treat uppercase as major triad at scale degree
            print(f"[warn] Unknown roman numeral '{rn}', skipping.")
            continue
        degree, chord_type = ROMAN_TO_CHORD[rn]
        chord = [root_midi + degree + n for n in CHORD_FORMULAS[chord_type]]
        out.append(chord)
    return out

def shift_notes_time(notes, offset):
    return [(p, s+offset, e+offset, v) for (p,s,e,v) in notes]

# =========================
# LIBRARY GENERATION
# =========================
def create_scale_files():
    for scale_name, intervals in SCALE_INTERVALS.items():
        for root_name, root_midi in NOTE_NUMS.items():
            # scale
            scale_notes = [(root_midi+i, i*0.25, i*0.25+0.5, 100) for i in intervals]
            path = os.path.join(BASE_DIR,"Scales",scale_name,root_name,f"{root_name}_{scale_name}.mid")
            create_named_midi([(f"{root_name}_{scale_name}_scale",
                                [(p,s,e,v) for (p,s,e,v) in scale_notes], False)], path)
            # arpeggio (every other)
            arp_ints = intervals[::2]
            arp_notes = [(root_midi+i, idx*0.5, idx*0.5+0.5, 100) for idx,i in enumerate(arp_ints)]
            path_arp = os.path.join(BASE_DIR,"Scales",scale_name,root_name,"Arpeggios",
                                    f"{root_name}_{scale_name}_arp.mid")
            create_named_midi([(f"{root_name}_{scale_name}_arpeggio", arp_notes, False)], path_arp)

def create_chord_files():
    for chord_name, ints in CHORD_FORMULAS.items():
        for root_name, root_midi in NOTE_NUMS.items():
            for inv_i, inv in enumerate(chord_inversions(ints)):
                chord_notes = [(root_midi+n, 0.0, 2.0, 100) for n in inv]
                path = os.path.join(BASE_DIR,"Chords",chord_name,f"Inversion_{inv_i}",
                                    f"{root_name}_{chord_name}_inv{inv_i}.mid")
                create_named_midi([(f"{root_name}_{chord_name}_inv{inv_i}", chord_notes, False)], path)

# =========================
# PROGRESSION ENGINE (block + arp + bass + drums) with grooves & loops
# =========================
def drum_track_for_genre(genre, bars, velocity=90):
    g = "pop"
    if genre in DRUM_GROOVES:
        g = genre
    groove = DRUM_GROOVES[g]
    notes = []
    for bar in range(bars):
        for name, pos in groove:
            pitch = DRUMS[name]
            start = bar*4.0 + pos
            notes.append((pitch, start, start+0.1, velocity))
    return notes

def bass_track_for_genre(chords_by_bar, genre, base_vel=88):
    g = genre if genre in BASS_PATTERNS else "pop"
    pattern = BASS_PATTERNS[g]
    notes = []
    time = 0.0
    for chord in chords_by_bar:
        root = min(chord) - 12  # drop an octave
        for interval in pattern:
            pitch = root + interval
            start = time
            end = start + 1.0
            notes.append((pitch, start, end, base_vel))
            time += 1.0
    return notes

def block_track_from_chords(chords_by_bar, groove="straight", vel=100):
    track = []
    time = 0.0
    pattern = RHYTHM_PATTERNS.get(groove, [1.0])
    for chord in chords_by_bar:
        dur = pattern[0] if pattern else 1.0
        for n in chord:
            track.append((n, time, time+dur, vel))
        time += sum(pattern) if pattern else 1.0
    return track

def arp_track_from_chords(chords_by_bar, groove="straight", vel=96):
    track = []
    time = 0.0
    pattern = RHYTHM_PATTERNS.get(groove, [0.25]*4)
    for chord in chords_by_bar:
        for i, n in enumerate(chord):
            dur = pattern[i % len(pattern)]
            track.append((n, time, time+dur, vel))
            time += dur
    return track

def generate_genre_progressions_full():
    out_root = os.path.join(BASE_DIR, "Progressions_Full")
    for genre, prog_list in GENRES.items():
        for prog_name in prog_list:
            for root_name, root_midi in NOTE_NUMS.items():
                roman_seq = PROGRESSIONS[prog_name]
                chords_one_pass = roman_to_midi_progression(roman_seq, root_midi, "major")
                # loop twice
                chords_two_loops = chords_one_pass + chords_one_pass
                bars = len(chords_two_loops)

                track_data = []
                # multiple groove variants in the SAME file
                for groove in ["straight","swing","syncopated"]:
                    block = block_track_from_chords(chords_two_loops, groove=groove, vel=100)
                    arp = arp_track_from_chords(chords_two_loops, groove=groove, vel=95)
                    bass = bass_track_for_genre(chords_two_loops, genre.lower(), base_vel=86)
                    drums = drum_track_for_genre(genre.lower(), bars, velocity=92)

                    track_data.extend([
                        (f"{root_name}_{prog_name}_block_{groove}", block, False),
                        (f"{root_name}_{prog_name}_arp_{groove}", arp, False),
                        (f"{root_name}_{prog_name}_bass_{groove}", bass, False),
                        (f"{root_name}_{prog_name}_drums_{groove}", drums, True),
                    ])

                path = os.path.join(out_root, genre, prog_name, root_name, f"{root_name}_{prog_name}.mid")
                create_named_midi(track_data, path)
    print("✅ Genre progressions (block/arp/bass/drums, grooves, 2x loops) generated.")

# =========================
# MELODY & ARRANGER
# =========================
def generate_melody(chords_by_bar, scale_intervals, root_midi, bars=None):
    """Simple: chord tone on strong beat, passing scale note after."""
    if bars is None:
        bars = len(chords_by_bar)
    melody = []
    time = 0.0
    scale_notes = [root_midi+i for i in scale_intervals]
    for i in range(bars):
        chord = chords_by_bar[i % len(chords_by_bar)]
        chord_tone = random.choice(chord[:min(3,len(chord))])  # root/3rd/5th
        melody.append((chord_tone, time, time+0.5, 102))
        time += 0.5
        passing = random.choice(scale_notes)
        melody.append((passing, time, time+0.5, 96))
        time += 0.5
        # fill remaining 3rd & 4th beats with scale tones
        for _ in range(2):
            nxt = random.choice(scale_notes)
            melody.append((nxt, time, time+0.5, 94))
            time += 0.5
    return melody

def generate_comping(chords_by_bar, pattern=[1,1,1,1], vel=92, start_time=0.0):
    """Hit the full chord with the given durations pattern inside each bar."""
    notes = []
    t = start_time
    for chord in chords_by_bar:
        for dur in pattern:
            for n in chord:
                notes.append((n, t, t+dur, vel))
            t += dur
    return notes

def generate_song(root_name, genre, filename):
    structure = SONG_STRUCTURES.get(genre, SONG_STRUCTURES["pop"])
    midi_tracks = []
    current_time = 0.0
    root_midi = NOTE_NUMS[root_name]
    scale = SCALE_INTERVALS["major"] if genre.lower() != "jazz" else SCALE_INTERVALS["dorian"]

    for section in structure:
        roman_prog = SECTION_PROGS.get(section, SECTION_PROGS["verse"])
        chords = roman_to_midi_progression(roman_prog, root_midi, "major")

        # comping pattern by genre
        comp_pat = {"pop":[1,1,1,1], "jazz":[0.5,0.5,1,1], "blues":[1,1,1,1]}.get(genre, [1,1,1,1])
        piano = shift_notes_time(generate_comping(chords, comp_pat, vel=92), current_time)
        bass = shift_notes_time(bass_track_for_genre(chords, genre.lower(), base_vel=84), current_time)
        drums = shift_notes_time(drum_track_for_genre(genre.lower(), len(chords), velocity=90), current_time)
        melody = shift_notes_time(generate_melody(chords, scale, root_midi, bars=len(chords)), current_time)

        midi_tracks.extend([
            (f"{section}_piano", piano, False),
            (f"{section}_bass", bass, False),
            (f"{section}_drums", drums, True),
            (f"{section}_melody", melody, False),
        ])
        current_time += len(chords)  # next section after these bars

    create_named_midi(midi_tracks, filename)
    print(f"🎼 Song created: {filename}")

# =========================
# MAIN: run everything
# =========================
if __name__ == "__main__":
    ensure_dir(BASE_DIR)

    print("Generating theory library (scales/chords/arps)…")
    create_scale_files()
    create_chord_files()
    print("✅ Theory library done.")

    print("Generating genre progressions (full band)…")
    generate_genre_progressions_full()

    print("Generating example arranged songs…")
    # Make a few demo songs
    generate_song("C","pop", os.path.join(BASE_DIR,"Songs","Pop","C_pop_song.mid"))
    generate_song("F","jazz", os.path.join(BASE_DIR,"Songs","Jazz","F_jazz_song.mid"))
    generate_song("A","blues", os.path.join(BASE_DIR,"Songs","Blues","A_blues_song.mid"))

    print("✅ All done. Check the MIDI_Library folder.")
