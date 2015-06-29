library (reshape)
library (ggplot2)
library (dplyr)


#THIS IS FOR BITS OF MEMORY OVER TIME

bits_of_memory_df <- read.csv("all_bits_df_self_memory.csv")
#bits_of_memory_df <- as.data.frame(beaker::get('all_bits_df'))

#add
colnames(bits_of_memory_df) <- c('Row_Label', 'B0', 'B1', 'B2', 'B3', 'B4', 'Condition', 'Generation')

bits_of_memory_df$Row_Label <- NULL
bits_of_memory_df$Generation <- as.numeric(as.character(bits_of_memory_df$Generation))
bits_of_memory_df$Condition <- as.factor(as.numeric(as.character(bits_of_memory_df$Condition)))
bits_of_memory_df$B0 <- as.numeric(as.character(bits_of_memory_df$B0))
bits_of_memory_df$B1 <- as.numeric(as.character(bits_of_memory_df$B1))
bits_of_memory_df$B2 <- as.numeric(as.character(bits_of_memory_df$B2))
bits_of_memory_df$B3 <- as.numeric(as.character(bits_of_memory_df$B3))
bits_of_memory_df$B4 <- as.numeric(as.character(bits_of_memory_df$B4))

weights = 0:4
bits_of_memory_df$Mean <- apply(bits_of_memory_df, 1, function(d) {weighted.mean(weights, d[1:5])})

#want a smaller df
#for given condition and generation what is the mean of  the means
#aggregate( Mean~Generation + Condition, bits_of_memory_df, function(x){c(group_mean = mean(x))})
summary_df <- group_by(bits_of_memory_df, Condition, Generation) 

summary_df <- summarize(summary_df, group_mean = mean(Mean), group_sd = sd(Mean) )
#standard deviation
print(summary_df)
#bits_of_memory_df$Generation <- c(1:nrow(bits_of_memory_df))
#bits_of_memory_df


ggplot(data = summary_df, aes(x = Generation, y = group_mean, fill = Condition, ymin = group_mean - group_sd, ymax = group_mean + group_sd)) + geom_line(aes(color = Condition)) + theme_minimal() + geom_ribbon(alpha=.3) + theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank()) + scale_y_continuous("Average Bits of Memory")

ggsave("Average_Bits_Memory_Overtime_Self_Memory.pdf")


ggplot(data = subset(summary_df, Condition %in% c(-0.5, 0, 0.01, 0.05, 0.075, 0.1, 0.2)), aes(x = Generation, y = group_mean, fill = Condition, ymin = group_mean - group_sd, ymax = group_mean + group_sd)) + geom_line(aes(color = Condition)) + theme_minimal() + geom_ribbon(alpha=.3) + theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank()) + scale_y_continuous("Average Bits of Memory")

ggsave("Average_Bits_Memory_Overtime_Restricted_Self_Memory.pdf")