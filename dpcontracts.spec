#
# This file is auto-generated. DO NOT EDIT
# Generated by: autospec.py
#
Name     : dpcontracts
Version  : 0.6.0
Release  : 8
URL      : https://files.pythonhosted.org/packages/aa/e2/cad64673297a634a623808045d416ed85bad1c470ccc99e0cdc7b13b9774/dpcontracts-0.6.0.tar.gz
Source0  : https://files.pythonhosted.org/packages/aa/e2/cad64673297a634a623808045d416ed85bad1c470ccc99e0cdc7b13b9774/dpcontracts-0.6.0.tar.gz
Summary  : A simple implementation of contracts for Python.
Group    : Development/Tools
License  : LGPL-2.1
Requires: dpcontracts-python = %{version}-%{release}
Requires: dpcontracts-python3 = %{version}-%{release}
BuildRequires : buildreq-distutils3

%description
Introduction
============
This module provides a collection of decorators that makes it easy to
write software using contracts.

Contracts are a debugging and verification tool.  They are declarative
statements about what states a program must be in to be considered
"correct" at runtime.  They are similar to assertions, and are verified
automatically at various well-defined points in the program.  Contracts can
be specified on functions and on classes.

Contracts serve as a form of documentation and a way of formally
specifying program behavior.  Good practice often includes writing all of
the contracts first, with these contract specifying the exact expected
state before and after each function or method call and the things that
should always be true for a given class of object.

Contracts consist of two parts: a description and a condition.  The
description is simply a human-readable string that describes what the
contract is testing, while the condition is a single function that tests
that condition.  The condition is executed automatically and passed certain
arguments (which vary depending on the type of contract), and must return
a boolean value: True if the condition has been met, and False otherwise.

Legacy Python Support
=====================
This module supports versions of Python >= 3.5; that is, versions with
support for "async def" functions.  There is a branch of this module that
is kept compatible to the greatest possible degree for versions of Python
earlier than 3.5 (including Python 2.7).

The Python 2 and <= 3.5 branch is available at
https://github.com/deadpixi/contracts/tree/python2

This legacy-compatible version is also distributed on PyPI along the 0.5.x
branch; this branch will kept compatible with newer versions to the greatest
extent possible.

That branch is a drop-in replacement for this module and includes all
functionality except support for "async def" functions.

Preconditions and Postconditions
================================
Contracts on functions consist of preconditions and postconditions.
A precondition is declared using the `requires` decorator, and describes
what must be true upon entrance to the function. The condition function
is passed an arguments object, which as as its attributes the arguments
to the decorated function:

    >>> @require("`i` must be an integer", lambda args: isinstance(args.i, int))
    ... @require("`j` must be an integer", lambda args: isinstance(args.j, int))
    ... def add2(i, j):
    ...   return i + j

Note that an arbitrary number of preconditions can be stacked on top of
each other.

These decorators have declared that the types of both arguments must be
integers.  Calling the `add2` function with the correct types of arguments
works:

    >>> add2(1, 2)
    3

But calling with incorrect argument types (violating the contract) fails
with a PreconditionError (a subtype of AssertionError):

    >>> add2("foo", 2)
    Traceback (most recent call last):
    PreconditionError: `i` must be an integer

Functions can also have postconditions, specified using the `ensure`
decorator.  Postconditions describe what must be true after the function
has successfully returned.  Like the `require` decorator, the `ensure`
decorator is passed an argument object.  It is also passed an additional
argument, which is the result of the function invocation.  For example:

    >>> @require("`i` must be a positive integer",
    ...          lambda args: isinstance(args.i, int) and args.i > 0)
    ... @require("`j` must be a positive integer",
    ...          lambda args: isinstance(args.j, int) and args.j > 0)
    ... @ensure("the result must be greater than either `i` or `j`",
    ...         lambda args, result: result > args.i and result > args.j)
    ... def add2(i, j):
    ...     if i == 7:
    ...        i = -7 # intentionally broken for purposes of example
    ...     return i + j

