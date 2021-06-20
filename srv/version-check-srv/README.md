# Version Check Services
This services is built to automatically check a folder which assosiated in with git, and check whether in the same branch,
a new commit/version is deployed. This services used python as its programming language

## Compiling protoc file

Install the grpc_tools from requirements.txt
```python3
$ python3 -m venv venv
$ source venv/bin/activate  # Linux/macOS only
(venv) $ python -m pip install -r requirements.txt
```

How to compile your protoc file
```sh
cd /path/to/version-check-srv/proto
python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. ./version-check.proto
```

This generates several Python files from the .proto file. Here’s a breakdown:

- python -m grpc_tools.protoc runs the protobuf compiler, which will generate Python code from the protobuf code.
- -I ../protobufs tells the compiler where to find files that your protobuf code imports. You don’t actually use the import feature, but the -I flag is required nonetheless.
- --python_out=. --grpc_python_out=. tells the compiler where to output the Python files. As you’ll see shortly, it will generate two files, and you could put each in a separate directory with these options if you wanted to.
- ../protobufs/recommendations.proto is the path to the protobuf file, which will be used to generate the Python code.