# Insert and Search tools for mongoDB

A simple python demonstrative tool to insert and search data in [`MongoDB`](https://www.mongodb.com/)
using [`ODM MongoEngine`](https://docs.mongoengine.org/). Implemented caching with [`Redis`](https://redis.io/).

## **insert.py**

A simple script to insert authors and quotes data in JSON format into mongoDB.
Before using script, DB connection credentials should be specified in config.ini
All fields should be filled, every quote should have valid Author.
Contains documents` models which could be used externally. JSON files should be 
in the same folder with script. 
JSON format:

```text
Authors .json format:
[{  "fullname": "<name>",
    "born_date": "<date>",
    "born_location": "<location>",
    "description": "<description>"},]

Quotes .json format:
[{  "tags": [<tag1>,<tag2>],
    "author": "<author>",
    "quote": "<quote>"},]
```

## **search.py**
A simple CLI search engine to search Quotes by author name or tag(s).
Connections to mongoDB and redis should be established compulsory.
Input commands should be entered carefully, since input validation
is not implemented.

#### **Usage**

- **`name:<author>`**: Searches for quotes with given name (ex. name:Albert Einstein; name:alb)
- **`tag:<tag1>,<tag2>`**: Searches for quotes with a given tag(s). (ex. tag:live,value; tag:vi,va)


## **Setup**

Install the dependencies from **requirements.txt** and run one of the following commands:

```bash
- python insert.py
- pyrthon search.py
```

Enter your commands according to the usage instructions provided above.

For any issues or questions, please refer to the **[GitHub repository](https://github.com/NightSpring1)**.