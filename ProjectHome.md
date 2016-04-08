# Dragonfly #

> <font color='red' size='large'><b>
<blockquote>The Dragonfly project has moved to GitHub.</blockquote>

<blockquote>The move from Google Code to GitHub is meant to encourage and facilitate collaboration, as offered by the Git version control system as opposed to Subversion. It also places the project on a vibrant platform of open-source development.</blockquote>

<blockquote>Dragonfly's new home is available on GitHub here:<br>
<a href='https://github.com/t4ngo/dragonfly'>https://github.com/t4ngo/dragonfly</a>
</b></font></blockquote>


---


Dragonfly is a speech recognition framework.  It is a Python
package which offers a high-level object model and allows its
users to easily write scripts, macros, and programs which use
speech recognition.

It currently supports the following speech recognition engines:
  * _Dragon NaturallySpeaking_ (DNS), a product of [Nuance](http://www.nuance.com/).
  * _Window Speech Recognition_ (WSR), as included in Microsoft Windows Vista.

A sister project is the [Dragonfly command-modules repository](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html).  This is a steadily growing collection of command-modules for controlling common programs and automating frequent desktop activities.  This is the place to look if you want to use speech recognition to increase your productivity and efficiency.  It also contains many examples, from simple to complex, of how to use the Dragonfly library.

## Documentation ##

The [library's documentation](http://packages.python.org/dragonfly/) is available for browsing online. Please refer to it for a more detailed overview of the Dragonfly library.


## Features ##

Dragonfly was written to make it very easy for Python macros,
scripts, and applications to interface with speech recognition
engines.  Its design allows speech commands and grammar objects
to be treated as first-class Python objects.  This allows easy
and intuitive definition of complex command grammars and greatly
simplifies processing recognition results.

  * _Language object model_ - The core of Dragonfly is based on a flexible object model for handling speech elements and command grammars.  This makes it easy to define complex language constructs, but also greatly simplifies retrieving the semantic values associated with a speech recognition.
  * _Support for multiple speech recognition engines_ - Dragonfly's modular nature lets it use different speech recognition engines at the back end, while still providing a single front end interface to its users.  This means that a program that uses Dragonfly can be run on any of the supported back end engines without any modification. Currently Dragonfly supports Dragon NaturallySpeaking and Windows Speech Recognition (included with Windows Vista).
  * _Built-in action framework_ - Dragonfly contains its own powerful framework for defining and executing actions.  It includes actions for text input and key-stroke simulation.


## Installation and Use ##

For detailed instructions on how to install and use Dragonfly, please refer to the [library's documentation](http://packages.python.org/dragonfly/).


## Rationale behind Dragonfly ##

Dragonfly offers a powerful and unified interface to developers
who want to use speech recognition in their software.  It is
used for both speech-enabling applications and for automating
computer activities.

In the field of scripting and automation, there are other
alternatives available that add speech-commands to increase
efficiency.  Dragonfly differs from them in that it is a
powerful development platform.  The open source alternatives
currently available for use with DNS are compared to Dragonfly
as follows:

  * _[Vocola](http://vocola.net/)_ - Vocola uses its own easy-to-use scripting language; however, this language is not complete - for example, it lacks simple conditional statements and the ability to call external python code from within it,  especially if there are dynamic elements in the utterance.

> On the other  hand, Dragonfly is a complete Python module that can use all the power  of the Python language (including other modules) dynamically.  Furthermore, Dragonfly allows for more intimate interaction with the  underlying recognition engine whereas Vocola relies entirely upon the  utilities exposed in Natlink. This results in greater stability,  especially with respect to arbitrary uttered text as a variable (i.e. anything in Vocola vs. Dictation() in Dragonfly).
  * _[Unimacro](http://qh.antenna.nl/unimacro/index.html)_ - Unimacro offers a set of macros for common activities, whereas Dragonfly is a platform on which macro-writers can easily build new commands.