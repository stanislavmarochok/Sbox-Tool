# SBox Tool
Diploma thesis project, multifunctional flexible scalable and easily modifiable SBox tool for generating and analyzing SBoxes with multiple generation and analyzation methods.

# Welcome message
Dear stranger,

I am Ing. Stanislav Marochok, and I am happy to welcome you in this repository. 

I am the author of the whole code, but I am not the author of the "Prescribed DDT" generation method implemented within this project. The author of the method is prof. Pavol Zajac and I have just implemented the algorithm.

If you have any questions, improvements, advices, or just want to talk, write me a mail [ssssstas30@gmail.com](mailto:ssssstas30@gmail.com) - this is my personal mail.

# The research description
Within the research our goal was to analyze existing methods of S-box contruction, and implement our own new method. We called the new method "Prescribed DDT". After the implementation we needed to somehow analyze the results. That is where we came to a decision that it is neccessary to implement a software which can do such job. We called the software "S-box Tool".

# S-box Tool
## Used technologies
We have used Python 3 to implement the software. In the beggining we used also SageMath library to do some calculations on S-boxes, but later we got rid of referencing the SageMath since we implemented all the neccessary functionality by ourselves.

## Arguments
"S-box tool" is a command line tool and it supports multiple arguments, which will be described in this paragraph.

After the name of an argument there will be a flag, which describes how the argument can be used:
[boolean] - the argument should not be followed by any additional values like "true", "1" or something like that, it is enough to just include the argument.

[int] - the argument must be followed by some integer.

[string] - the argument must be followed by some string.

### Options of methods of generation

Using argument from this group you can specify which method do you want to use to generate your S-boxes.

#### --random-generation [boolean]
S-boxes will be generated randomly. 

#### --prescribed-ddt [boolean]
S-boxes will be generated using our new method "Prescribed DDT", which gives better results than random generation, but in the same time is slower.

### Additional options to methods of generation

#### --generation-timeout [int]
Sometimes if you are using the "Prescribed DDT" method it can run too long, but if you specify argument "Generation timeout" you can define the maximum time (in seconds) you would like to wait for the results. This generation timeout applies to only 1 S-box out of the entire collection, for example if you specify that you need 10 S-boxes, and generation timeout is 5 seconds, the program will wait for 5 seconds will 1 S-box is generated, and after that it will wait again 5 seconds for the next S-box and so on.

### Additional options of S-boxes generation

#### --sboxes-count [int]
Specify this argument if you want more than one S-box to be generated.

#### --sboxes-size [int]
Specify this argument following by an integer, which will be taken as the power of 2, to define the maximum number which can be substituted by the S-boxes you want to generate. For example, "--sboxes-size 5" means that there will be generated S-boxes of size 2\*\*5 = 32, so the S-box is able to substitute integers in range [0, 32).

#### --prescribed-ddt-max-item [int]
Use this argument to specify the maximum item in the Differential Distribution Table that you want your newly generated S-boxes to have. This argument should be specified only if you are using the "Prescribed DDT" method of generation.

### S-box analyzing options
This group of arguments deal with the methods of analysis of S-boxes.

#### --analyze-ddt [boolean]
Use this argument to obtain detailed information about Differential Distribution Table properties from your newly generated S-boxes. That properties include such as "Maximum item in DDT", "Number of zero items in DDT", "Number of maximum items in DDT"

#### --analyze-bijection [boolean]
Analyze if newly generated S-boxes are bijectional or not.

### Options of export of the results

#### --dEC [boolean]
Disable export of generated SBoxes to CSV

### Options of output

#### --dC [boolean]
Disable printing logs on the screen (console output). Enabled by default.

#### --dF [boolean]
Disable printing logs to files. Enabled by default.

#### -oF [string]
Specify the folder where outputs will be saved.

to be continued...
