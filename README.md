My hello-world program for reinforment learning.

Developed as part of the obbligations for the module [Artificial Inteelligence](https://www.fri.uni-lj.si/en/course/63510), offered by University of Ljubljana.

How to run the program? Install the required dependencies (see requirements.txt), and then you may play minesweeper yourself by running `python3 minesweeper.py` (nope, I did not implement any logic to change the size of the grid or the number of mines... But it's really straightforward, so you can change that in the code yourself!).
Alternatively, you may train the agent: simply run `python3 main_loop.py`. Also in this case you may customize the agent (learning rate, DQN size, whether the position of the bombs should be visible or not, ...). 

I'll push a PDF with the project presentation, with all the details of the implementation, ASAP. Keep tight! :)

Some sources that helped me to get started with DQN (some pieces of code are taken from there):
* Some nice videos about the actual implementation of DQN with tensorflow - [link](https://www.youtube.com/watch?v=SMZfgeHFFcA)
* A great article that made me really understand what is going on- [link](https://rubenfiszel.github.io/posts/rl4j/2016-08-24-Reinforcement-Learning-and-DQN.html)
* An implementation of reinforcment learning for playing minesweeper; I could not replicate the experiment though- [link](https://github.com/jakejhansen/minesweeper_solver/blob/master/article.pdf)
* A nice series of articles that approaches RL step-by-step - [link](https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0)
