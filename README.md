# ExamShuffle
Python code for shuffling LaTeX multiple choice exam questions and choices.

It checks main.tex file, finds the questions and choices. Shuffles questions, shuffles choices. Generates 4 random tests in LaTeX. Compile each one and you'll have 4 multiple choice exams with shuffled questions and answers.

# About main.tex LaTeX file

The file should be prepared using exam package. Question format is given at main.tex. Change question points according to your number of questions. For the example every question is 2.5 points. 
You should change the header of the LaTeX file. It shows my university info now. 

# About output exam_version files

The output file is set at showing anwers as bold and giving a correct answer sheet at the bottom. If you want to compile student version remove answers from document options and remove the answer sheet at the bottom.

