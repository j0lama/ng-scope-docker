# ng-scope-docker
Utility for running NG-Scope using Docker

# Run NG-Scope docker
A precompiled NG-Scope docker image can be used to run NG-Scope anywhere. Use **run.sh** to deploy it as follows: 
```bash
Usage: ./ng-scope.sh [Options...]
  -i, --image <Image name>        Name of the Docker image (e.g. j0lama/ng-scope:latest)
  -o, --out  <Output folder>      Name of the Docker image (e.g. j0lama/ng-scope:latest)
  -f, --frag                      Enable log fragmentation
  -e, --earfcn "<EARFCN List>"    List of EARFCN (Use quotes)
  -h, --help                      Show help menu
Examples:
  ./ng-scope.sh --image j0lama/ng-scope:latest --earfcn "700"
  ./ng-scope.sh --image j0lama/ng-scope:latest --earfcn "700 300"
  ./ng-scope.sh --image j0lama/ng-scope:latest --frag --earfcn "700 300"
  ./ng-scope.sh --image j0lama/ng-scope:latest --frag --earfcn "700 300" --out enb_logs
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
