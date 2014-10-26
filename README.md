Snippety
=========

Snippety generates reptitive snippets of code and inserts them back into your source file. It does so using very simple __directives__ in your comments, and uses your existing source code as template - a code generator that runs from inside your source files!

##Motivation
We sometimes end up writting a lot of code like this:
``` python
def constructor(record as DataRecord):
    self.name = record.GetValue('name')
    self.age = record.GetValue('age')
    self.height = record.GetValue('height')
    self.weight = record.GetValue('weight')
```
There are ways round this using reflection or structuring your classes differently, but in some cases that's not a viable option (not enough time/skill, or even performance issues) and you just wish you could treat your code like text with a __for__ loop.

With Snippety you just write the first snippet that repeats, and add a __snippety directive__ in your comments, either inline as in this example or by wrapping multiple lines.

``` python
    self.name = record.GetValue('name') #sn_i [name] age height weight
```

This directive effectively states: for x in __age height weight__: copy the snippet and replace __name__ with x.
Running the file through Snippety will result in this:

``` python
    self.name = record.GetValue('name') #sn_i [name] age height weight
    self.age = record.GetValue('age')               #generated_code
    self.height = record.GetValue('height')         #generated_code
    self.weight = record.GetValue('weight')         #generated_code
```

#####Good to know:
 
 * Snippety regenerates the lines each time it is run, so you only need to change the original snippet.
 * You can have multi-line snippet, and even nested chunks within those!
 * You can direct the output to another file.
 * You can use key-value collections defined in a config file instead.
 * You can apply conditional statements (repeat for all elements if)
 * There's an easy enumeration [0, 1, 2...] feature
 * There's intelligent capitalsation handling
 * Snippety can be run as a tool, or easily integrated into a python script, with a simple OOP model that lets you modify or extend the functionality however you please.

#####Example:

Multi-line directive with enumerator:
``` python
def constructor(record as DataRecord):
    #sn_s [name, 0*1] age height weight
    self.name = record[0]
    #sn_e
    self.age = record[1]                   #generated_code
    self.height = record[2]                #generated_code
    self.weight = record[3]                #generated_code
```

##Getting set up

Best to use from source for now as it's still in Beta. Basically download the files and play around with them


##Tests

Snippety uses [pytest](http://pytest.org/latest/) for it's unit tests, and there's a fair amount of test that pass, but could do with more edge-case testing.

##Contribution guidelines

  * Stick to [Python Style Guide](http://legacy.python.org/dev/peps/pep-0008/) (especially regarding spaces not tabs for indentation, or else copying code becomes a nightmare).
  * Make sure the code is compatible with Python 2.7.

##Questions:

Email me at andyhasit@gmail.com.