We can now call the function and ensure that everything is working correctly:

    >>> add2(1, 3)
    4

Except that the function is broken in unexpected ways:

    >>> add2(7, 4)
    Traceback (most recent call last):
    PostconditionError: the result must be greater than either `i` or `j`

The function specifying the condition doesn't have to be a lambda; it can be
any function, and pre- and postconditions don't have to actually reference
the arguments or results of the function at all.  They can simply check
the function's environments and effects:

    >>> names = set()
    >>> def exists_in_database(x):
    ...   return x in names
    >>> @require("`name` must be a string", lambda args: isinstance(args.name, str))
    ... @require("`name` must not already be in the database",
    ...          lambda args: not exists_in_database(args.name.strip()))
    ... @ensure("the normalized version of the name must be added to the database",
    ...         lambda args, result: exists_in_database(args.name.strip()))
    ... def add_to_database(name):
    ...     if name not in names and name != "Rob": # intentionally broken
    ...         names.add(name.strip())

    >>> add_to_database("James")
    >>> add_to_database("Marvin")
    >>> add_to_database("Marvin")
    Traceback (most recent call last):
    PreconditionError: `name` must not already be in the database
    >>> add_to_database("Rob")
    Traceback (most recent call last):
    PostconditionError: the normalized version of the name must be added to the database

All of the various calling conventions of Python are supported:

    >>> @require("`a` is an integer", lambda args: isinstance(args.a, int))
    ... @require("`b` is a string", lambda args: isinstance(args.b, str))
    ... @require("every member of `c` should be a boolean",
    ...          lambda args: all(isinstance(x, bool) for x in args.c))
    ... def func(a, b="Foo", *c):
    ...     pass

    >>> func(1, "foo", True, True, False)
    >>> func(b="Foo", a=7)
    >>> args = {"a": 8, "b": "foo"}
    >>> func(**args)
    >>> args = (1, "foo", True, True, False)
    >>> func(*args)
    >>> args = {"a": 9}
    >>> func(**args)
    >>> func(10)

A common contract is to validate the types of arguments. To that end,
there is an additional decorator, `types`, that can be used
to validate arguments' types:

    >>> class ExampleClass:
    ...     pass

    >>> @types(a=int, b=str, c=(type(None), ExampleClass)) # or types.NoneType, if you prefer
    ... @require("a must be nonzero", lambda args: args.a != 0)
    ... def func(a, b, c=38):
    ...     return " ".join(str(x) for x in [a, b])

    >>> func(1, "foo", ExampleClass())
    '1 foo'

    >>> func(1.0, "foo", ExampleClass) # invalid type for `a`
    Traceback (most recent call last):
    PreconditionError: the types of arguments must be valid

    >>> func(1, "foo") # invalid type (the default) for `c`
    Traceback (most recent call last):
    PreconditionError: the types of arguments must be valid

Contracts on Classes
====================
The `require` and `ensure` decorators can be used on class methods too,
not just bare functions:

    >>> class Foo:
    ...     @require("`name` should be nonempty", lambda args: len(args.name) > 0)
    ...     def __init__(self, name):
    ...         self.name = name

    >>> foo = Foo()
    Traceback (most recent call last):
    TypeError: __init__ missing required positional argument: 'name'

    >>> foo = Foo("")
    Traceback (most recent call last):
    PreconditionError: `name` should be nonempty

Classes may also have an additional sort of contract specified over them:
the invariant.  An invariant, created using the `invariant` decorator,
specifies a condition that must always be true for instances of that class.
In this case, "always" means "before invocation of any method and after
its return" -- methods are allowed to violate invariants so long as they
are restored prior to return.

