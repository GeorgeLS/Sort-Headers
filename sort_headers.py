import sys, fileinput

headers = []

def is_directive(_str):
    return _str.find("#define") != -1 or _str.find("#pragma") != -1

def extract_header(n, _str):
    s_pos = 0
    e_pos = 0
    cur_pos = 0
    for ch in _str:
        cur_pos += 1;
        if ch == '<' or ch == '"':
            s_pos = cur_pos
        if ch == '>' or ch == '"':
            e_pos = cur_pos - 1
    headers.append((n, _str[s_pos : e_pos]))

def read_headers_from_file(filename):
    file = open(filename, "r")
    line_n = 0
    for line in file:
        if line.find("#include") != -1:
            extract_header(line_n, line)
        elif line.find("#if") != -1:
            for aux_line_n, aux_line in enumerate(file):
                if aux_line.find("#endif") != -1:
                    break
            line_n += aux_line_n + 2
            continue
        elif is_directive(line) or line == "\n":
            pass
        else:
            break
        line_n += 1
    file.close()

def write_sorted_headers_to_file(filename):
    lst1, lst2 = zip(*headers)
    result = list(zip(lst1, sorted(lst2)))
    line_lst = [n[0] for n in result]
    for line_n, line in enumerate(fileinput.input(filename, inplace=True)):
        if line_n in line_lst:
            header = str([item[1] for item in result if line_n in item][0])
            print("#include<" + header + ">")
        else:
            sys.stdout.write(line)
    fileinput.close()

def main(argv):
    for filename in argv:
        read_headers_from_file(filename)
        write_sorted_headers_to_file(filename)
        del headers[:]

if __name__ == "__main__":
    main(sys.argv[1:])
