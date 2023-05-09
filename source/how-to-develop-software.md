% How to Develop Software
% Ulf Westermann
% 2023-05-08, v0.0.1


# Introduction

This is an opinionated text on software engineering, as most other texts on this subject. Contrary to what many people believe, there is little scientific evidence on what works and what not [^leprechauns]. Despite the 'click-baity' title, I believe that nobody, including me, knows what's the best way to develop software. There are as many different perspectives as there are developers, and most of them are valid. Surely, there is a great diversity in how people think and like to work. Software engineering practices should respect and appreciate this. However, what follows is a summary on theoretical backgrounds, best practices and personal experience, that somehow have proven to be beneficial to me. For a more conventional, traditional and complete view, see [^swebok].

There are different types of software (e.g. embedded or web) and problem domains (e.g. aerospace or games) with different tools, practices and cultures. It is often confusing to talk about software without further specifying it. If not mentioned otherwise, this text refers to software engineering in general.

Compared to the early days of computing, where even the simplest things needed to be discovered or invented, we nowadays can profit from the knowledge that is already available. It is important to tap into this huge body of knowledge, instead of reinventing the wheel every time.

A lot of knowledge has been distilled into ready to use software in the form of libraries. Modern programming languages often come with a standard library that already contains all basic algorithms and data structures ("batteries included"). That means that software engineering has changed from mainly inventing fundamental stuff to reusing it. Writing glue code that connects existing blocks has become the prevalent activity for developers. That does not mean that knowledge about basics is not necessary. In order to use them profitably, one needs to have knowledge of the internals to make trade-offs an informed decision.

For people without computer science background, the next section gives an orientation about which topics could be worth of investing some time.


# What to Know

- Basic theoretical computer science
  - Algorithms and data structures
  - Computability, complexity and information theory
  - Programming languages
  - Computer architecture and operating systems
  - Math
- Practical skills
  - Usage of operating systems (e.g. shell)
  - Usage of basic software engineering tools (e.g. text editor, compiler, build system, version control)
  - Touch typing (for a high bandwidth interface to the machine)


# A More Philosophical Perspective

Software engineering, is a socioeconomic endeavor, and as such, it falls into the category of complex [^complex] (or wicked [^wicked]) problems. For a useful categorization, see [^cynefin].

The class of complex problems lies between the class of simple and even complicated problems on one side of the spectrum, and problems that are accessible by statistical methods on the other side. Simple/complicated problems can be described by linear systems with relatively few "moving parts". They can be understood by humans. On the other hand, systems with many parts and uniform structure that behave predictable as a whole, such as gases, can be described statistically without knowing what every particle in the gas is up to.

Complex systems are in the wicked middle, they are to complex to be understood fully by humans (in the sense that the outcome of parameter changes is not completely predictable) and they have to much structure to be accessible by statistical methods. Complex systems are non-linear (in software development, humans are the non-linear element), and may also be chaotic, which means that minimal changes in start conditions (the infamous butterfly effect [^butterfly]) can have huge effects in outcome. Think about a cocktail party as an analogy for software development: Even when trying to exactly reproduce a previous party (same people, music, drinks), the outcome may be completely different. Do not draw the false conclusion that you should have drinks while developing software...

The reductionistic approach [^reductionism], which is prevalent in science, also does not help in the understanding of complex problems. This approach tries to explain phenomena based on their smallest basic elements. Unfortunately, one property of complex systems is that the whole is more than the sum of its elements. Those systems exhibit emergent behavior, which is not explainable by looking at the parts in isolation. For example, a human is more than a heap of atoms and biochemical reactions on microscopic level. The informaton how everything is put together and interacts (the process) constitutes the whole.

Given that the previous assessments are true, any analogy of the software development process with mechanistic systems (which belong to the class of simple/complicated) must be wrong. Trying to focus on isolated steps, trying to formalize the process, or trying to reduce it to simple numbers (performance indicators or metrics), does not respect the complex nature of the problem.


# Humans
motivation


# Teams

self forming, no hierachy. groups made working by evolution since humans exist.


# What is Software

bridge


# What is Software Enginneering


# Design & Practices

Architecture = design

 software qualities -> software structure that supports qualities

conways law! molly rocket



# TL;DR

Key takeaways:

1. Learn about the history of the field, read classic papers and books.
2. Be skeptical about alleged truths. Most scientific results are not as solid as believed.
3. Learn theoretical (e.g. computer science) and practical (e.g. touch typing) basics.


# See Also


# References

