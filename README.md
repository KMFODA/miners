# Opentensor Miners
Opentensor Miners

# Installing
With ≥python3.8 installed:
```bash
python3 -m pip install -e .
```

# Running openminers
```bash
import openminers
with openminers.TemplateMiner():
    pass
```

# Running Benchmarks
```bash
python3 benchmarks/base.py openai 
```

# TODO
- [x] Create this repo
- [x] Add setup.py
- [x] Add template text_to_text miner
- [x] Add template text_to_text forward tests 
- [x] Add benchmarks
- [ ] Add Wandb to miner
- [x] Add more miners
- [ ] Advance blacklist function
- [ ] Advance priority function
- [ ] Advance telemetry through wandb
- [ ] Add tests to miners
- [ ] Add benchmarks to miners