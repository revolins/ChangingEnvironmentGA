import csv
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#import scipy.stats as stats
import pickle
import operator

COLORS = ["silver", "maroon", "red", "purple", "fuchsia", "green", "lime", "olive", "yellow",
              "navy", "blue", "teal", "aqua"]

def main():
    test_dir = "output_test"
    data = get_data(test_dir)
    #data = get_pickled_data(test_dir)
    pop_costs = None
    mutation_bits = "0.5"
    mutation_initials = "0.1"
    plot_aggregate_over_time(data, pop_costs, mutation_bits, mutation_initials, test_dir)



def get_data(common_dir):
    """Version of get_data that doesn't use cPickle"""
    #Make a new dictionary
    data = {}
    #For each sub directory...
    for sub_dir in os.listdir(common_dir):
        #If it's not actually a directory, skip it
        if not os.path.isdir(common_dir + "/" + sub_dir):
            continue
        #Grab the meaningful config name
        sub_dir_name_list = sub_dir.split("/")[-1].split(".")
        config = ".".join(sub_dir_name_list[:-1])
        #removes gen quick fix
        config = config[:-3]
        config = config.split("_")
        config = tuple(config)

        #Make sure the config name is in the dictionary
        if config not in data:
            data[config] = []

        data[config].append(pd.read_csv(common_dir+"/"+sub_dir+"/bits_of_memory_overtime.csv"))

    return data


def plot_aggregate_over_time(data, pop_cost=None, mutation_bit=None, mutation_initial=None, directory="."):
    plt.clf()
    colors = [color for color in COLORS]
    ax = plt.subplot(111)
    for config in data:
        if (pop_cost is not None and pop_cost != config[0]):
            continue
        if (mutation_bit is not None and mutation_bit != config[1]):
            continue
        if (mutation_initial is not None and mutation_initial != config[2]):
            continue

        averages_df_list = []
        all_runs_averages = []
        #gets averages in each data frame
        for df in data[config]:
            df_weighted = df["Organisms With 1 Bits of Memory"]
            num_orgs = df.sum(1)
            
            for i in range(2,len(df.columns)):
                df_weighted +=  df["Organisms With {0} Bits of Memory".format(i)].multiply(i)
           
            averages_df_list.append(df_weighted.multiply(1.0 / num_orgs))

        #averages all the runs
        for gen in range(len(averages_df_list[0])):
            df_sum = 0.0
            for df in averages_df_list:
                df_sum += df[gen]
            all_runs_averages.append(df_sum / len(averages_df_list))
        
        x = [val for val in range(len(all_runs_averages))]            
        try:
            ax.plot(x, all_runs_averages, color=colors.pop(), label=(config))
        except:
            colors = [color for color in COLORS]
            ax.plot(x, all_runs_averages, color=colors.pop(), label=(config))
    
    handles, labels = ax.get_legend_handles_labels()
    hl = sorted(zip(handles, labels), key = operator.itemgetter(1))
    handles2, labels2 = zip(*hl)
    

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(handles2, labels2, bbox_to_anchor=(1, 1), loc=2, mode="expand", borderaxespad=0.)
    plt.xlabel("Generation")
    plt.ylabel("Average Bits of Memory")
    
    plt.savefig(directory+"/average_bits_of_memory_" + str(pop_cost) + "_" + str(mutation_bit) + "_" + str(mutation_initial) + ".png")

def plot_stddev_over_time(data, key=None, directory="."):
    plt.clf()
    lines = {}
    colors = [color for color in COLORS]
    ax = plt.subplot(111)
    for config in data:
        if (key != None and key not in config):
            continue
        series = []
        for run in range(len(data[config])):
            series.append(data[config][run][1]["Ref_Standard_Deviation"])
        
        averages = []
        #stdevs = []

        for i in range(len(series[0])):
            add_factor = 0
            #if "rana" in config:
            #    add_factor = 20000
            devs = [np.log(s[i]) for s in series]
            averages.append(sum(devs)/float(len(devs)))
        lines[config] = Line2D(data[config][0][1]["Generation"], averages)
    
        x = data[config][0][1]["Generation"]
        try:
            ax.plot(x, averages, color=colors.pop(), label=(config.split("_")[1]))
        except:
            colors = [color for color in COLORS]
            ax.plot(x, averages, color=colors.pop(), label=(config.split("_")[1]))
    
    handles, labels = ax.get_legend_handles_labels()
    labels = [float(label) for label in labels]
    hl = sorted(zip(handles, labels), key = operator.itemgetter(1))
    handles2, labels2 = zip(*hl)
    labels2 = [str(label) for label in labels2]

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend(handles2, labels2, bbox_to_anchor=(1, 1), loc=2, mode="expand", borderaxespad=0.)
    plt.xlabel("Generation")
    plt.ylabel("Log of Standard Deviation")
    #plt.figlegend([lines[l] for l in lines], [l for l in lines])
    plt.savefig(directory+"/diversity_over_time_"+key+"_10000gen.png")

def plot_average_final_fitness(data, key=None, directory="."):
    plt.clf()
    colors = [color for color in COLORS]
    ax = plt.subplot(111)
    for config in data:
        corrs = []
        finals = []
        if key == None or key in config:
            for run in range(len(data[config])):
                corrs.append(data[config][run][0])
                add_factor=0
                #if "rana" in config:
                #    add_factor = 20000
                finals.append(add_factor+float(data[config][run][1]["Ref_Average_Fitness"][-1:]))
                #finals.append(float(data[config][run]["best_reference"]["Best_fitness"][-1:]))
            try:
                ax.plot(corrs, np.log(finals), marker=".", ls="", color=colors.pop(),
                        label=(config.split("_")[1]))
            except:
                colors = [color for color in COLORS]
                ax.plot(corrs, np.log(finals), marker=".", ls="", color=colors.pop(),
                        label=(config.split("_")[1]))
    
    handles, labels = ax.get_legend_handles_labels()
    labels = [float(label) for label in labels]
    hl = sorted(zip(handles, labels), key = operator.itemgetter(1))
    handles2, labels2 = zip(*hl)
    labels2 = [str(label) for label in labels2]

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend(handles2, labels2, bbox_to_anchor=(1, 1), loc=2, mode="expand", borderaxespad=0.)
    plt.xlabel("Correlation")
    plt.ylabel("Log of Reference Average Fitness")
    plt.savefig(directory+"/correlation_vs_final_fitness_scatter_"+key+".png")

if __name__ == "__main__":
    main()
        