[^leprechauns]: [The Leprechauns of Software Engineering](https://leanpub.com/leprechauns). Laurent Bossavit. 2017.
[^complex]: [Complex System](https://en.wikipedia.org/wiki/Complex_system)
[^wicked]: [Wicked Problem](https://en.wikipedia.org/wiki/Wicked_problem)
[^butterfly]: [Butterfly Effect](https://en.wikipedia.org/wiki/Butterfly_effect)
[^swebok]: [Software Engineering Body of Knowledge](https://en.wikipedia.org/wiki/Software_Engineering_Body_of_Knowledge)
[^cynefin]: [Cynefin framework](https://en.wikipedia.org/wiki/Cynefin_framework)
[^reductionism]: [](https://en.wikipedia.org/wiki/Reductionism)

---




# What is Software Engineering

NATO conference bla bla. Hidden agenda to get funds for an instituion....


## Detour - What is Software and What is Engineering

Bridge vs Compiler
Development in most cases for new problems -> exploration, because if not new, standard software can be used -> MS Excel vs cp bridge to new river


# What's Important

(in this order)

1. People
2. Methodology & Design
3. Tools (Language, SCM, Requirements, Issue Tracking)


# People

The single most important factor for successful software projects is people.

The simple solutions seems to be to just hire the best people available, by baiting them with a lot of money. There are two problems with this approach:

(1) What are the "best" people? Diplomas and certificates have often shown to be bad indicators.

(2) A lot of money does not necessarily attract the best people, maybe just the greediest ones. Psychology has shown that beyond a certain amount of money, one does not get proportionally more motivated. Economists would speak of diminishing returns (of invested salary). Interestingly, paying less than what is considered a fair salary, really destroys motivation.


## People - So, What Does Motivate Us?

Psychology knows two kinds of motivation: Intrinsic and extrinsic.

Extrinsic motivation comes from external influences, as salary, awards or punishment. In an environment with external motivation, actions become directed at these external factors, not necessarily at the actual work goal. For instance, getting a better job title (for prestige) or salary becomes more important than doing the actual work. This not only can destroy intrinsic motivation, but work quality can be poor and motivation wanes quickly if the external influence is removed.

Intrinsic motivation...

Myth of 10 x programmer

Teamwork

Expertise, deliberate practice

Mindset

Self-determination (wie hies das buch?)

## Detour - Hierachy and Bureocracy

## People - Back to Point (1): How to Select Them?

In short, don't select people, let people select you.

Believing that one can select the "right" people is hybris. Who selected the selector to be competent?

Provide an environment that fosters motivation, health and sustainability. It will attract people.


# Methodology & Design

Teams

## Design

Make it easy to change + other non-change related -ilities.

Good desing becomes what psychology calls (affordance)[https://en.wikipedia.org/wiki/Affordance], once good intutions are built.


# Tools

tools


## Detour - Self Determination Theory


## Detour - Intuitions

Design by intuition. Build intuitions by deliberate learning.


## Detour - How do we learn (Paul Ralph)

While working on a project, we learn new things


## Detour - Feedback

## Detour - Lean Development

## Detour - Null Hypothesis

## Detour - Agile Manifesto

## Detour - What is Software Engineering

swebok

## Detour - Reduction of a Complex World Into a Number

Why metrics are bad


# Annex A - Reading/Listening Recommendations

Reinventing Organizations
Thinking Fast and Slow
The Pragmatic Programmer
Lean Development
The Practice of Programming
Gigerenzer (2007). Gut Feelings: The Intelligence of the Unconscious
Das Buch über self-determination theory


# Annex B


* We are a small team. There is no one who could control/check the work of others. Normally the creator is responsible for fixing problems that occur later. If the creator is no longer available, someone else will have to deal with the problems. So please work responsible.

* Try to work and learn independent and self-responsible, while being a team player and helpful if others could benefit from your assistance. Take care of issues you find, probably no one else will do. Active communication with colleagues and customers is very appreciated.

* Don't be dogmatic about tools (or something else), it can be used whatever is the best fit for the problem, but consider that there is existing knowledge about certain tools. If other tools are used, there is a learning curve and a good chance that software using other tools will not be maintained, abandoned or rewritten. Commonly used tools are:
    - Linux
    - Shell scripts
    - ISO C99 and newer (GNU make, ClangFormat, CppCheck, CBMC)
    - Python 3 (PyCharm, Pylint, mypy)
    - Fossil SCM or Git VCS
    - Pandoc (Markdown, PlantUML)
    - Source Code IDE/Editor of choice

* Prefer free and libre software. Paying license fee itself is a smaller problem compared to the hassle with license management, license servers and the bureaucratic overhead of renewing licenses. Most of the time, there is also good and instant community support for free and libre software and, at least for popular projects, extensive online documentation. In case of problems or for security reasons, open sourced projects can be examined to understand how they work and, because you have a copy of the code, they will always be available.

* Prefer simple text over binary or unreadable text formats (*cough*..xml..*cough*) and a shell interpreter in a terminal over GUIs. Text is readable and modifiable by humans and machines without special tools, it can be put under version control, diffed, patched, searched and, if size plays a role, compressed. Shell command line programs in a terminal can process text, can be scripted, automated and combined. While this gives great flexibility, sometimes a GUI (e.g. website) can be more appropriate when information is better visualized graphically or when users have a less technical background. See also: Unix Philosophy.

* Scope of Work: Source code is only a small part of the work. Scope/feature negotiation, coordination with others, integration, documentation, test and user support is similarly important. Work on software is not done until all of these are finished.

* Use version control for software source code and other textual artefacts.

* Coding Style: Adapt to what is already there, don't mix different styles. If there are widely used styles (e.g. PEP 8 for Python), use them. Enforce formatting and style with tools before checking into version control to avoid code churn (and therefore unnecessary changes in the version control history).

* In general, always try to take the perspective of others who are new to the project (or you in one year). Try to reduce the number of WTF!s (principle of least astonishment) when someone deals with your project. Follow canonical conventions, use defaults and use idiomatic language constructs.

* Make sure that source code and documentation can be found. Put it where you would look for it. Minimum documentation recommendation (if no other documentation requirements apply): Write at least one document, preferably in Pandoc Markdown. The following should be covered:
    - Introduction (overview, context and scope)
    - Requirements (what is needed? to be agreed with customer)
    - Design (this is for developers: main architectural decisions explained/justified, internal structure, conventions, how to extend/build/test/deploy project)
    - Manual (this is for users: how to use the integrated software product)

* Language for documentation and source code is always English.

* Design and Code: Don't stop with the first code iteration that works, that's were the work begins. Refine your code until it is perfect. Test it. Take special care of error and edge cases. Make sure the software has internal and external conceptional integrity and allows forming a mental model. Value clarity, consistency and generality. Care about useful abstractions. Apply divide and conquer strategy. Separate concerns (SoC) and ensure that knowledge has only one authorative repsentation (DRY). Minimize dependencies, favour loose coupling and locality. Avoid decisions that make change and extension difficult. Keep it as simple (KISS) as possible, but not simpler. Be aware that simple != easy. Reduce accidental complexity, it is the root of all evil (see: No Silver Bullet). The best code is no code. If you've never developed larger systems or maintained software, these points may not seem to be obviously important at first. Book recommendations: The Practice of Programming by Kernighan/Pike and The Pragmatic Programmer by Thomas/Hunt.

* But, maybe the hardest problem in software (besides naming) is to write the right software, i.e. a software that fulfils all needs. Key is to uncover and understand the needs, aka requirements. That can't be done without knowledge about the problem domain!

* How to Think about Code: Source code is a design document in the same sense as schematics are the design of an electronic circuit or an architectural drawing is the design of a bridge. The big advantage of code is that building the product (i.e. an executable binary) is cheap and fast compared to building a bridge. This should have impact on the software development process...! True, not all design decisions and trade-offs are obvious from the source code. That's the reason for having a design/architecture document.

* Software Development Process and Methodology: Adapt to the circumstances. Avoid overhead and waste, be pragmatic. Try to think thinks through to the end and in its bigger context. A good strategy is to make a small upfront design and then start prototyping. In the design, take into consideration which software qualities are important. Use the prototypes to evaluate your assumptions about the design and implementation. Then refine your prototyped code and design until it has release status. Involve static analysis tools, tests, colleagues, users/other stakeholders (in that order) to give feedback. It is often helpful to start with modules whose feature set is fixed (because they represent existing external interfaces or hardware). Those fix points help by limiting the design space. Use 'tracer bullets' to evaluate complete parts of your design. Don't use too many low level unit tests in the prototyping phase, they are an impediment to code change/evolution.

* General Suggestions: Try to improve your writing skills (take this document as an example (of how not to do it)). Learn touch typing. Learn to utilize a good, productive developer's cross-platform text editor (e.g. Vim, Neovim, Emacs, VSCodium). You may think that you have no time to learn that, but in reality, you don't have time not to learn it.



