import random, os
from .config import *
from .utils import create_named_midi
from .theory import roman_to_midi_progression

def drum_track_for_genre(genre, bars, velocity=90):
    groove = DRUM_GROOVES.get(genre, DRUM_GROOVES["pop"])
    notes = []
    for bar in range(bars):
        for name, pos in groove:
            pitch = DRUMS[name]
            start = bar*4.0 + pos
            notes.append((pitch, start, start+0.1, velocity))
    return notes

def bass_track_for_genre(chords_by_bar, genre, base_vel=88):
    pattern = BASS_PATTERNS.get(genre, BASS_PATTERNS["pop"])
    notes, time = [], 0.0
    for chord in chords_by_bar:
        root = min(chord) - 12
        for interval in pattern:
            pitch = root + interval
            notes.append((pitch, time, time+1.0, base_vel))
            time += 1.0
    return notes

def generate_melody(chords_by_bar, scale_intervals, root_midi):
    melody, time = [], 0.0
    scale_notes = [root_midi+i for i in scale_intervals]
    for chord in chords_by_bar:
        chord_tone = random.choice(chord[:3])
        melody.append((chord_tone, time, time+0.5, 102)); time+=0.5
        melody.append((random.choice(scale_notes), time, time+0.5, 96)); time+=0.5
        for _ in range(2):
            melody.append((random.choice(scale_notes), time, time+0.5, 94)); time+=0.5
    return melody

def generate_song(root_midi, genre, filename):
    structure = SONG_STRUCTURES.get(genre, SONG_STRUCTURES["pop"])
    midi_tracks, current_time = [], 0.0
    scale = SCALE_INTERVALS["major"]

    for section in structure:
        roman_prog = SECTION_PROGS.get(section, SECTION_PROGS["verse"])
        chords = roman_to_midi_progression(roman_prog, root_midi)

        piano = [(n, t+current_time, t+1+current_time, 90) for t,n in enumerate(chords[0])]
        bass  = [(n, t+current_time, t+1+current_time, 80) for t,n in enumerate(chords[0])]
        drums = drum_track_for_genre(genre, len(chords))
        melody = generate_melody(chords, scale, root_midi)

        midi_tracks.extend([
            (f"{section}_piano", piano, False),
            (f"{section}_bass", bass, False),
            (f"{section}_drums", drums, True),
            (f"{section}_melody", melody, False),
        ])
        current_time += len(chords)

    create_named_midi(midi_tracks, filename)
    print(f"🎼 Song created: {filename}")
