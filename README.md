Snippety
=========

Snippety generates code inside your code from your code.

###Wait......it does what?

Sometime end up with stuff like this:
``` python
def __init__(self, dataRow):
    self._name = dataRow.name
    self._age = dataRow.age
    self._height = dataRow.height
    self._weight = dataRow.weight
    ###
    ### Duplication plain to see, but no simple way to avoid it*
    ###
    print "created ", self.name
```
(_You could solve this particular example with **getattr()** and **setattr()** because it's Python, but this is just an example for illustration. Snippety works on any text files._)

With Snippety, you type a directive in a comment:

``` python
def __init__(self, dataRow):
    self._name = dataRow.name         #sn_i [name] age height weight
    print "created ", self.name
```

And it generates this:

``` python
def __init__(self, dataRow):
    self._name = dataRow.name         #sn_i [name] age height weight
    self._age = dataRow.age           #generated_code
    self._height = dataRow.height     #generated_code
    self._weight = dataRow.weight     #generated_code
    print "created ", self.name
```

###Why is this special?

__A)__ Because you create the instructions to generate new lines of code right from inside your code. No need to open up an external tool. 

__B)__ It is dynamic, so if you change your directive, and rerun Snippety, it updates your files, removing its own generated lines, but leaving everything else untouched.

``` python
def __init__(self, dataRow):
    self._name = dataRow.name         #sn_i [name] weight
    self._weight = dataRow.weight     #generated_code
    print "created ", self.name
```
How cool is that?

__C)__ There are different types of directives to handle things like enumeration, capitalisation, or reading values from a config file, and you can easily write your own.

Here's an example using enumeration, and showing a directive with start (__sn_s__) and end (__sn_e__) directives as opposed to the inline (__sn_i__) shown above.

``` python
def __init__(self, dataRow):
    #sn_s [name, 0*1] age height weight
    self.name = dataRow[0]
    #sn_e
    self._age = dataRow[1]        #generated_code
    self._height = dataRow[2]     #generated_code
    self._weight = dataRow[3]     #generated_code
    print "created ", self.name
```

##Good to know:
 
 * Snippety regenerates the lines each time it is run, so you only need to change the original snippet.
 * You can have multi-line snippet, and even nested chunks within those!
 * You can direct the output to another file.
 * You can use key-value collections defined in a config file instead.
 * You can apply conditional statements (repeat for all elements if)
 * There's an easy enumeration [0, 1, 2...] feature
 * There's intelligent capitalsation handling
 * Snippety can be run as a tool, or easily integrated into a python script, with a simple OOP model that lets you modify or extend the functionality however you please.

##Important information:

Snippety replaces the contents of the file you're actually working on, so make sure your IDE tells you when the underlying file contents have changed (most do). 

__THERFORE YOU MUST REMEMBER TO SAVE YOUR FILES BEFORE RUNNING SNIPPETY OVER THEM!__


Alternatively you can tell Snippety to output to a different location, leaving your source files untouched.

##How to use it

At the moment you need to call it from Python by importing snippety and exploring the classes and their docs.

As a simple example, create a file called __test.txt__ with this:

```
I'm a cat       #sn_i [cat] dog squirrel piggy
```

And a python file called **run_snippety.py** in the same directory:

``` python
from snippety import Snippety
sn = Snippety()
sn.process_file(argv[1])
```
From the command line, run:

**>>> run_snippety.py test.txt**

And __test.txt__ should become:

```
I'm a cat       #sn_i [cat] dog squirrel piggy
I'm a dog       #generated code
I'm a squirrel  #generated code
I'm a piggy     #generated code
```

There is more you can do, such as:
``` python
# process_dir catches all the files in a directory.
# can be passed include and exclude lists
sn.process_dir('.')
```
Unfortunately you'll have to look into the source code and unit tests to get an idea of what directives are working and available.

More documentation is coming :-)

##Tests

Snippety uses [pytest](http://pytest.org/latest/) for it's unit tests, and there's a fair amount of test that pass, but could do with more edge-case testing.

##Contribution guidelines

  * Stick to [Python Style Guide](http://legacy.python.org/dev/peps/pep-0008/)
  * Make sure the code is compatible with Python 2.7.

##Questions:

Email me at andyhasit@gmail.com.
