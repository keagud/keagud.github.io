{% extends "base.html" %}
{% block title %}cake frosting sprinkle{% endblock %}
{% block date %}2023-04-06{% endblock %}
{% block content %}

    {{blockquote("Imagine you want to plant a brand new vegetable garden somewhere in your yard, and the first task is to stake out the plot. Odds are good that you'll be perfectly successful by just eyeballing it, hammering a wooden stake at one corner, and using it as a reference. Or you could be more formal and use a tape measure. The ultimate, guaranteed correct solution is to hire a team of surveyors to make sure the distances are exact and the sides perfectly parallel. But really, who would do that?", attribution="<i>programming in the twenty-first century</i>") }}

<p>
When I first started to write programs, I was very bad at it - unsuprising, since this is the default status for any particular human with regard to any particular activity. Programming is somewhat unique, however, in that you can get good grades in your middle school/high school/undergraduate computer science classes, and grow a reputation as a Knowledgable Computer Person whom others seek out for help during exam season, and still be quite bad at programming. Actually come to think of it, this may also apply to most other skills, but not as obviously. Much of this comes down to the two ways you learn to write programs in formal education:
    <ol>
    <li>
    Plot out every aspect of control flow and program logic beforehand. Chart out all the classes (and of course there will be classes, because OOP == real programming, dontcha know) in UML, link each layer of abstraction, generate a specification for the API each class must abide by. The actual act of writing the code should just be translating this logic into your IDE, more or less 1 to 1
    </li>
    <li>
    Don't plan at all other than a vague idea of what you want the program to do. Figure it out along the way.
    </li>
    </ol>

Method 2 is obviously not held up as desirable, but it's an emergant feature of the focus on method 1. We like to write code because it's fun! It's fun to puzzle out a problem, less so to consider whether Class A's relation to Class B is is-a or has-a before we're permitted to actually open the text editor. So the pendulum swings the other way in reaction, to no planning. The child isn't wrong to not want to eat cauliflower, but left to their own devices they'd just eat Oreos.
Both of these approaches are, for the majority of use cases, bad. Not all use cases certainly; if you're building a skyscraper, you do actually need to hire a team of surveyors. A one-off bash script can just be created stream-of-consciousness, as a hacky bodged Athene from the mind of Zeus. But I've found the majority of my projects fall in between these two extremes, where what's needed is the programming equivalent of a stake and a tape measure.
</p>

{% endblock content %}
