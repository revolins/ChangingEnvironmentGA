# Measuring Selective Pressures for Increased Memory Value in Iterated Prisoner’s Dilemma
This project quantifies the effect of noisy opponents on average memory length in an evolving population of IPD strategies. 

## Researchers:
Karen Suzue, Alec Said, Jay Revolinsky

# We assume that the user has anaconda/miniconda installed
https://docs.anaconda.com/free/miniconda/miniconda-install/

# Build Environment
```
conda env create -f environment.yml
```

# Startup Environmnet
```
conda activate memGA
```

# Test Run Commands
```
python changing_environment_ga.py -o pd_test
```

# Static Experiment (Note: Default Number of Tests = 100 or --nt 100)
```
python test.py --static --nt 2
```

# Low Mutation, Co-Evolutionary Experiment
```
python test.py --mut_rat 0.01 --nt 2
```

# High Mutation, Co-Evolutionary Experiment
```
python test.py --mut_rat 0.1 --nt 2
```

# Example SLURM Job Submission (Run = automatic submission)
```
python slurm.py --mut_rat 0.01 --noise 0.01 --run
```

# changing_environment_ga.py -- Command Line Arguments
## (Required)
* -o, --output_folder   desired output directory


## (Optional)
* --seed, --s   value to seed runs, for reproducibility
* --number_of_generations, --ng     number of generations for organisms (DEFAULT = 500)
* --number_of_organisms, --no   number of organisms involved in a given population (DEFAULT = 10)
* --org_type    Type of organism used in experiment, PD uses PDOrg (DEFAULT = pd)
* --tournament_size, --ts  Size of tournament for competing organisms (DEFAULT = 8)
* --verbose     True = full output, False = organism output (DEFAULT = True) (?)
* --number_of_rounds, --nr  Number of rounds in a given tournament before next generation decided (DEFAULT = 64)
* --temptation, Value of defecting when other organism cooperates (DEFAULT = 5)
* --reward, Value of cooperating when other organism cooperates (DEFAULT = 3)
* --punishment, Value of defecting when other organism defects (DEFAULT = 1)
* --sucker, Value of cooperating when other organism defects (DEFAULT = 0)
* --proportion_cost_per_memory_bit, --m_c   Fitness cost imposed for each memory bit organism has (DEFAULT = 0.0)
* --max_bits_of_memory, --max_m     Limit on organism's memory list bits (DEFAULT = 4)
* --max_bits_of_summary, --max_s    Limit on organism's decision list bits (DEFAULT = 4)
* --mutation_likelihood_of_bits_of_memory "--ml_mem",  Likelihood that memory list mutates after mutation decided (DEFAULT = 1.0)
* --mutation_likelihood_of_initial_memory_state, --ml_dec Likelihood that decision list mutates after mutation decided (DEFAULT = 1.0)
* --toggle_self_memory_on   True = Organism remembers their moves, False = Organism ignores their past moves (DEFAULT = False) (?)
* --mutation_rate, --mr  Mutation Rate to determine if organism will mutate during a given generation (DEFAULT = 0.0)
* --output_frequency    Rate at which organisms output their state (DEFAULT=10)
* --selection_by_static_competitor, --static    True = static, False = co-evolutionary (DEFAULT = False)
