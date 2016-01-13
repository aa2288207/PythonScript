import inspect

class A:
  def a(self):
    print("A.a()")
    B().b()

class B:
  def b(self):
    print("B.b()")
    stack = inspect.stack()
    the_class = stack[1][0].f_locals["self"].__class__
    the_method = stack[1][0].f_code.co_name
    print("  I was called by {}.{}()".format(str(the_class), the_method))

A().a()