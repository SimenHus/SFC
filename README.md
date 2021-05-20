# SFC
Program to generate simple SFC. The generated SFCs are intended to use together with simple photoediting software (i.e. paint) to create a complete SFC.

Both files need to be in the same directory. The program will generate a folder to store pictures in, default "Bilder", with the name of "SFC.png".

Edit perzonalization.py to change background color, file names and more.

# How to use

Action prompt:
Typing "show" will show the current image. This does not mean that the image is saved

Typing "save" will save the picture locally on your computer, under the filesname and directory specified in "personalization.py"

Typing "quit" will exit the program without saving

Typing "add sequence" (not caps-sensitive) will allow you to expand your SFC with a new sequential step.
Following this action you will be prompted with several questions to generate a step.

# Designing a sequential step

It is recommended to take a look at the example SFC and reading this paragraph before creating your own SFC.

When prompted...
...step name: The answer will be the text displayed inside the cell-rectangle. This answer is expected to be short

...initiation step: The answer will decide if the cell-rectangle will have an additional rectangle inside, to indicate that this is an initiation cell. Answer is expected to be "yes", "true" (not caps-sensitive) or anything else

...add action: Answering no will not add an action to this step. You will still be able to add a criteria.

..add action: Answering yes will prompt you follow-up questions to add spesifics to your action.

...action type: Standard action types for a sequential step (in example N, R, L). Answering L or D will   prompt you follow-up questions with time constant and time unit.
...action description: Describe what your action does. Answer may be short or long
...connected cells: Connected timers or counters are represented here. If you are not using any, give a   blank answer (just press enter).

...criteria: The answer will be displayed next to the line at the bottom of the sequential step, as an indication of the steps criteria needed to continue. Answerhas no expected size.
