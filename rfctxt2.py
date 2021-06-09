import sys
import re

# インデントの長さを計算する
def indc(line):
    r = 0
    for c in line:
        if c != ' ':
            break
        r = r + 1
    return r

def rfctxt_format(path, out=sys.stdout):
    indent = 0

    # 全部読み込み
    with open(path) as f:
        all = f.read()

    # ページのヘッダ・フッタを削除。区切りは置いておく
    all = re.sub('\n\n\n[^\n\x0c]+\n\x0c\nRFC[^\n]+\n\n\n', '\x0c\n', all)

    # ページ区切り前に空行が入ってるケースがある。空行前が . じゃなくて空行後が小文字で始まってる場合は連続してると判断。
    all = re.sub('([^\n.]\n)\n\x0c\n(\s+[a-z])', r'\1\2', all)

    # ページ区切りを削除
    all = re.sub('\x0c\n', '', all)


    # 行ごとに分割

    lines = all.splitlines(keepends=False)

    ind_pre = 0
    len_pre = 0
    last = '.'
    bull = False
    for line in lines:
        ind = indc(line)
        # 箇条書きの先頭
        if re.match('^[ ]+[0-9.]+[ ]+', line) or \
        re.match('^[ ]+[o;/#+\-*][ ]+', line):
            print('', file=out)
            print(line, end='', file=out)
            bull = True
        # 前の行の続きの可能性がある
        elif ind > 0 and ind_pre > 0 and last != '.' and len_pre > 60:
            if not bull and ind != ind_pre:
                print('', file=out)
                print(line, end='', file=out)
            else:
                print(line[ind-1:], end='', file=out)
        else:
            print('', file=out)
            print(line, end='', file=out)
            bull = False

        ind_pre = ind
        if line:
            last = line[-1]
            len_pre = len(line)

if __name__ == '__main__':

    # usage
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <input_file.txt>')
        sys.exit(1)

    # 第2引数に出力ファイルパス
    if len(sys.argv) > 2:
        try:
            with open(sys.argv[2], 'w') as out:
                rfctxt_format(sys.argv[1], out)
                exit(0)

        except OSError as e:
            print(e)
            exit(1)

    rfctxt_format(sys.argv[1])
