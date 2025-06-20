#!/usr/bin/env python3
"""
prover.py - Python replacement for the Bash script.
Reads `inputs.txt` and writes `Prover.toml` with the same semantics.
"""

from pathlib import Path
import re
import sys

INPUT  = Path("inputs.txt")
OUTPUT = Path("Prover.toml")
TEXT   = INPUT.read_text()

# ---------- helpers ---------------------------------------------------------
def extract_value(key: str) -> str:
    """Return the value (inside quotes) for `key = "..."`."""
    m = re.search(rf'^{key}\s*=\s*"([^"]+)"', TEXT, re.M)
    if not m:
        sys.exit(f"{key} not found in {INPUT}")
    return m.group(1)


def strip_0x(s: str) -> str:
    return s[2:] if s.startswith("0x") else s


def hex_to_dec_list(hex_str: str) -> list[str]:
    """Convert an even-length hex string to a list of decimal bytes as strings."""
    if len(hex_str) % 2:                       # pad if someone forgot the leading 0
        hex_str = "0" + hex_str
    return [str(int(hex_str[i : i + 2], 16)) for i in range(0, len(hex_str), 2)]


def to_toml_array(items: list[str]) -> str:
    """Format a list of strings as a TOML array with quoted elements and no spaces."""
    return "[" + ",".join(f'"{item}"' for item in items) + "]"


# ---------- read & transform ------------------------------------------------
expected_address = extract_value("expected_address")     # keep its “0x”
hashed_message   = strip_0x(extract_value("hashed_message"))
pub_key_x        = strip_0x(extract_value("pub_key_x"))
pub_key_y        = strip_0x(extract_value("pub_key_y"))
signature        = strip_0x(extract_value("signature"))[:-2]   # drop last byte (v)

# convert to decimal byte-arrays
hashed_message_arr = to_toml_array(hex_to_dec_list(hashed_message))
pub_key_x_arr      = to_toml_array(hex_to_dec_list(pub_key_x))
pub_key_y_arr      = to_toml_array(hex_to_dec_list(pub_key_y))
signature_arr      = to_toml_array(hex_to_dec_list(signature))

# ---------- write -----------------------------------------------------------
OUTPUT.write_text(
    "\n".join(
        [
            f'expected_address = "{expected_address}"',
            f"hashed_message = {hashed_message_arr}",
            f"pub_key_x = {pub_key_x_arr}",
            f"pub_key_y = {pub_key_y_arr}",
            f"signature = {signature_arr}",
        ]
    )
    + "\n"
)

print(f"Wrote {OUTPUT}")