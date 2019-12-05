Contributions: Simrat Bains
-------------------------

    Group work isn't always my go-to option when it comes to big projects. My experiences have been fairly
    terrible when it comes to collaborating with others: be it taking responsibility for ones work or overall 
    morale of the group, something has always gotten in the way of a succesful teamwork. However, this project
    by far one of the best experiences Iv'e ever had. Very quickly we established our roles and responsibilities
    which made divying up the workload much simpler.

    The team was very familiar with python, we decided to work with pygame; this increased our efficiency and 
    we were able to deliver on our short term goals with ease. Since I have a background with Adobe Photoshop 
    and Illustrator, I was able to play to my strengths and was responsible of the main menu, color selection 
    screen, and graphics for the game.

    Menu()
    -----------------
    The *Menu()* class is a sublcass of *object*. The main menu has an event listener which is waiting for a
    keypress: specifically the key f or *K_f* as pygame understands it as. If the key is pressed, the variable
    *self.run* becomes False and the menu terminates. 

    Character_Select()
    -----------------
    After *Menu()* ends, *Character_Select()* is the next window that pops up. In this part of the menu, there 
    are nine rectangles, each representing a color that the player can play as. All the colors key and value pairs
    are stored in a python dictionary called *colors*. 

    .. code:: python 

       colors = { 0: (255,6,80), 1: (218,165,32), 2: (107,142,35), 3: (64,224,208), 4: (153,255,204), 5: (111,90,255), 
               6: (169,169,169), 7: (240,230,140), 8: (255,64,255) }

    
