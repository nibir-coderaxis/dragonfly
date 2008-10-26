#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it 
#   under the terms of the GNU Lesser General Public License as published 
#   by the Free Software Foundation, either version 3 of the License, or 
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but 
#   WITHOUT ANY WARRANTY; without even the implied warranty of 
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public 
#   License along with Dragonfly.  If not, see 
#   <http://www.gnu.org/licenses/>.
#

"""
    This file implements the Compound grammar element class for
    creating grammar element structures based on a simple text format.
"""


import string
import dragonfly.grammar.elements_basic as elements_
import dragonfly.parser as parser_
import dragonfly.log as log_


class _Stuff(parser_.Sequence):

    def __init__(self):
        self._single = None

    def initialize(self):
        self._single = _Single()
        self._single.initialize()
        repetition = parser_.Repetition(self._single)
        elements = (
            repetition,
            parser_.Repetition(
                parser_.Sequence((
                    parser_.String("|"),
                    repetition,
                    )),
                min=0),
            )
        parser_.Sequence.__init__(self, elements)

    def set_elements(self, identifiers):
        self._single.set_elements(identifiers)

    def set_actions(self, identifiers):
        self._single.set_actions(identifiers)

    def value(self, node):
        repetitions = [node.children[0].value()]
        for repetition in node.children[1].children:
            repetitions.append(repetition.children[1].value())

        alternatives = []
        for repetition in repetitions:
            if len(repetition) == 1:
                alternatives.append(repetition[0])
            else:
                element = elements_.Sequence(repetition)
                alternatives.append(element)

        if len(alternatives) == 1:
            return alternatives[0]
        else:
            return elements_.Alternative(alternatives)

stuff = _Stuff()



class _Single(parser_.Sequence):

    def __init__(self):
        pass

    def initialize(self):
        self._element_identifier = _ElementRef()
        self._action_identifier = _ActionRef()
        alternatives = parser_.Alternative((
            _Literal(),
            _Optional(),
            _Group(),
            self._element_identifier,
            ))
        elements = [
            parser_.Whitespace(optional=True),
            alternatives,
            parser_.Optional(
                parser_.Sequence((
                    parser_.Whitespace(optional=True),
                    self._action_identifier,
                    ))
                ),
            parser_.Whitespace(optional=True),
            ]
        parser_.Sequence.__init__(self, elements)

    def set_elements(self, identifiers):
        self._element_identifier.set_identifiers(identifiers)

    def set_actions(self, identifiers):
        self._action_identifier.set_identifiers(identifiers)

    def value(self, node):
        alternative = node.children[1]
        element = alternative.children[0].value()

        optional = node.children[2]
        if optional.children:
            action = optional.children[0].children[1].value()
            element.add_action(action)

        return element


class _ElementRef(parser_.Sequence):

    def __init__(self):
        characters = string.letters + string.digits + "_"
        name = parser_.CharacterSeries(characters)
        elements = (parser_.String("<"), name, parser_.String(">"))
        parser_.Sequence.__init__(self, elements)
        self._identifiers = None

    def set_identifiers(self, identifiers):
        self._identifiers = identifiers

    def value(self, node):
        name = node.children[1].value()
        try: return self._identifiers[name]
        except KeyError: raise


class _ActionRef(parser_.Sequence):

    def __init__(self):
        characters = string.letters + string.digits + "_"
        name = parser_.CharacterSeries(characters)
        elements = (parser_.String("{"), name, parser_.String("}"))
        parser_.Sequence.__init__(self, elements)
        self._identifiers = None

    def set_identifiers(self, identifiers):
        self._identifiers = identifiers

    def value(self, node):
        name = node.children[1].value()
        try: return self._identifiers[name]
        except KeyError: raise


class _Literal(parser_.Sequence):

    def __init__(self):
        characters = string.letters + string.digits + "_"
        word = parser_.CharacterSeries(characters)
        whitespace = parser_.Whitespace()
        elements = (
            word,
            parser_.Repetition(
                parser_.Sequence((whitespace, word)),
                min=0),
            )
        parser_.Sequence.__init__(self, elements)

    def value(self, node):
        return elements_.Literal(node.match())


class _Optional(parser_.Sequence):

    def __init__(self):
        elements = (parser_.String("["), stuff, parser_.String("]"))
        parser_.Sequence.__init__(self, elements)

    def value(self, node):
        child = node.children[1].value()
        return elements_.Optional(child)


class _Group(parser_.Sequence):

    def __init__(self):
        elements = (parser_.String("("), stuff, parser_.String(")"))
        parser_.Sequence.__init__(self, elements)

    def value(self, node):
        child = node.children[1].value()
        return child


stuff.initialize()


#---------------------------------------------------------------------------
# The Compound class.

class Compound(elements_.Alternative):

    _log = log_.get_log("compound.parse")
    _parser = parser_.Parser(stuff, _log)

    def __init__(self, spec, extras={}, actions={}, name=None, value=None, elements={}):
        self._spec = spec
        self._value = value

        # Convert extras argument from sequence to mapping.
        if isinstance(extras, (tuple, list)):
            mapping = {}
            for element in extras:
                if not isinstance(element, elements_.ElementBase):
                    self._log.error("Invalid extras item: %s" % element)
                    raise TypeError("Invalid extras item: %s" % element)
                if not element.name:
                    self._log.error("Extras item does not have a name: %s" % element)
                    raise TypeError("Extras item does not have a name: %s" % element)
                if element.name in mapping:
                    self._log.warning("Multiple extras items with the same name: %s" % element)
                mapping[element.name] = element
            extras = mapping
        elif not isinstance(extras, dict):
            self._log.error("Invalid extras argument: %s" % extras)
            raise TypeError("Invalid extras argument: %s" % extras)

        # Temporary transition code so that both "elements" and "extras"
        #  are supported as keyword arguments.
        if extras and elements:
            extras = dict(extras)
            extras.update(elements)
        elif elements:
            extras = elements

        # This solution is non-ideal as "stuff" is a global instance.
        stuff.set_elements(extras)
        stuff.set_actions(actions)

        element = self._parser.parse(spec)
        elements_.Alternative.__init__(self, (element,), name=name)

    def __str__(self):
        arguments = ["%r" % self._spec]
        if self.name: arguments.append("name=%r" % self.name)
        arguments = ", ".join(arguments)
        return "%s(%s)" % (self.__class__.__name__, arguments)

    def value(self, node):
        if self._value is None:
            elements_.Alternative.value(self, node)
        else:
            return self._value


#---------------------------------------------------------------------------
# The Choice class which maps multiple Compound instances to values.

class Choice(elements_.Alternative):

    def __init__(self, name, choices):

        # Argument type checking.
        assert isinstance(name, str)
        assert isinstance(choices, dict)
        for k, v in choices.iteritems():
            assert isinstance(k, str)

        # Construct children from the given choice keys and values.
        self._choices = choices
        children = []
        for k, v in choices.iteritems():
            child = Compound(spec=k, value=v)
            children.append(child)

        # Initialize super class.
        elements_.Alternative.__init__(self, children=children, name=name)