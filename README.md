This notebook walks through an engagement with Wellcome Collection's catalogue API for the purpose of working with the digitised text that Wellcome makes available.

It is an end to end example, starting with accessing, cleaning and working with catalogue metadata, going through the process of acquiring the raw text of books held by Wellcome Collection and ending with the very basics of topic modelling it. In a way, it walks through an initial digital engagement to get a rough feel for the possibilities of a dataset and a digital method.

The intent of the notebook is to help in getting started at working with this text. Nothing in here is necessarily the best &mdash; or even a correct &mdash; way to do a given thing, but it will show you **a** way that can get you started.

## Getting Started

In principle you should be able to deploy in different notebook environments.

The only method that I have actually tested is to run my own Jupyter server, for example:

```
git clone https://github.com/bogden1/wellcome_topics.git
cd wellcome_topics
mkvirtualenv wellcome_topics #Optional, but strongly recommended
pip install -r requirements.txt
jupyter lab --ServerApp.iopub_data_rate_limit 10000000
```

## Presentations

This repository also contains [presentations](presentations/README.md) delivered during the project.

## Acknowledgements

This notebook is an output from the [TNA/RLUK Professional Fellowship](https://www.rluk.ac.uk/) "Collaborative Experimentation: Research Software Prototyping for Co-Learning and Exploration in Cultural Heritage", which investigated RSE-led prototyping as a method of interdisciplinary collaboration and co-learning in digital cultural heritage.
