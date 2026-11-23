"""One Letter: Coffee or Tea — entry program.

Writes exactly one letter to /output/entry.txt: "A" for coffee.
Stdlib only, deterministic, no network, no model calls.

Why A (coffee), from the judge brief published in RULES.txt — the
criteria are weighed in this order: (1) exactly one letter, A or B
— both letters tie; (2) vivid — coffee lands as the fuller, more
alive answer: morning jolt, bitterness, steam, caffeine rush,
"but first, coffee"; tea is calm and quiet by comparison;
(3) funnier — coffee carries the sharper wit: caffeine addiction,
"don't talk to me before my coffee"; tea humour is milder;
(4) truer — coffee is the louder, more committed stance, the honest
answer of the person sending it; tea reads as the safe, polite one.
So A is the more vivid, funnier and truer single letter.
"""
import os

TEXT = "A"


def main():
    # Enforce the scorer's gate (RULES.txt): UTF-8, exactly 1 char,
    # not whitespace-only; and the task: exactly one letter, A or B.
    # Fail loudly instead of writing an invalid entry.
    if len(TEXT) != 1 or TEXT not in ("A", "B") or not TEXT.strip():
        raise SystemExit("entry text violates the 1-char A/B gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Write to a temp file in the same
    # directory, flush it to disk, then rename over the target.
    tmp_path = os.path.join(out_dir, ".entry.txt.tmp")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify: the file the grader reads must be byte-identical
    # to the gated text. Fail loudly instead of shipping a corrupt entry.
    with open(final_path, encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt read-back mismatch after atomic write")


if __name__ == "__main__":
    main()
