library (reshape)
library (ggplot2)
library (dplyr)


#THIS IS FOR BITS OF MEMORY OVER TIME

bits_of_memory_df <- read.csv("all_bits_df_static_comp_more_values.csv")
#bits_of_memory_df <- as.data.frame(beaker::get('all_bits_df'))

#add
colnames(bits_of_memory_df) <- c('Row_Label', 'B0', 'B1', 'B2', 'B3', 'B4','Condition', 'Generation')

bits_of_memory_df$Row_Label <- NULL
bits_of_memory_df$Generation <- as.numeric(as.character(bits_of_memory_df$Generation))
bits_of_memory_df$Condition <- as.factor(as.numeric(as.character(bits_of_memory_df$Condition)))
bits_of_memory_df$B0 <- as.numeric(as.character(bits_of_memory_df$B0))
bits_of_memory_df$B1 <- as.numeric(as.character(bits_of_memory_df$B1))
bits_of_memory_df$B2 <- as.numeric(as.character(bits_of_memory_df$B2))
bits_of_memory_df$B3 <- as.numeric(as.character(bits_of_memory_df$B3))
bits_of_memory_df$B4 <- as.numeric(as.character(bits_of_memory_df$B4))


#Use for testing
#Dummy df columns
#B0 <- c(17, 17, 17, 17, 17, 17, 17, 18)
#B1 <- c(17, 17, 17, 17, 17, 17, 17, 17)
#B2 <- c(18, 17, 17, 17, 17, 17, 17, 17)
#B3 <- c(17, 17, 17, 18, 17, 17, 17, 17)
#B4 <- c(17, 17, 17, 17, 17, 17, 18, 17)
#Generation <- c(500, 500, 500, 500, 500, 500, 500, 500)
#Condition <- c(3, 3, 3, 3, 7, 7, 7, 7)
#Make new dummy data frame to test pairwise wilcox
#dummy_df <- data.frame(B0, B1, B2, B3, B4, Condition, Generation)
#dummy_df$Row_Label <- NULL
#dummy_df$Condition <- as.factor(dummy_df$Condition)
#bits_of_memory_df <- rbind(bits_of_memory_df, dummy_df)

#bits_of_memory_df


weights = 0:4
bits_of_memory_df$Mean <- apply(bits_of_memory_df, 1, function(d) {weighted.mean(weights, d[1:5])})

#want a smaller df
#for given condition and generation what is the mean of  the means
#aggregate( Mean~Generation + Condition, bits_of_memory_df, function(x){c(group_mean = mean(x))})
summary_df <- group_by(bits_of_memory_df, Condition, Generation) 

summary_df <- summarize(summary_df, group_mean = mean(Mean), group_sd = sd(Mean) )
#standard deviation
#print(summary_df)
#bits_of_memory_df$Generation <- c(1:nrow(bits_of_memory_df))




ggplot(data = summary_df, aes(x = Generation, y = group_mean, fill = Condition, ymin = group_mean - group_sd, ymax = group_mean + group_sd)) + geom_line(aes(color = Condition)) + theme_minimal() + geom_ribbon(alpha=.3) + theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank()) + scale_y_continuous("Average Bits of Memory")

ggsave("Average_Bits_Memory_Overtime_Static_Comp.pdf")


ggplot(data = subset(summary_df, Condition %in% c(0, 0.01, 0.03, 0.05, 0.075)), aes(x = Generation, y = group_mean, fill = Condition, ymin = group_mean - group_sd, ymax = group_mean + group_sd)) + geom_line(aes(color = Condition)) + theme_minimal() + geom_ribbon(alpha=.3) + theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank()) + scale_y_continuous("Average Bits of Memory") + scale_fill_manual(values=c("#F5828C", "#8CF582", "#82F5EB", "#828BF5")) + scale_color_manual(values=c( "#F5828C", "#8CF582",  "#82F5EB", "#828BF5"))

ggsave("Average_Bits_Memory_Overtime_Restricted_Static_Comp.pdf")



#Makes assumptions about data
#Have to check these assumptions
#Each sample is an indep random sample
#Distribution follows normal distrib
#Equal width
#MAKE HISTOGRAM TO CHECK THESE ASSUMPTIONS
#hist(bits_of_memory_df$Mean)

#ANOVA TEST
#How different are things
#anova_bits <- aov(bits_of_memory_df$Mean ~ bits_of_memory_df$Condition) 
#summary(anova_bits)


#TUKEY TEST
#Off of ANOVA
#Things are different so which ones are different
#TukeyHSD(anova_bits)


#KRUSKAL-WALLIS TEST
#How different are things
#Similar to Anova
#Doesn't assume normality of shape of graph
kruskal_bits <- kruskal.test(Mean ~ Condition, data = subset(bits_of_memory_df, bits_of_memory_df$Generation == 499))
end_df <- subset(bits_of_memory_df, bits_of_memory_df$Generation == 499)
kruskal_bits

#Wilcox and Rank Sum Test
#Like TUKEY but doesn't assume normality
pairwise.wilcox.test(end_df$Mean, end_df$Condition, "bonferroni")

warnings()