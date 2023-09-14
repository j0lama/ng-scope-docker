#!/bin/bash

Help() {
    echo "Usage: $0 [Options...]" >&2
    echo "  -i, --image <Image name>        Name of the Docker image (e.g. j0lama/ng-scope:latest)"
    echo "  -o, --out  <Output folder>      Output folder (will create if it does not exist)"
    echo "  -f, --frag  <Seconds>           Enable log fragmentation with <seconds> per log file"
    echo "  -e, --earfcn \"<EARFCN List>\"    List of EARFCN (Use quotes)"
    echo "  -t, --timeout <Seconds>         Stop NG-Scope after <seconds> of runtime"
    echo "  -h, --help                      Show help menu"
    echo "Examples:"
    echo "  $0 --image j0lama/ng-scope:latest --earfcn \"700\""
    echo "  $0 --image j0lama/ng-scope:latest --earfcn \"700 300\""
    echo "  $0 --image j0lama/ng-scope:latest --frag 200 --earfcn \"700 300\""
    echo "  $0 --image j0lama/ng-scope:latest --frag 200 --earfcn \"700 300\" --out enb_logs"
    echo "  $0 --image j0lama/ng-scope:latest --frag 200 --earfcn \"700 300\" --out enb_logs --timeout 60"
    exit 1
}

FRAG=0
TIMEOUT=0
IMAGE=ngscope
while [[ $# -gt 0 ]]; do
  case $1 in
    -i|--image)
      IMAGE="$2"
      shift # past argument
      shift # past value
      ;;
    -f|--frag)
      FRAG=$2
      shift # past argument
      shift # past value
      ;;
    -e|--earfcn)
      EARFCN=$2
      shift # past argument
      shift # past value
      ;;
    -o|--out)
      OUTPUT=$2
      shift # past argument
      shift # past value
      ;;
    -t|--timeout)
      TIMEOUT=$2
      shift
      shift
      ;;
    -h|--help)
      Help
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

# Checking arguments
#if [[ -z "$IMAGE" ]]; then
#    echo "Error: Image name argument missing"
#    echo "Execute '$0 --help' for more help"
#    exit 1
#fi
if [[ -z "$EARFCN" ]]; then
    echo "Error: List of EARFCN missing"
    echo "Execute '$0 --help' for more help"
    exit 1
fi

LOGS=$(realpath $OUTPUT)
echo $LOGS

#docker run -e HOST_HOSTNAME=`hostname` --name ng-scope -ti --privileged --rm -v $LOGS:/ng-scope/build/ngscope/src/logs/ $IMAGE ./start.sh $FRAG $(echo "$EARFCN" | tr -d '"')
docker run -e HOST_HOSTNAME=`hostname` --name ng-scope -ti --privileged -v /dev:/dev -v /proc:/proc --rm -v $LOGS:/ng-scope/build/ngscope/src/logs/ $IMAGE python3 start.py -f $FRAG -t $TIMEOUT -e $(echo "$EARFCN" | tr -d '"')

#if [[ ! -z "$OUTPUT" ]]; then
#    mv logs/ $OUTPUT
#fi