# Introduction #

The Dragonfly library brings powerful tools to the fingertips of end users.  This page describes a very simple and bare-bones module for controlling notepad.  This module introduces various fundamental concepts of the Dragonfly library.  It can also easily be used as a module template for controlling other applications.

The notepad module described here is comparable to traditional Natlink macros.  It can be loaded and used by the normal Natlink system.  In general, this means that this notepad module should be placed in the `My Documents\Natlink` folder.  The main difference between this module and traditional Natlink macros is the object model for defining grammars and processing recognitions.


# Source code #

The source code listed below is also included in the Dragonfly repository [here](http://code.google.com/p/dragonfly/source/browse/trunk/dragonfly/examples/notepad_example.py).

```
from dragonfly.grammar.grammar     import Grammar
from dragonfly.grammar.context     import AppContext
from dragonfly.grammar.mappingrule import MappingRule
from dragonfly.grammar.elements    import Dictation
from dragonfly.actions.actions     import Key, Text


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

grammar_context = AppContext(executable="notepad")
grammar = Grammar("notepad_example", context=grammar_context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

example_rule = MappingRule(
    name="example",                    # The name of the rule.
    mapping={                          # The mapping dict: spec -> action.
             "save [file]":            Key("c-s"),
             "save [file] as":         Key("a-f, a"),
             "save [file] as <text>":  Key("a-f, a/20") + Text("%(text)s"),
             "find <text>":            Key("c-f/20") + Text("%(text)s\n"),
            },
    extras=[                           # Special elements in the specs of the mapping.
            Dictation("text"),
           ],
    )

# Add the action rule to the grammar instance.
grammar.add_rule(example_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
```


# Discussion #

The notepad module presented above shows how to use several of Dragonfly's basic building blocks.