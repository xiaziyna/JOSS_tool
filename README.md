# JOSS_tool
```
pip3 install -r requirements.txt
python3 dockerfile_modifier.py
docker build -f Dockerfile.modified -t joss-review . --build-arg PACKAGE_REPO=https://github.com/rahil-makadia/grss/
docker run -it joss-review
```
