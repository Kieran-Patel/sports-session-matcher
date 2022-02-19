# sports-session-matcher

This exercise grew out of the need to match members of a tennis club together in predefined slots, depending on their individual availabilities. Members would be able to submit the slots they were available to play, and then a pairwise assignment would be made in order to but everyone in pairs.

To solve the matching puzzle, I converted the data from a tablular problem to a network (graphical) problem. In this network, nodes represent members, and then vertices represent a connections between two members... namely when they could play tennis at the same time. One then runs a maximal matching algorithm on this network to pair everyone up!

This project was further extended from simply an algorithm to a usable produce; using streamlit to build a simple web application. In this web application, users could enter their availablilities using a drop down feature, and then there is a separate 'solver' tab which applies the prior mentioned algoirthm.
