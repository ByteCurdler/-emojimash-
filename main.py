import operator
import sys
import copy


class chars:
    number = "🔢"
    string = "🔤"
    true = "🗹"
    false = "🗷"
    null = "🚫"
    string_escape = "❕"
    math = "🧮"
    math_ops = {
        "➕": (operator.add, 2),
        "➖": (operator.sub, 2),
        "✖": (operator.mul, 2),
        "➗": (operator.floordiv, 2),
        "⚙": (operator.mod, 2),
        "⤴": (operator.pow, 2),
        "⁺": (operator.pow, 2),
        "🟰": (operator.eq, 2),
        "＝": (operator.eq, 2),
        "🔄": (operator.neg, 1),
        "‼": (operator.not_, 1),
        "🔢": (int, 1),
        "🔤": (str, 1),
        "❓": (bool, 1),
        "📜": (list, 1),
    }
    makelist = "📜"
    makedict = "📙"
    getitem = "🔍"
    print = "🖨"
    print_nl = "📠"  # Print with newline
    delete = "🗑"
    comment = "💬"
    label = "🏷"
    goto = "🎠"
    gotoif = "🚀"
    copy = "📋"
    no_op = "\n\t \uFe0F"  # Fe0F == Variation Selector-16 (makes emoji)
    input = "⌨"
    length = "📏"
    pop = "🎉"
    stack = "📚"
    setitem = "📝"
    swap = "🔄"
    callfunc = "🐸"
    return_ = "🛑"
    eraseitem = "🖍"


def lexify(text):
    inp = list(text.replace("\uFe0F", ""))  # Fe0F == Variation Selector-16
    code = []
    labels = {}
    while inp:
        symbol = inp.pop(0)
        symname = [i for i in dir(chars) if getattr(chars, i) == symbol]
        if symname:
            symname = symname[0].rstrip("_")  # For things like return_
        else:
            symname = None
        # print(symbol, symname)
        if symname == "string":
            buffer = ""
            while (char := inp.pop(0)) != chars.string:
                if char == chars.string_escape:
                    char2 = inp.pop(0)
                    if char2 in (chars.string, chars.string_escape):
                        buffer += char2
                    else:
                        buffer += char + char2
                else:
                    buffer += char
            code.append(("push", buffer))
        elif symname == "math":
            op = inp.pop(0)
            if op in chars.math_ops:
                code.append(("math", op))
        elif symname in ("makelist", "makedict", "getitem", "copy", "length",
                         "stack", "print", "print_nl", "delete", "input",
                         "pop", "setitem", "swap", "return", "eraseitem"):
            code.append((symname,))
        elif symname in ("comment", "label", "goto", "gotoif", "number",
                         "callfunc"):
            ind = inp.index(symbol)
            buffer = "".join(inp[:ind])
            inp = inp[ind+1:]
            if symname == "label":
                labels[buffer] = len(code)
            if symname in ("goto", "gotoif", "callfunc"):
                code.append((symname, buffer))
            if symname == "number":
                code.append(("push", int(buffer)))
        elif symname in ("true", "false", "null"):
            code.append(("push", {
                "true": True,
                "false": False,
                "null": None
            }[symname]))
        elif symbol not in chars.no_op:
            print(f"error: unknown char '{symbol}' ({symname=})")
            sys.exit()

    return code, labels


def run(code, labels):
    pc = 0
    stack = []
    funcstack = []
    while pc < len(code):
        cmd, *args = code[pc]
        if cmd == "push":
            stack.append(args[0])
        if cmd == "math":
            op, numargs = chars.math_ops[args[0]]
            items = [stack.pop() for _ in range(numargs)][::-1]
            stack.append(op(*items))
        if cmd == "list":
            if type(stack[-1]) is int:
                num = stack.pop()
                stack.append([stack.pop() for _ in range(num)][::-1])
        if cmd == "dict":
            if type(stack[-1]) is list and type(stack[-2]) is list:
                stack.append(dict(zip(stack.pop(), stack.pop())))
        if cmd == "getitem":
            ind = stack.pop()
            stack.append(stack[-1][ind])
        if cmd == "print":
            print(stack[-1], end="")
        if cmd == "print_nl":
            print(stack[-1])
        if cmd == "delete":
            stack.pop()
        if cmd == "goto":
            pc = labels[args[0]]-1
        if cmd == "gotoif":
            if stack.pop():
                pc = labels[args[0]]-1
        if cmd == "copy":
            stack.append(copy.deepcopy(stack[-1]))
        if cmd == "input":
            stack.append(input())
        if cmd == "length":
            stack.append(len(stack[-1]))
        if cmd == "pop":
            if type(stack[-1]) is str:
                stack.append(stack[-1][0])
                stack[-2] = stack[-2][1:]
            else:
                stack.append(stack[-1].pop(0))
        if cmd == "stack":
            stack.append(copy.deepcopy(stack))
        if cmd == "setitem":
            ind = stack.pop()
            stack[-1][ind] = stack.pop()
        if cmd == "swap":
            N = stack.pop()
            stack[-N], stack[-1] = stack[-1], stack[-N]
        if cmd == "callfunc":
            funcstack.append(pc)
            pc = labels[args[0]]-1
        if cmd == "return":
            if funcstack:
                pc = funcstack.pop()
            else:
                return
        if cmd == "eraseitem":
            ind = stack.pop()
            del stack[-1][ind]
        pc += 1


eraseitem = "🖍"

# code = "🔢123🔢📠🔢2🔢🧮➕📠️🗑💬text📜wahoo📜📠️"
️  # code = """
# 🔢5🔢🏷️🏷📠🔢🏷➖📋🚀🧮🚀
# """
# code = """
# 🔢5🔢🔢2🔢🧮➕
# 🔢5🔢🔢2🔢🧮➖
# 🔢5🔢🔢2🔢🧮✖
# 🔢5🔢🔢2🔢🧮➗
# 🔢5🔢🔢2🔢🧮⚙
# 🔢5🔢🔢2🔢🧮⤴️
️  # 🔢5🔢🔢2🔢🧮＝
# 🔢5🔢🧮🔄
# 🔢5🔢🧮‼️
️  # 🔤50🔤🧮🔢
# 🔢5🔢🧮🔤
# 🗹🧮🔤
# 📚🧮🔤
# 🔢5🔢🧮❓
# 📚🧮❓
# 🔤🔤🧮❓
# 🔢0🔢📜🧮❓
# 🔤🎉hello🎉🔤🧮📜
# 📚
# 🏷🏷️🏷#     🎉
#     📠
#     🗑
#     📏
# 🚀📚🚀
# """
# code = """
# 🔤You did "🔤
# 🔤input> 🔤🐸🖨⌨🐸
# 🔤"🔤
# 🧮➕🧮➕📠
#
# 🛑
# 🏷⌨🏷️🏷🖨🗑⌨
# 🛑
# """
code = """
🔢1🔢 🔢9🔢 🏷🔄🏷 🗑
cp0 P# " " P1 0d1
+x cp0 0d11 -x
GotoIf(for pop pop
"""
lex = lexify(code)
# print(lex)
run(*lex)
# print(lex)
run(*lex)
