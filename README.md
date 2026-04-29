# big-O-evaluator

Desktop app for evaluating algorithm complexity.

## Structure

- `src/big_o_evaluator/`: application package and entrypoint
- `src/big_o_evaluator/core/`: algorithm analysis and evaluation logic
- `src/big_o_evaluator/ui/`: window and visualization code
- `src/big_o_evaluator/workers/`: background or threaded work
- `core/`, `ui/`, `workers/`: legacy top-level folders kept for now while the new package layout is introduced

## Run

```bash
python -m pip install -e .
big-o-evaluator
```
