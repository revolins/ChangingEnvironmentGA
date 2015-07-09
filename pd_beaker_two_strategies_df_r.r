library (reshape)
library (ggplot2)
library (dplyr)

#THIS IS FOR NUMBER OF STRATEGIES OVER GENERATIONS

#strategies_df <- as.data.frame(beaker::get('strategies_df'))
strategies_df <- read.csv("strategies_df.csv", header=FALSE)
#strategies_df <- read.csv("
#renaming column names in dataframe
colnames(strategies_df) <- c('Row_Label', seq(0, 500, 10), 'Condition', 'Strategy')

#should get rid of row labels
strategies_df$Row_Label <- NULL
strategies_df <- melt(strategies_df)


#rename axis

colnames(strategies_df)[2] <- "Generation"

#print(strategies_df)

#tell x is a number
strategies_df$Generation <- as.numeric(strategies_df$Generation) 

#tell y is a number
colnames(strategies_df)[3] <- "Frequency"
strategies_df$Frequency <- as.numeric(strategies_df$Frequency)

#print(strategies_df$Generation)

#makes pretty line graph with no background grid
ggplot(data = strategies_df, aes(x = Generation, y = Frequency, group = Strategy, color = Strategy)) +  geom_line() + theme_minimal() +  theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank(), legend.position ="none") + scale_x_continuous() 

ggsave("Strategy_Frequency_Plot.pdf")       	 		  		     		      		       	    





