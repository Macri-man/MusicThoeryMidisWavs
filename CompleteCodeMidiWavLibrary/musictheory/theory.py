from .config import CHORD_FORMULAS, ROMAN_TO_CHORD

def chord_inversions(formula):
    return [formula[i:] + [n+12 for n in formula[:i]] for i in range(len(formula))]

def roman_to_midi_progression(roman_seq, root_midi, key_mode="major"):
    out = []
    for rn in roman_seq:
        if rn not in ROMAN_TO_CHORD:
            continue
        degree, chord_type = ROMAN_TO_CHORD[rn]
        chord = [root_midi + degree + n for n in CHORD_FORMULAS[chord_type]]
        out.append(chord)
    return out