Invariant contracts are passed a single variable, a reference to the
instance of the class. For example:

    >>> @invariant("inner list can never be empty", lambda self: len(self.lst) > 0)
    ... @invariant("inner list must consist only of integers",
    ...            lambda self: all(isinstance(x, int) for x in self.lst))
    ... class NonemptyList:
    ...     @require("initial list must be a list", lambda args: isinstance(args.initial, list))
    ...     @require("initial list cannot be empty", lambda args: len(args.initial) > 0)
    ...     @ensure("the list instance variable is equal to the given argument",
    ...             lambda args, result: args.self.lst == args.initial)
    ...     @ensure("the list instance variable is not an alias to the given argument",
    ...             lambda args, result: args.self.lst is not args.initial)
    ...     def __init__(self, initial):
    ...         self.lst = initial[:]
    ...
    ...     def get(self, i):
    ...         return self.lst[i]
    ...
    ...     def pop(self):
    ...         self.lst.pop()
    ...
    ...     def as_string(self):
    ...         # Build up a string representation using the `get` method,
    ...         # to illustrate methods calling methods with invariants.
    ...         return ",".join(str(self.get(i)) for i in range(0, len(self.lst)))

    >>> nl = NonemptyList([1,2,3])
    >>> nl.pop()
    >>> nl.pop()
    >>> nl.pop()
    Traceback (most recent call last):
    PostconditionError: inner list can never be empty

    >>> nl = NonemptyList(["a", "b", "c"])
    Traceback (most recent call last):
    PostconditionError: inner list must consist only of integers

Violations of invariants are ignored in the following situations:

    - before calls to __init__ and __new__ (since the object is still
      being initialized)

    - before and after calls to any method whose name begins with "__",
      except for methods implementing arithmetic and comparison operations
      and container type emulation (because such methods are private and
      expected to manipulate the object's inner state, plus things get hairy
      with certain applications of `__getattr(ibute)?__`)

    - before and after calls to methods added from outside the initial
      class definition (because invariants are processed only at class
      definition time)

    - before and after calls to classmethods, since they apply to the class
      as a whole and not any particular instance

For example:

    >>> @invariant("`always` should be True", lambda self: self.always)
    ... class Foo:
    ...     always = True
    ...
    ...     def get_always(self):
    ...         return self.always
    ...
    ...     @classmethod
    ...     def break_everything(cls):
    ...         cls.always = False

    >>> x = Foo()
    >>> x.get_always()
    True
    >>> x.break_everything()
    >>> x.get_always()
    Traceback (most recent call last):
    PreconditionError: `always` should be True

Also note that if a method invokes another method on the same object,
all of the invariants will be tested again:

    >>> nl = NonemptyList([1,2,3])
    >>> nl.as_string() == '1,2,3'
    True

Transforming Data in Contracts
==============================
In general, you should avoid transforming data inside a contract; contracts
themselves are supposed to be side-effect-free.

However, this is not always possible in Python.

Take, for example, iterables passed as arguments. We might want to verify
that a given set of properties hold for every item in the iterable. The
obvious solution would be to do something like this:

    >>> @require("every item in `l` must be > 0", lambda args: all(x > 0 for x in args.l))
    ... def my_func(l):
    ...     return sum(l)

This works well in most situations:

    >>> my_func([1, 2, 3])
    6
    >>> my_func([0, -1, 2])
    Traceback (most recent call last):
    PreconditionError: every item in `l` must be > 0

But it fails in the case of a generator:

    >>> def iota(n):
    ...     for i in range(1, n):
    ...         yield i

    >>> sum(iota(5))
    10
    >>> my_func(iota(5))
    0

The call to `my_func` has a result of 0 because the generator was consumed
inside the `all` call inside the contract. Obviously, this is problematic.

Sadly, there is no generic solution to this problem. In a statically-typed
language, the compiler can verify that some properties of infinite lists
(though not all of them, and what exactly depends on the type system).

We get around that limitation here using an additional decorator, called
`transform` that transforms the arguments to a function, and a function
called `rewrite` that rewrites argument tuples.

