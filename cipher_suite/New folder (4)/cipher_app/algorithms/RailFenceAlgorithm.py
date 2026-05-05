def RailFence(mode="decode", text="", rails=3):
    row = int(rails)
    if mode == "encode":
        words = text.replace(" ", "")
        length = len(words)
        x = []
        for i in range(row):
            for j in range(length):
                cycle = 2 * (row - 1)
                pos = j % cycle
                if pos == i or pos == cycle - i:
                    x.append(words[j])
        return "".join(x)
    elif mode == "decode":
        wordss = text.replace(" ", "")
        rows = row
        rail = []
        rails_list = []
        cycle = 2 * (rows - 1)
        fullycle = len(wordss) // cycle
        remainder = len(wordss) % cycle
        for i in range(rows):
            if i == 0 or i == rows - 1:
                rail.append(fullycle)
                rails_list.append(f"rail{i}")
            else:
                rail.append(2 * fullycle)
                rails_list.append(f"rail{i}")
        for k in range(remainder):
            if k < rows:
                rail[k] = rail[k] + 1
            elif k >= rows:
                for p in range(remainder - rows):
                    rail[max(range(rows)) - 1 - p] = rail[max(range(rows)) - 1 - p] + 1
                break
        Sum = 0
        for n in range(len(rails_list)):
            Sum += rail[n]
            if n == 0:
                rails_list[n] = wordss[:rail[n]]
            elif n > 0:
                rails_list[n] = wordss[Sum - rail[n]: Sum]
        n = len(wordss)
        rail_idx = [0] * rows
        current_row = 0
        direction = 1
        result = []
        for _ in range(n):
            result.append(rails_list[current_row][rail_idx[current_row]])
            rail_idx[current_row] += 1
            if current_row == rows - 1:
                direction = -1
            elif current_row == 0:
                direction = 1
            current_row += direction
        return "".join(result)
