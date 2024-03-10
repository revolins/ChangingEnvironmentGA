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

# Example Run Command
```
python changing_environment_ga.py -c config/pd_config.ini -o pd_test
```

# Command Line Arguments
* -c  config file location
* -o  desired output directory
