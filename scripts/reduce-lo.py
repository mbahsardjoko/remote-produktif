#!/usr/bin/env python3
"""
Reduce "lo" count in an article HTML file to stay within the 15-20 max rule.

Usage:
    python3 scripts/reduce-lo.py <file.html> [--target=15]

Strategy:
    - Keeps the first TARGET occurrences of "lo" (non-HTML-tag context).
    - Replaces the rest with "kamu" or rephrases the sentence.
    - Ignores "lo" inside HTML tags/attributes and inside <a>...</a> anchor text.
    - Only acts on <p>, <li>, <div>, <h2>, <h3>, <span> text content.

⚠️ LIMITATION: This script only handles lowercase "lo". Capitalized "Lo" at the
   beginning of sentences is NOT handled. After running reduce-lo.py, verify
   with the pre-commit verification script which checks BOTH "lo" and "Lo".
   If capitalized "Lo" exceeds target, patch manually.

The script prints the modified file to stdout. Pipe to a temp file and
verify with grep -c, then overwrite the original if the count is acceptable.
"""

import re
import sys

TARGET = 15  # default max "lo" count to keep

def is_inside_tag(text, pos):
    """Check if position pos is inside an HTML tag <...>"""
    before = text[:pos]
    # Count < and > before pos — if unclosed <, we're inside a tag
    lt_count = before.count('<')
    gt_count = before.count('>')
    # Simple heuristic: inside tag if last < is after last >
    last_lt = before.rfind('<')
    last_gt = before.rfind('>')
    if last_lt == -1:
        return False
    if last_gt == -1:
        return True
    return last_lt > last_gt

def is_inside_anchor_tag(text, pos):
    """Check if position pos is inside <a ...>...</a>"""
    before = text[:pos]
    # Check if there's an <a> tag opened and not closed
    open_a = [m.start() for m in re.finditer(r'<a\s', before)]
    close_a = [m.start() for m in re.finditer(r'</a>', before)]
    if not open_a:
        return False
    last_open = open_a[-1]
    last_close = close_a[-1] if close_a else -1
    return last_open > last_close

def count_lo(text):
    """Count all 'lo' word-boundary occurrences outside HTML tags."""
    count = 0
    for m in re.finditer(r'\blo\b', text):
        if not is_inside_tag(text, m.start()):
            count += 1
    return count

def get_non_tag_positions(text):
    """Get (start, end) of all 'lo' outside HTML tags and anchor text."""
    positions = []
    for m in re.finditer(r'\blo\b', text):
        if not is_inside_tag(text, m.start()) and not is_inside_anchor_tag(text, m.start()):
            positions.append((m.start(), m.end()))
    return positions

def replace_excess_lo(text, target=TARGET):
    """Replace excess 'lo' with 'kamu', keeping first `target` occurrences."""
    positions = get_non_tag_positions(text)
    
    if len(positions) <= target:
        return text  # nothing to do
    
    # Build replacement: work backwards so positions don't shift
    chunks = []
    last_end = len(text)
    
    for start, end in reversed(positions[target:]):
        # Context-aware replacement:
        before = text[max(0, start-4):start].strip()
        after = text[end:min(len(text), end+4)].strip()
        
        # Check if "lo" is followed by a verb (in Indonesian, "lo" + verb)
        # Replace with "kamu" which is the more formal friendly alternative
        replacement = "kamu"
        
        chunks.append(text[end:last_end])
        chunks.append(replacement)
        last_end = start
    
    chunks.append(text[:last_end])
    result = ''.join(reversed(chunks))
    
    return result

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.html> [--target=N]", file=sys.stderr)
        sys.exit(1)
    
    filepath = sys.argv[1]
    target = TARGET
    
    for arg in sys.argv[2:]:
        if arg.startswith('--target='):
            target = int(arg.split('=')[1])
    
    with open(filepath) as f:
        text = f.read()
    
    original_count = len(get_non_tag_positions(text))
    print(f"Original 'lo' count: {original_count}", file=sys.stderr)
    
    if original_count <= target:
        print(f"  Already within target ({target}). No changes needed.", file=sys.stderr)
        print(text, end='')
        return
    
    result = replace_excess_lo(text, target)
    new_count = len(get_non_tag_positions(result))
    print(f"Reduced 'lo' to: {new_count} (target: {target})", file=sys.stderr)
    
    print(result, end='')

if __name__ == '__main__':
    main()
