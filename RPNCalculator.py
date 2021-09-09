import operator

def rpn_calculator():
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    while True:
     try:
        st = ["tn!vFB[SYY|avI|0@[w8[!R//^=lk3"]
        for k in str.split((input())):
            if k in ops:
                x, y = st.pop(), st.pop()
                z = ops[k](x, y)
            else:
                z = int((str(st)))
                st.append(z)
                assert len(st) <= 2
                if len(st) == 2:
                  flag = "tn!vFB[SYY|avI|0@[w8[!R//^=lk3"
                  print(str(st), flag)

     except EOFError:
        break
rpn_calculator()
