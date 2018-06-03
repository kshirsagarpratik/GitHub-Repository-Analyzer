Please enter your own credentials for GitHub.

Install Python 3.6.x

On terminal/command prompt run
```
sudo pip3 install requests
```

Clone the repository on your system. Open the terminal from the repository directory and run -
```
python Iterate.py
```

The output of the analyzer will be in *output.txt*

The documentation can be found in *Homework2 Documentation.pdf* along with the source

# Homework 2

Your second homework assignment is to create a Git repository analyzer by automatically obtaining fixes to the source code that developers performed to address bug/issue reports for software applications. We are interested to determine patterns of code fixes in response to issues/bug reports as expressed in **patches**, which are modular code fragments that specify changes between versions of the code artifacts in a repo. These changes are often specified as instructions that are applied to the source code to implement the fix. Thus, instead of committing the code directly, a developer creates a patch and  applies/pushes it to the git repo, which takes instructions from the patch and applies it to the source code. Historically, the name patch originated from the Unix tool called *patch* that updated text files using instructions from a separate file called [a patch file](https://en.wikipedia.org/wiki/Patch_%28Unix%29). Git patches are essentially metadata files that describe how to apply changes to the source code of the previous version of the application to switch to the next consecutive version of the same application. For example, the following lines in a patch "- int a = 2" and "+ float b = 3" would mean that the declaration and initialization of the variable a in some Java file is replaced with the declaration and initalization of the variable b, hence + and - signs in the beginning of the lines. You can find more information in various sources (e.g., https://git-scm.com/docs/git-format-patch). Patches are effective because they make it easier for software developers to understand the changes to the source code at a high level and link them to specific issues/bug reports. The goal of this homework is to determine if there are "common" bugs based on the repeated patterns of patches that are applied to the source code to fix bugs.

In this homework, which you will build on the results of your previous homework, you will again use the Github Developer API to obtain open-source software projects with their metainformation. I recommend that you use **JGit** that has rich functionality and well-documented [JGit API calls](https://www.eclipse.org/jgit/), however, you can explore the toolkit/frameworks space on your own and find something that fits the task better. For each repo that you iterate through in Github (in reality, you will iterate through several repos), you will obtain patches for fixes as well as all metainformation related to these fixes, when available (e.g., the description of the issue/bug, dates and times and the content of discussions, developers ids). You will obtain existing patches or create new ones as needed by diffing consequtive versions and linking the patch to a specific commit and extracting and saving its metadata (e.g., the commit message). As a result, you will obtain a rich data set that can contain information about program entities (e.g., fields, their types, control structures, parameters of methods) that were modified as a result of fixes to specific bugs/issues.

To analyze how patches modify the source code, you can use the Application Programming Interface (API) of the tool called Understand (https://scitools.com/non-commercial-license/), a static code analysis tool that supports many programming languages and it is used by many Fortune 500 companies, an Eclipse parser, or some other open-source tools. If you haven't done so and if you choose Understand, you should apply for a non-commercial license immediately, install the tool, and investigate its IDE and its API libraries. You can complete this homework using a language of your choice, e.g., Java or Scala or Python or Go or Clojure or simply the utility curl when applicable (I prefer that you use Java for this assignment). You will use Maven or SBT or Gradle - your choice - for building the project. You can use the latest community version of *IntelliJ IDE* for this assignment.
