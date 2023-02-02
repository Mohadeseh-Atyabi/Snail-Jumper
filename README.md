# Snail-Jumper

The aim of this project is to use the evolutionary algorithm for neural network learning in an environment where there is not enough data for training. One of these environments is the game, where something new is always happening, and it is impossible to produce educational data for education.

The game designed in this project can be implemented in two modes, manual and neural development, and its goal is to cross the obstacles on the way, which is done in manual mode with **space**. After running the game.py file, you will see the following image, by choosing the first option, the game will run in manual mode, and by selecting the second option, you can run it in the form of neural evolution.

<p align='center'>
  <img src="https://user-images.githubusercontent.com/72689599/216266581-7602ee55-4388-4f3f-9717-35aea4bf7b4f.png"/>
</p>

## Description of the problem
To run the game in the form of neural evolution, we need to design a neural network that receives important decision-making parameters as input and then produces the corresponding output. At the end, the generated output acts like pressing the space button.

Normally, to train a neural network, after determining the important parameters in choosing and building the architecture of the neural network, feedforward is done. Then a cost function should be defined so that in backpropagation, the weights and biases are updated in such a way that it leans towards the minimum. But in this project, there is no data for training and backpropagation, and that is why we use evolutionary algorithms.

In this way, a large number of players are produced in the game (300 in that project), each of which has a neural network initialized with normal random weights and zero biases. Now, each of the players will show a different performance according to the available initial values, by observing the obstacles. The more the player continues on his path, the more fitness he acquires. According to the principle of evolution, the players with better performance will be transferred to the next generations, and by considering crossover and mutation after several generations, it is expected that they will show better performance and travel further.

## Implementation
**Neural network implementation (nn.py file)**

- In the __init__ class, a Python list containing the number of neurons in each layer will be received. For example, using [3, 10, 2] means that 3 neurons will be used in the input layer, 10 neurons in the hidden layer and 2 neurons in the output layer. The weight matrix and biases will also be created according to the received inputs.

- An activity function such as sigmoid should be implemented in the activation function.

- In the forward function, the input of the neural network is received under the input of the function, and after performing feedforward, it returns the neurons of the last layer as output.

------

**Implementation of important parameters in decision-making and selection of neural network architecture (play.py)**

- In __init__ this architecture class used in the project should be selected. Note that there is no optimal answer to the problem and you should check different architectures by trial and error.

- In the think function, the input vector of the neural network is formed according to the inputs of the function, and then the output of the neural network is generated with the help of self.nn.forward. This function is constantly called during the game, and parameters must be selected in the decision-making process that affect the choice of jumping left and right. Now, according to the desired output, the self.change_gravity function will be called.

------

**Implementation of survivor selection (evolution.py file)**

If the game is run in neural evolution mode, 300 players will be created and all will be executed according to the described scenarios. After the end of a generation (loss of all 300 players), the neural evolution part starts. Each player's fitness increases with the distance he travels. As a result, all players must have a field called fitness.

In the next_population_selection function, a list of players along with num_players is received at the input. Survivors are then returned according to the number of num_players received. In this section, 4 modes are implemented:
- Sort players by fitness and select num_players first players
- Roulette wheel
- SUS
- Q-tournament

------

**Implementation of parent selection and generation of new generation organisms (evolution.py file)**

After selecting the survivors, now the parents should be selected so that the next generations (children) can be created with their help. In this section, the generate_new_population function must be implemented. Survivors are received as input to the function and an array of num_players of descendants is returned as output. In this function, for the first generation, a random array of players is returned, but for subsequent generations, the parents are selected first and then the children are generated.

Children should be different from their parents. Therefore, the clone_player function is called to generate children, so that a new version of the previous players with the same fitness and neural network parameters is obtained.

## Learning curve

For a better analysis of the evolution process, in each generation, calculate the highest, lowest, and average shiitges of the players and finally plot them. You can do this in the next_population_selection function. In the image below, you can see an example of the information obtained after 12 generations.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/72689599/216300630-3efbcf2b-28d7-4ae2-b0bc-dcdfff5d4099.png'/>
</p>
