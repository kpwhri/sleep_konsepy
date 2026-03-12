def check_pattern(sentence, expected_val, *patterns):
    """Checks if any pattern in pattern_list matches the sentence and captures expected_val."""
    found = False
    for pat in patterns:
        m = pat.search(sentence)
        if m and 'val' in m.groupdict():
            if m.group('val') == str(expected_val):
                found = True
                break
            else:
                print(f'Found unexpected: {m.group("val")}.')
        print(f'Pattern not found: {pat}')
    return found
