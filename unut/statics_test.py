from statics import with_statics

def qux():
    print('Qux')
    return 0

@with_statics
def foo(static, x):
    static.init.s = static.declare.s and qux()
    static.s += x
    print(static.s)

foo(1)
foo(2)
foo(3)


class Bar:
    @with_statics
    def foo(static, self):
        static.init.s = static.declare.s and 0
        static.s += 2
        print(static.s)


b = Bar()
b.foo()
b.foo()
b.foo()
b.foo()
