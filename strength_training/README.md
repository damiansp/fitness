# Strength Training
A weight training program that focuses on high-weight/low-reps with the goal of building strength efficiently. I was motivated to start doing this after reading Dr. Peter Attia's book _Outlive_, that suggests gaining strength is one of the best things people can do to maintain good health into old age.

## How To:
1. When using for the first time, create a .csv input file (see <a href="#inputs">Inputs</a> below for format), and place it in the `data/` directory.  You can call the file anything you want, but by default, the program will assume it is called "input.csv".
2. To run, go to the root of this directory on the command line, and run:
```./entrypoint.py```
...if you named your input file "input.csv" this will run fine, and output a file to `data/schedule.csv`.  If you used a different input file name, you will need to instead run:
```./entrypoint.py -i my_filename.csv```
...and similarly, if you want your output file named something other than "schedule.csv", you may add:
```./entrypoint.py -i my_input_file.csv -o my_outputfile.csv```

Running the above will create your output schedule, and _will also_ update the input file to be ready for the next cycle. So...

3. On subsequent runs, when you are ready to begin the next cycle, you do not need to update your input file, as that will have been done automatically. You can again just run:
```./entrypoint.py [-i my_input_file.csv] [-o my_outputfile.csv]```
where the bracketed parts are optional.

4. You will only need to manually change the input file in the event of failures, and you wish to manually change the training max or the per-cycle increment.


## Inputs:
Initial exercises may be input in the `data/` directory in .csv format (see full example in `data/input.csv`:

day|type   |exercise   |training_max|increment_per_cycle
---|-------|-----------|------------|-------------------
1  |main   |squat      |200         |10
1  |support|gm standing|90          |2.5
1  |support|db lunge   |90          |5
1  |support|situp      |20          |2.5
2  |main   |bench      |150         |5
2  |support|db flies   |80          |1.25
2  |support|...        |...         |...
...|...    |...        |...         |...


## Outputs:
A 4-week schedule of exercises, and updates the input file to be incremented for the following cycle


## Dev
### TODOs
- [ ] Create weight list form schedule


