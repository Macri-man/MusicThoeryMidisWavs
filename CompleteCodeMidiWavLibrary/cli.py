import argparse
import os
import random
from musictheory.arranger import generate_song
from musictheory.config import NOTE_NUMS, GENRES


# Mapping enharmonic equivalents (Db → C#, etc.)
ENHARMONIC_EQUIVS = {
    "DB": "C#",
    "EB": "D#",
    "GB": "F#",
    "AB": "G#",
    "BB": "A#",
}


def normalize_note(note: str) -> str:
    """Normalize input note, fixing enharmonics if needed."""
    note = note.strip().upper()
    return ENHARMONIC_EQUIVS.get(note, note)


def main():
    parser = argparse.ArgumentParser(
        description="🎶 Simple Music Theory MIDI Generator",
        epilog="Examples:\n"
               "  python cli.py C jazz -o my_song.mid\n"
               "  python cli.py --random\n"
               "  python cli.py --batch 5 --prefix jam\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "root", nargs="?", help=f"Root note (available: {', '.join(NOTE_NUMS.keys())})"
    )
    parser.add_argument(
        "genre", nargs="?", help=f"Genre (available: {', '.join(GENRES.keys())})"
    )
    parser.add_argument(
        "-o", "--output", default="song.mid", help="Output MIDI file name (default: song.mid)"
    )
    parser.add_argument(
        "--list", action="store_true", help="List all available notes and genres"
    )
    parser.add_argument(
        "--random", action="store_true", help="Generate with a random root and genre"
    )
    parser.add_argument(
        "--length", type=int, default=None, help="Optional song length (bars/measures)"
    )
    parser.add_argument(
        "--batch", type=int, default=0, help="Generate N random songs in batch mode"
    )
    parser.add_argument(
        "--prefix", default="song", help="Prefix for batch output files (default: song)"
    )

    args = parser.parse_args()

    # Handle list mode
    if args.list:
        print("🎵 Available root notes:")
        print("   " + ", ".join(NOTE_NUMS.keys()))
        print("\n🎼 Available genres:")
        print("   " + ", ".join(GENRES.keys()))
        return

    # Handle batch mode
    if args.batch > 0:
        print(f"📦 Generating {args.batch} random songs with prefix '{args.prefix}'...")
        for i in range(1, args.batch + 1):
            root = random.choice(list(NOTE_NUMS.keys()))
            genre = random.choice(list(GENRES.keys()))
            out_file = f"{args.prefix}_{i}.mid"
            print(f"🎲 [{i}/{args.batch}] Root={root}, Genre={genre}, File={out_file}")
            if args.length:
                generate_song(NOTE_NUMS[root], genre, out_file, length=args.length)
            else:
                generate_song(NOTE_NUMS[root], genre, out_file)
        print("✅ Batch generation complete!")
        return

    # Handle random mode
    if args.random:
        root = random.choice(list(NOTE_NUMS.keys()))
        genre = random.choice(list(GENRES.keys()))
        print(f"🎲 Randomly chosen: Root={root}, Genre={genre}")
    else:
        if not args.root or not args.genre:
            print("❌ You must specify <root> and <genre> unless using --random or --batch.")
            return
        root = normalize_note(args.root)
        genre = args.genre.strip().lower()

    # Validate inputs
    if root not in NOTE_NUMS:
        print(f"❌ Invalid root note: {args.root}")
        print(f"   Try one of: {', '.join(NOTE_NUMS.keys())}")
        return
    if genre not in GENRES:
        print(f"❌ Invalid genre: {args.genre}")
        print(f"   Try one of: {', '.join(GENRES.keys())}")
        return

    # Generate single MIDI
    print(f"🎶 Generating song → Root: {root}, Genre: {genre}, Output: {args.output}")
    root_midi = NOTE_NUMS[root]

    if args.length:
        generate_song(root_midi, genre, args.output, length=args.length)
    else:
        generate_song(root_midi, genre, args.output)

    print(f"✅ Done! Saved to {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
