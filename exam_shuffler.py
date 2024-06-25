import re
import random

def process_latex(file_content):
    """Extracts and shuffles questions from a LaTeX exam."""
    # Regular expressions to extract questions and choices
    question_pattern = re.compile(r"\\question\[.*?\](.*?)(?=\\begin{choices})", re.DOTALL)
    choices_pattern = re.compile(r"\\begin{choices}(.*?)\\end{choices}", re.DOTALL)

    # Extract questions and their choices
    questions = question_pattern.findall(file_content)
    choices_blocks = choices_pattern.findall(file_content)

    # Process choices
    choices = []
    for choices_block in choices_blocks:
        individual_choices = re.findall(r"\\(choice|CorrectChoice)\s+(.*?)\n", choices_block, re.DOTALL)
        choices.append(individual_choices)

    # Shuffle questions and choices
    combined = list(zip(questions, choices))
    random.shuffle(combined)
    shuffled_questions, shuffled_choices = zip(*combined)

    return shuffled_questions, shuffled_choices

def generate_latex_output(shuffled_questions, shuffled_choices, version_num):
    """Creates LaTeX output with shuffled questions and an answer sheet."""
    output = r"""
\documentclass[11pt, a4page, answers]{exam}
\input{exam_header} % Include the header file (exam_header.tex)

\begin{document}
\title{Engineering Materials Midterm 2024}
% These commands set up the running header on the top of the exam pages
\pagestyle{head}
\firstpageheader{}{}{}
\runningheader{\class}{\examnum\ - Page \thepage\ / \numpages}{\examdate}
\runningheadrule
\begin{table}[ht]
\centering
\begin{tabular}{c}
\textbf{T.C.}                             \\
\textbf{Eskişehir Osmangazi Üniversitesi} \\
\textbf{Mühendsilik Mimarlık Fakültesi }                            
\end{tabular}
\end{table}
\textbf{\class} \hspace{0.5in} \textbf{\term} \hspace{0.5in} \textbf{\examnum} \hspace{0.5in} \textbf{\timelimit} \hfill \textbf{\examdate}
\begin{flushright}
\begin{tabular}{p{1in} c r r}
\textbf{Name:} & \makebox[2in]{\hrulefill} & \textbf{Number:} & \makebox[2in]{\hrulefill}\\
\textbf{Signature} &  & & \\
\\ 
\end{tabular}\\
\end{flushright}
\rule[1ex]{\textwidth}{.1pt}

\textbf{Exam rules}

\begin{itemize}
    \item Closed Notes
    \item Calculators are allowed
    \item Any exchange of information and materials is strictly prohibited
\end{itemize}

\begin{figure}[h]
    \includegraphics[width=0.8\linewidth]{Fig9-24.png}
    \caption{The iron–iron carbide phase diagram.}
    \label{fig:1}
\end{figure}

\newpage
\maketitle
\begin{questions}
"""

    for i, (question, choice_list) in enumerate(zip(shuffled_questions, shuffled_choices)):
        output += f"\\question[{2.5}] {question}\n\\begin{{choices}}\n"
        for choice_type, choice_text in choice_list:
            output += f"  \\{choice_type} {choice_text}\n"
        output += "\\end{choices}\n"

    output += r"\end{questions} \newpage \textbf{Answer Sheet (Version " + str(version_num) + ")}"
    choice_map = ["A", "B", "C", "D"]
    for i, (_, choice_list) in enumerate(zip(shuffled_questions, shuffled_choices)):
        correct_answer_index = next((index for index, (c, _) in enumerate(choice_list) if c == "CorrectChoice"), None)
        if correct_answer_index is not None:
            output += f"\n{i + 1}. {choice_map[correct_answer_index]}"
        else:
            output += f"\n{i + 1}. No correct answer found"

    output += r"""
\end{document}
"""
    return output

# Load the LaTeX file content (replace 'your_latex_file.tex' with your file path)
try:
    with open('main.tex', 'r') as f:
        latex_content = f.read()
except IOError as e:
    print(f"Error reading file: {e}")
    latex_content = ""

# Split header content into separate file for easier reusability
header_content = latex_content[:latex_content.find(r'\begin{document}')]
try:
    with open("exam_header.tex", "w") as header_file:
        header_file.write(header_content)
except IOError as e:
    print(f"Error writing header file: {e}")

# Generate 4 versions
for version in range(1, 5):
    shuffled_questions, shuffled_choices = process_latex(latex_content)
    output_latex = generate_latex_output(shuffled_questions, shuffled_choices, version)

    try:
        with open(f'exam_version_{version}.tex', 'w') as out_file:
            out_file.write(output_latex)
    except IOError as e:
        print(f"Error writing output file: {e}")
