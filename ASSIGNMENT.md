# 3.11 Assignment: Maze Search Implementation

## Description
## Module 3
 3.11 Assignment: Maze Search Implementation

### Overview

This assignment is a chance for you to practice using the algorithms described in this module. You will be given the description of the format your code needs to be able to process and several example mazes. You need to program three different algorithms from this module to solve the mazes. 

###  Instructions

#### Assignment brief

In this assignment, you will use three algorithms from this module to solve mazes. Take note of the following:

- You must use **at least one blind search algorithm** and **one heuristic search algorithm**. Your **third choice can be either.** 
- Your code must be written in Python. You will submit all of your code on Gradescope. 
- When you submit all code, include a README file explaining how to use your code and a report. 
- Your code must include a file that serves as an interface to your solving algorithms. 

This file must be named **maze_solvers.py.**
- The file must include the function names: **maze_solver_one**, **maze_solver_two** and **maze_solver_three**. Each of those functions must require one parameter, the maze to solve (see maze format description later in the assignment brief), and it must return the solution to the maze. 

```
solution = maze_solver_one(maze)

solution = maze_solver_two(maze)

solution = maze_solver_three(maze)
```

The rest of your code can include other files and functions named however you wish. The three maze solver functions should call those functions to solve the maze it was given as input. 

#### Maze 

The maze will be stored as a text file. 

- The first line of the file contains the dimensions of the maze. The first number is the width, and the second number is the height.

For example, 10 6 is a maze that is 10 units wide and 6 units tall. 

- The maze is defined using text characters. 

S is the starting location
- E is the exit location
- X is a barrier/wall
- Your solution will include an extra character: * is the path taken (learn more in the examples below)

Select the following heading to learn more about the maze format.

#### Maze format

A maze might look like this:

```
10 6

XXXXXXXXXX

X        S

X XXXXXX X

X X    XXX

X   XX   E

XXXXXXXXXX
```

- Your solution will include an extra character: * is the path taken

The solution to the above example is:

```
10 6

XXXXXXXXXX

X********S

X*XXXXXX X

X*X****XXX

X***XX***E

XXXXXXXXXX
```

Another example:

```
8 8

XXXXXXXX

X      X

X  X   X

E  X   X

X  X   S

X  XX  X

X      X

XXXXXXXX
```

This maze has multiple solutions. Any solution is acceptable.

Two possible solutions:

```
8 8

XXXXXXXX

X ***  X

X *X*  X

E**X***X

X  X  *S

X  XX  X

X      X

XXXXXXXX
```

```
8 8

XXXXXXXX

X      X

X  X   X

E* X   X

X* X  *S

X* XX *X

X******X

XXXXXXXX
```

 

- Your code should be able to handle a maze of up to 1,000 x 1,000.
- You can use the following example mazes to try out your algorithms: [link placeholder]
- When you upload your code to Gradescope, your code will be tested on additional examples. You will be informed if your algorithms are unable to find a solution to the test mazes. You can upload revisions until your code can solve each test maze. 
- The following maze should be used for your report: [link placeholder]

#### Report

The report for this module requires you to compare the performance of your different algorithms on the given maze. Your report should include the following:

-  An introduction to search algorithms
- The specific search algorithms you are using
- The heuristic functions those algorithms are using (for the heuristic search algorithms) 
- Compare the performance of your chosen algorithms on the maze provided.
- Comment on the optimality of the path to the goal, the time taken and the space required. 
- Describe changes to the maze that would affect the performance of your algorithms. 
- Identify changes that would make each of your algorithms perform the best (either optimality of path or time to find the goal). 
- Conclude with a real-life situation you have encountered where one of your search algorithms could be applied.

#### Submission information

Review the rubric to ensure that your submission meets the criteria for achievement. Before you begin, take note of the following:

- **Attempts**: Any number of times prior to the deadline.
- **Report length**: 5+ pages, including title page and references. Code is not counted toward the length. 
- **Submission**: Report and code. Code must include maze_solvers.py. Turn in on Gradescope. 
- **Plagiarism**: Your code and your report are expected to be your own. This is an individual assignment. Copying the code structure from another student while replacing variable and function names still counts as copying. AI may be used to help revise and debug your code. Ensure that your use of AI is not replacing your own learning or thinking. A good understanding of these algorithms and how to use them is necessary for your long-term success. 

Select Next to explore the module summary.

Icon Progress Bar (browser only)

## Due Date
2026-04-04T03:59:59Z

## Setup
```bash
pip install -r requirements.txt
```

## Running Tests
```bash
pytest
```

## Submission
Complete the implementation in `main.py` and ensure all tests pass.
