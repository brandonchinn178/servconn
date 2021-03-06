ServConn
========

This repository defines classes that wrap connections to certain servers. The current classes defined are:
- DatabaseConnector: a class that wraps a SQL connection. Currently supports MySQL, SQLite, and PostgreSQL
- SocketConnector: a class that wraps a socket connection

Development
-----------

To develop, use the following to setup your environment

1. (optional) Setup a virtual environment with virtualenv
2. Install pip, brew
3. `brew install freetds` - the pymssql package needs this installation
4. `pip install -r requirements.txt` - installs all of the python SQL packages

Installing
----------

To install this package, either run `python setup.py install` from this project or call `pip install servconn`.

DatabaseConnector
-----------------

This class lets you query a SQL connection without dealing with connection or cursor objects.

### Usage

The DatabaseConnector can be used as a regular object or as a context manager.

```
from servconn import DatabaseConnector

db = DatabaseConnector.connect_mysql(host, username='test')
db.execute('INSERT INTO table VALUES (1,2)')

with DatabaseConnector.connect_mysql(host) as db:
    db.query('SELECT * FROM table')
```

### Class Methods
- `DatabaseConnector.__init__(connection, cursor)`: Creates a new DatabaseConnector object with the given connection and cursor.
- `DatabaseConnector.__del__()`: Closes the connection before this object is deleted.
- `DatabaseConnector.__enter__()`: Allows a DatabaseConnector to be used as a context manager
- `DatabaseConnector.__exit__()`: Closes the connection on exit as a context manager
- `DatabaseConnector.connect_mysql([host, username, password, port, database, **kwargs])`: Connects to a MySQL server. Connects to localhost by default on port 3306, optionally with the given username, password, and database. Additional parameters will be passed into the connect function
- `DatabaseConnector.connect_sqlite([database, **kwargs])`: Connects to the SQLite database file provided. Defaults to the database in RAM. Additional parameters will be passed into the connect function
- `DatabaseConnector.connect_postgres([host, username, password, port, database, **kwargs])`: Connects to a PostgreSQL server. Connects to the Unix socket by default on port 5432, optionally with the given username, password, and database. Additional parameters will be passed into the connect function
- `DatabaseConnector.connect_mssql([host, username, password, port, database, **kwargs])`: Connects to a Microsoft SQL server. Connects to localhost by default on port 1433, optionally with the given username, password, and database. Additional parameters will be passed into the connect function

### Instance Variables
- `DatabaseConnector.connection`: The MySQL Connection object
- `DatabaseConnector.cursor`: The MySQL Cursor object

### Instance Methods
- `query(query)`: Returns the result of running the given query on the connection
- `query_column(query)`: Returns the result of running the given query on the connection. Only returns the first column for every row, returning a tuple of Strings instead of a tuple of tuples.
- `execute(query)`: Executes the query and commits the transaction, but doesn't return anything. Useful for INSERT or DROP operations
- `compute(query)`: Returns the first row of the result of the running the query. Useful for SQL aggregate functions
- `close()`: Closes the connection from any further queries

SocketConnector
---------------

This class lets you send and receive JSON packets to the provided server.

### Usage

The SocketConnector is used as a regular Python object. Data can also be sent via the class method `send_to` for one-time connections.

```
from servconn import SocketConnector

socket = SocketConnector(host, port)
data = {
    'hello': 'world'
}
response = socket.send(data)
response = SocketConnector.send_to(host, port, data)
```

### Class Methods
- `SocketConnector.__init__(host, port[, bufsize=4096, ca_certs=None, delimiter='$'])`: Creates a new SocketConnector object that will connect to the given host and port. Various options may also be specified (see instance variables)
- `SocketConnector.send_to(host, port, data, **kwargs)`: Creates a SocketConnector object and sends the given data to the given host and port. Useful for one-time connections.

### Instance Variables
- `SocketConnector.host`: The host to connect to
- `SocketConnector.port`: The port to connect to
- `SocketConnector.bufsize`: The maximum amount of data allowed to be received at once through this socket (by default 4096)
- `SocketConnector.ca_certs`: The file path to an SSL certificate. Set to enable encrypted connections (by default None)
- `SocketConnector.delimiter`: The delimiter used for the `sendall` function. Messages will continue to be received until this delimiter is reached in the message string (by default '$')

### Instance Methods
- `send(data)`: Sends the provided data over the socket as a JSON-formatted string. Returns the response up to the bufsize.
- `sendall(data)`: Sends the provided data over the socket as a JSON-formatted string. Receives data until the delimiter is reached, then returns the response.
