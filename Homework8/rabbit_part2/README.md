# Notification simulator 

A simple python demonstrative tools for queue usage in [`rabbitMQ `](https://redis.io/).
Creation fake contacts with [`Faker`](https://faker.readthedocs.io/). 
[`MongoDB`](https://www.mongodb.com/) and [`ODM MongoEngine`](https://docs.mongoengine.org/) are used as data storage/data manipulation.


#### **Usage**
Run scrips in a given order:
1) **`python seed.py`**: Creates a number of fake contacts data and inserts it into mongoDB.
2) **`python consumer_sms.py`**: Runs a stub server which waits a task from rabbitMQ SMS_queue and simulates sending notification to a contact.
3) **`python consumer_email.py`**:  Runs a stub server which waits a task from rabbitMQ Email_queue and simulates sending notification to a contact.
4) **`python producer.py`**: Creates tasks to notify contacts via email or SMS and puts it into related queue depending on which way to notify contact is more preferable.

After running all scrips, a simulation of SMS/E-mail sending could be seen in corresponding servers consoles.

## **Setup**

Install the dependencies from **requirements.txt**, edit rabbitMQ & mongoDB connections in config.ini.


For any issues or questions, please refer to the **[GitHub repository](https://github.com/NightSpring1)**.