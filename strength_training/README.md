# Strength Training
A weight training program that focuses on high-weight/low-reps with the goal of building strength efficiently. I was motivated to start doing this after reading Dr. Peter Attia's book _Outlive_, that suggests gaining strengh is one of the best things people can do to maintain good health into old age.


# TODOs
- [X] Make class for a week
- [X] Make class for a cycle
- [X] Read inputs form various formats
- [X] Output weekly schedule to csv
- [ ] Store weekly params
- [ ] Check failures or updates
- [ ] Get next week


## Inputs:
Initial exercises may be input in the `data/` directory with any of the following formats:
- csv:

day|type   |exercise   |training_max|increment_per_cycle
---|-------|-----------|------------|-------------------
1  |main   |squat      |200         |10
1  |support|gm standing|90          |2.5
1  |support|db lunge   |90          |5
1  |support|situp      |20          |2.5
2  |main   |bench      |150         |5
2  |support|db flies   |80          |1.25
2  |support|...        |...         |...

- pickle: a pickled dictionary formatted as:
```{python}
[
    {
        'main': [('Squat', 188.)],  # may contain multiple tuples
        'support': [
             ('GM Standing', 76.5),
             ('DB Lunge', 69.5),
             ('Situp', 17.1)
         ]
    },
    {
        'main': [('Bench', 139.)],
        'support': [
             ('DB Flies', 69.5),
             ('Wide Dips', 14.54),
             ('Knuckle Duster', 24.)
        ]
    },
    {
        'main': [('Deadlift', 215.)],
        'support': [
             ('DB Skull Crusher', 20.75),
             ('Kroc Rows', 39.5),
             ('Situps', 17.1)
        ]
    },
    {
        'main': [('Overhead Press', 106.5)],
        'support': [
            ('Pullup', 10.),
            ('Curl', 20.75),
            ('Knuckle Duster', 24.)
        ]
    }
]
```
...where each dictionary represents a single day's exercises.
- json: A json object formatted as the `pickle` example above, but with lists in place of the tuples


