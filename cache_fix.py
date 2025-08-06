"""
A simple script to convert old cache format to new format.
From storing just the guesses to store guess, rank, and foils
"""
import os
import time
import json
import wordle_contexts

new_cache_dir = "cache"
# old_cache_dir = "cache.2"
old_cache_dir = "cachej"

def main():
    """Convert old cache to new cache."""
    start = time.perf_counter()

    # Go through all game contexts
    for context in wordle_contexts.get_all_contexts():
        # Check if old cache exists
        new_filename = context._guesses_filename()
        old_filename = os.path.join(old_cache_dir, os.path.relpath(new_filename, new_cache_dir))

        try:
            with open(old_filename) as f:
                old_guesses = json.load(f)
        except FileNotFoundError:
            continue

        print(f"Fixing cache for {'naive' if context.naive else 'smart'} {context.name} Length {context.word_length}")

        # Convert old cache to new cache
        solution_group = context.get_solution_group()

        best_rank = None
        best_guesses = []
        best_foils = []
        for guess in old_guesses:
            rank, foil = solution_group.guess_rank(guess)

            if best_rank is None:
                best_rank = rank
            else:
                assert rank == best_rank

            best_guesses.append(guess)
            best_foils.append(foil)

        # Save new cache
        context.save_guesses(best_rank, best_guesses, best_foils)

    stop = time.perf_counter()
    print(f"Built cache in {stop - start:.4f} seconds.")

if __name__ == "__main__":
    main()