For example:

    >>> @transform(lambda args: rewrite(args, l=list(args.l)))
    ... @require("every item in `l` must be > 0", lambda args: all(x > 0 for x in args.l))
    ... def my_func(l):
    ...     return sum(l)
    >>> my_func(iota(5))
    10

Note that this does not completely solve the problem of infinite sequences,
but it does allow for verification of any desired prefix of such a sequence.

This works for class methods too, of course:

    >>> class TestClass:
    ...     @transform(lambda args: rewrite(args, l=list(args.l)))
    ...     @require("every item in `l` must be > 0", lambda args: all(x > 0 for x in args.l))
    ...     def my_func(self, l):
    ...         return sum(l)
    >>> TestClass().my_func(iota(5))
    10

Contracts on Asynchronous Functions (aka coroutine functions)
=============================================================
Contracts can be placed on coroutines (that is, async functions):

    >>> import asyncio
    >>> @require("`a` is an integer", lambda args: isinstance(args.a, int))
    ... @require("`b` is a string", lambda args: isinstance(args.b, str))
    ... @require("every member of `c` should be a boolean",
    ...          lambda args: all(isinstance(x, bool) for x in args.c))
    ... async def func(a, b="Foo", *c):
    ...     await asyncio.sleep(1)

    >>> asyncio.get_event_loop().run_until_complete(
    ...     func( 1, "foo", True, True, False))

Predicates functions themselves cannot be coroutines, as this could
influence the run loop:

    >>> async def coropred_aisint(e):
    ...     await asyncio.sleep(1)
    ...     return isinstance(getattr(e, 'a'), int)
    >>> @require("`a` is an integer", coropred_aisint)
    ... @require("`b` is a string", lambda args: isinstance(args.b, str))
    ... @require("every member of `c` should be a boolean",
    ...          lambda args: all(isinstance(x, bool) for x in args.c))
    ... async def func(a, b="Foo", *c):
    ...     await asyncio.sleep(1)
    Traceback (most recent call last):
    AssertionError: contract predicates cannot be coroutines

Contracts and Debugging
=======================
Contracts are a documentation and testing tool; they are not intended
to be used to validate user input or implement program logic.  Indeed,
running Python with `__debug__` set to False (e.g. by calling the Python
intrepreter with the "-O" option) disables contracts.

Testing This Module
===================
This module has embedded doctests that are run with the module is invoked
from the command line.  Simply run the module directly to run the tests.

Contact Information and Licensing
=================================
This module has a home page at `GitHub <https://github.com/deadpixi/contracts>`_.

This module was written by Rob King (jking@deadpixi.com).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

%package python
Summary: python components for the dpcontracts package.
Group: Default
Requires: dpcontracts-python3 = %{version}-%{release}

%description python
python components for the dpcontracts package.


%package python3
Summary: python3 components for the dpcontracts package.
Group: Default
Requires: python3-core
Provides: pypi(dpcontracts)

%description python3
python3 components for the dpcontracts package.


%prep
%setup -q -n dpcontracts-0.6.0
cd %{_builddir}/dpcontracts-0.6.0

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C.UTF-8
export SOURCE_DATE_EPOCH=1582920871
# -Werror is for werrorists
export GCC_IGNORE_WERROR=1
export CFLAGS="$CFLAGS -fno-lto "
export FCFLAGS="$CFLAGS -fno-lto "
export FFLAGS="$CFLAGS -fno-lto "
export CXXFLAGS="$CXXFLAGS -fno-lto "
export MAKEFLAGS=%{?_smp_mflags}
python3 setup.py build

%install
export MAKEFLAGS=%{?_smp_mflags}
rm -rf %{buildroot}
python3 -tt setup.py build  install --root=%{buildroot}
echo ----[ mark ]----
cat %{buildroot}/usr/lib/python3*/site-packages/*/requires.txt || :
echo ----[ mark ]----

%files
%defattr(-,root,root,-)

%files python
%defattr(-,root,root,-)

%files python3
%defattr(-,root,root,-)
/usr/lib/python3*/*
