REST=${1:-0.5}
WORK=0.06666666666667
TIME=`echo "$WORK*30 + $REST*30" | bc`
echo Running with $REST min rest time for a total time of: $TIME
python3 entypoint.py -c kbc -t $TIME -w $WORK -r $REST
