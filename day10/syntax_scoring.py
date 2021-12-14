def syntax_score():
    syntax_error_score = 0
    autocomplete_scores = set()
    for line in iter(puzzle_input.readline, ''):
        s = line.strip()
        for i in range(1000):
            s = s.replace('()', '')
            s = s.replace('<>', '')
            s = s.replace('[]', '')
            s = s.replace('{}', '')
        if s.find('[)') >= 0 or s.find('{)') >= 0 or s.find('<)') >= 0:
            syntax_error_score += 3
        elif s.find('(]') >= 0 or s.find('{]') >= 0 or s.find('<]') >= 0:
            syntax_error_score += 57
        elif s.find('(}') >= 0 or s.find('[}') >= 0 or s.find('<}') >= 0:
            syntax_error_score += 1197
        elif s.find('(>') >= 0 or s.find('[>') >= 0 or s.find('{>') >= 0:
            syntax_error_score += 25137
        else:
            #incomplete line
            line_autocomplete_score = 0
            s1 = list(s)
            while s1:
                line_autocomplete_score *= 5
                match s1.pop():
                    case '(':
                        line_autocomplete_score += 1
                    case '[':
                        line_autocomplete_score += 2
                    case '{':
                        line_autocomplete_score += 3
                    case '<':
                        line_autocomplete_score += 4
            autocomplete_scores.add(line_autocomplete_score)
    while len(autocomplete_scores)>1:
        autocomplete_scores.remove(min(autocomplete_scores))
        autocomplete_scores.remove(max(autocomplete_scores))
    return syntax_error_score, autocomplete_scores.pop()


if __name__ == '__main__':
    print("Advent of Code – Day 10: Syntax Scoring")
    with open('example.txt') as puzzle_input:
        syntax_error_score, autocomplete_score = syntax_score()
        print(f"The example's total syntax error score is {syntax_error_score}! The autocomplete score accounts for {autocomplete_score} points! Whoohoo.")
    with open('puzzle_input.txt') as puzzle_input:
        syntax_error_score, autocomplete_score = syntax_score()
        print(f"The puzzle's total syntax error score is {syntax_error_score}! The autocomplete score accounts for {autocomplete_score} points! Whoohoo.")
