# Brief

Build four small code samples in this directory. Each is a seam with its unit tests, a short description and three change requests.

## A seam

A seam is one Python function in which a language model's output passes through logic written in code. The function takes its input, asks the model for something, and returns a result after code has worked on the model's answer: checks, limits, formats.

- The model is an argument of the function: a callable that takes a prompt string and returns a string. Nothing in the code imports a model provider or opens a network connection.
- The model has real work to do in the function (it writes, picks, sorts, summarises or extracts something), and so does the code around it.
- A seam calls the model at one point only, and stands alone: no seam uses another.

## What to deliver

Four seams, in four different domains of your choosing. None about fitness or training.

One directory per seam, named after it:

```
<seam>/
  <seam>.py
  test_<seam>.py
  README.md
  requests/
    01.md
    02.md
    03.md
```

- **The code.** One file, short enough to read in a few minutes.
- **The tests.** They pass with `python -m unittest` run from the seam's directory, using a fake model and no network.
- **`README.md`.** A few sentences on what the function is for: who uses it, what goes in, what comes out.
- **The requests.** Three per seam, one file each.

## A request

A request asks for a change to the function's behaviour, written the way someone who uses the product would ask for it: the problem they see, an example of it, what they want instead.

- The person asking has never seen the code. The request says what is wrong, never how to fix it.
- Each request stands on its own, against the code as you deliver it. It is not a follow-up to another request, and it does not ask for something the function already does.
- One request is about an hour's work for a developer.

## Form

- Python 3, standard library only.
- Everything in English.
- Where this brief leaves something open, choose and carry on.
