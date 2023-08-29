# ng-scope-docker
Utility for running NG-Scope using Docker

# Run NG-Scope docker
A precompiled NG-Scope docker image can be used to run NG-Scope anywhere. Use *j0lama/ng-scope:latest* and specify the EARFCN value: 
```bash
./run.sh j0lama/ng-scope:latest <EARFCN List>
```

# Compile your own NG-Scope image
In case you want to modify NG-Scope and build your own docker image, just go into the docker/ directory and run the following:
```bash
./build.sh -n <Image name>
```
Use the flag **-s** to build the image from scratch (no cached).

For pushing the compiled image to [DockerHub](https://hub.docker.com) use:
```bash
sudo ./push.sh <Image name>
```
