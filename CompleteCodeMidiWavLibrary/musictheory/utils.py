import os, random
import pretty_midi

SWING_AMOUNT = 0.58
TIMING_JITTER = 0.01
VELOCITY_JITTER = 6

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def humanize_notes(notes, swing=True):
    out = []
    for pitch, start, end, vel in notes:
        if swing:
            eighth_pos = (start*2) % 2
            if 0.9 < eighth_pos < 1.1:
                shift = (SWING_AMOUNT - 0.5) * 0.25
                start += shift; end += shift
        start = max(0.0, start + random.uniform(-TIMING_JITTER, TIMING_JITTER))
        end   = max(start+0.01, end + random.uniform(-TIMING_JITTER, TIMING_JITTER))
        vel   = max(1, min(127, vel + random.randint(-VELOCITY_JITTER, VELOCITY_JITTER)))
        out.append((pitch, start, end, vel))
    return out

def create_named_midi(track_data, filename):
    """track_data = [(name, [(pitch,start,end,vel), ...], is_drum_bool), ...]"""
    ensure_dir(os.path.dirname(filename))
    pm = pretty_midi.PrettyMIDI()
    for name, notes, is_drum in track_data:
        program = 0  # TODO: map instruments by genre
        inst = pretty_midi.Instrument(program=program, name=name, is_drum=is_drum)
        for pitch, start, end, vel in humanize_notes(notes):
            inst.notes.append(pretty_midi.Note(velocity=vel, pitch=pitch, start=start, end=end))
        pm.instruments.append(inst)
    pm.write(filename)
