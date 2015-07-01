library (ggplot2)



#makes graph of most common strategy
most_common_strategy <- read.csv("most_common.csv")


most_common_strategy$Condition <- as.factor(as.numeric(as.character(most_common_strategy$Condition)))
most_common_strategy$Common_Strategy <- as.character(most_common_strategy$Common_Strategy)

ggplot( data = subset( most_common_strategy, Condition != -0.5 && Condition != 0.0), aes( x = Common_Strategy, group = Condition, color = Condition, fill = Condition)) + geom_bar(position="dodge") + theme_minimal() + theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank()) + scale_x_discrete("Strategy") + scale_y_continuous("Frequency")

ggsave("Most_Common_Strategies_5_Bits.pdf")