# ng-scope-docker
Utility for running NG-Scope using Docker

## Setup
The `install.sh` script will setup the environment.
It will pull the default docker image (`princetonpaws/ng-scope:22.04`) and copy the `ng-scope.sh` to `/usr/local/bin/ngscope-docker`.

## Run NG-Scope docker
A precompiled NG-Scope docker image can be used to run NG-Scope anywhere. Use **run.sh** to deploy it as follows: 
```bash
Usage: ./ng-scope.sh [Options...]
  -i, --image <Image name>        Name of the Docker image (e.g. j0lama/ng-scope:latest)
  -o, --out  <Output folder>      Output folder (will create if it does not exist)
  -f, --frag  <Seconds>           Enable log fragmentation with <Seconds> per log file
  -e, --earfcn "<EARFCN List>"    List of EARFCN (Use quotes)
  -t, --timeout <Time>            Stop NG-Scope after <Time> of runtime
  -h, --help                      Show help menu
Examples:
  ./ng-scope.sh --image j0lama/ng-scope:latest --earfcn "700"
  ./ng-scope.sh --image j0lama/ng-scope:latest --earfcn "700 300"
  ./ng-scope.sh --image j0lama/ng-scope:latest --frag 200 --earfcn "700 300"
  ./ng-scope.sh --image j0lama/ng-scope:latest --frag 200 --earfcn "700 300" --out enb_logs
  ./ng-scope.sh --image j0lama/ng-scope:latest --frag 200 --earfcn "700 300" --out enb_logs --timeout 1m
```

### Options
#### -i, --image \<Image name\> [default: ngscope]
NG-Scope will run in a docker container.
`<Image name>` must be a container based on the included Dockerfile.
The default is to use a local image named `ngscope`, but it can be any local container or one in a registry.
An up-to-date version will be maintained at j0lama/ng-scope:latest (subject to change).

#### -o, --out \<Output folder\> [default: .]
NG-Scope will produce DCI logs and SIB logs.
`<Output folder>` controls where those files are stored.
The directory will be mounted into the docker container.
If the directory does not exist, the docker mounting procedure will create it.
Typically, docker expects absolute paths, but a relative path can be supplied here as well.

#### -f, --frag \<Seconds\> [default: 0]
**WARNING: Experimental feature. Use at risk of captured data loss.**
It can be useful to fragment large DCI logs into file fragments.
NG-Scope can do this automatically.
Each file fragment will contain logs for the supplied number of seconds.
A value of 0 disables file fragmentation (default).

#### -e, --earfcn "\<EARFCN List\>" [required]
The EARFCN values to listen to.
A space separated list may be supplied.

#### -t, --timeout \<Time\> [default: 0]
Run NG-Scope for the desired amount of `<Time>`.
The supplied value can either be an integer, which will be interpreted as seconds.
`<Time>` can also be a number followed immediately by either `s`, `m`, or `h` to indicate seconds, minutes, or hours, repectively.
A value of 0 disables this behavior (default).

## Compile your own NG-Scope image
In case you want to modify NG-Scope and build your own docker image, just go into the docker/ directory and run the following:
```bash
./build.sh -n <Image name>
```
Use the flag **-s** to build the image from scratch (no cached).

For pushing the compiled image to [DockerHub](https://hub.docker.com) use:
```bash
sudo ./push.sh <Image name>
```
