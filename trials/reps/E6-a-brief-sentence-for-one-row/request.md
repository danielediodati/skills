# Request

The user, 2026-10-03, after the closing eval pass of ticket 14.4 (`docs/work/14-this-workout/issues/04-this-workout-or-from-now-on.md`) in REPS at `ed911df`, paraphrased:

> Explain the first miss. What happens in the planner: does it read free text, or is there a rule that removes only one exercise?

The pass, as the next commit's ticket records it (`4a5af5f`):

> Closing pass, 2026-10-03, 3 repetitions, on ADR-0011's choices: **routed 48/57 (84%)**, **held 30/31 (96%)**, $1.22, 14 s a run.
>
> | row | what happened |
> |---|---|
> | lunges-again 3/3, no-plank 2/3, away, twenty-bare, hinge-excluded | asked «solo oggi o d'ora in poi?» instead of acting |
> | hate-bench 1/3 | «la tengo a mente» with nothing kept |
> | you-choose plan 1/3 | `Front_Barbell_Squat`, «front squat replaces back squat»: «niente squat» read as one squat out |

The row, from `docs/adapting/eval-set.toml`: `you-choose` says «oggi niente squat, proponi tu», goes to `adapt_this_workout`, `without_pattern = ["squat"]`.
