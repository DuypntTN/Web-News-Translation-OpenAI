# Lab03- Web News Translation

## 1. Introduction

- This is a project to translate web news from English to Vietnamese. The project is implemented by using the [OpenAI Translate API](https://platform.openai.com/account/api-keys).

## 2. Installation

- Clone this repository:

```
git clone https://github.com/DuypntTN/Web-News-Translation-OpenAI.git
```

- Install the requirements:

```
pip install -r requirements.txt
```

or

```
conda install --file requirements.txt
```

## 3. Usage

- First, you need to create an account on [OpenAI](https://beta.openai.com/).
- Then, create an API key and paste it into the file `main.py` in line 62. `openai.api_key =[your API key]`
- Run the file `main.py`:

```
python main.py
```

- The link default web news is [VN Express](https://vnexpress.net/) or you can change it in line `129` in the file `main.py`.
- The translated news will be saved as `Translated.pdf`.

## 4. Result

Demo pdf
![](./Translated.pdf) 
---

If you have any questions, please contact me via email: [Duypnt23@gmail.com]
