from sys import argv

max_col = {'red' : 12, 'green' : 13, 'blue' : 14 }

with open(argv[1]) as f:
    result = 0
    for l in f.read().splitlines():
        max_counts = { c:0 for c in max_col.keys() }
        game, cols = l.split(": ")
        for turn in cols.split("; "):
            for col_str in turn.split(", "):
                cnt_str, col = col_str.split(" ")
                cnt = int(cnt_str)
                if cnt > max_counts[col]:
                    max_counts[col] = cnt
        if min([ max_counts[c] <= max_col[c] for c in max_col.keys()]):
            result += int(game.split(" ")[1])
    print(result)
