# **pyBrain**

Brief description
====
This project is an example of Artificial Intelligence implementation.
It is based on personal studies about psicology and personal inspiration.
I've not knowledge about the actually proven AI technologies.

The basic idea: 
Considering a set of binary inputs, and a set of binary outputs, we have to create a data structure that for each combination on inputs can 
relate all the outputs combinations.

This data structure must allow to be *modeled* in order to provide, for a given input, the best outputs combination.

![Alt text](https://raw.githubusercontent.com/dddomodossola/pyBrain/master/res/basic_network.png "Basic network")

The information are represented by the connections in the "modelable substratus". These connections will be strengthened or weakened by some kind 
of law that, considering the output effect, teaches the network.
At this point, there is about nothing of *intelligence*.

Now, suppose you want to get an output that have to be related to the previous *events* (for *event* it is intended the combination of input/output),
how to do this with the said data structure? We can provide back the previous inputs outputs as new inputs.

![Alt text](https://raw.githubusercontent.com/dddomodossola/pyBrain/master/res/memory_network.png "Memory network")


feedback function

attention concept
