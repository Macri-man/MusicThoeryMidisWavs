import argparse, os
from musictheory.arranger import generate_song
from musictheory.config import NOTE_NUMS

def main():
    parser = argparse.ArgumentParser(description="Simple Music Theory MIDI Generator")
    parser.add_argument("root", help="Root note (C, D#, F#, etc.)")
    parser.add_argument("genre", help="Genre (pop, jazz, blues, etc.)")
    parser.add_argument("-o","--output", default="song.mid", help="Output MIDI file")
    args = parser.parse_args()

    if args.root not in NOTE_NUMS:
        print("❌ Invalid root note"); return

    root_midi = NOTE_NUMS[args.root]
    generate_song(root_midi, args.genre.lower(), args.output)

if __name__ == "__main__":
    main()
