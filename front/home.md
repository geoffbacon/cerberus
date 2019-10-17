<h1 align="center">Cerberus</h1>

<h3>What is Cerberus?</h3>

Cerberus is an app that reduces the annotation burden of linguists. It does this by making it easy for linguists to apply state-of-the-art natural language processing models to their data. Given some initial data, these models learn to perform linguistic annotation tasks themselves. They can then automatically perform those tasks on a much larger dataset, reducing the manual labour of a linguist. The models are not perfect and are designed to help bootstrap a linguistic project.

Cerberus currently supports the following tasks:

- **POS tagging**: Assigning a syntactic category to each word.
- **Translation**: Automatically translating from one language to another.
- **Classification**: Assigning a user-defined label to a word, sentence or paragraph.

Coming soon:

- **Spelling correction**: Correcting misspelt words.
- **Morphological analysis**: Assigning morphosyntactic features to each word.
- **Language modeling**: Generating grammatical sentences.


<h3>How to use Cerberus?</h3>

In brief, Cerberus can be used in four easy steps:

1. Choose a task from the drop down menu on the left.
2. Upload some initial data for Cerberus to learn from.
3. Click the "Train" button and wait until Cerberus has finished training the model.
4. Enter some text and Cerberus will annotate it for you.

Let's unpack that a little. To get started, choose a task from the drop down menu on the left. For each task, you'll need to train a model before you can use it. To do this, you'll need to give Cerberus some already annotated data so it can learn what to do. The data needs to be formatted in a particular way for Cerberus to read it. When you select a task from the drop down menu, Cerberus will tell you how the data needs to be formatted. Once you've given Cerberus the data, click the "Train" button. Cerberus will train the model and let you know once it's ready. If you close and re-open Cerberus, it will remember that you've already trained a model so you don't have to wait again. If you get more data, you can always re-train the model. Once you've trained a model, you can enter text in the app and Cerberus will annotate it for you. If you click the "Show metrics" button on the lefthand side, it will show you how long it took to train the model and how accurate it is. This helps you judge how much to trust Cerberus' annotations. 