import traceback
def sum(a, b):
    try:
        a = int(a)
        b = int(b)
        c=a/b
    except ValueError as e:
        tb=traceback.format_exc()
        print(tb)
sum("4", "2.0")
