library (ggplot2)



#makes graph of most common strategy
most_common_strategy <- read.csv("most_common.csv")


most_common_strategy$Condition <- as.factor(as.numeric(as.character(most_common_strategy$Condition)))
most_common_strategy$Common_Strategy <- as.character(most_common_strategy$Common_Strategy)


subset_data = subset( most_common_strategy, Condition != -0.5 && Condition != 0.0)
p <- ggplot( data = subset_data , aes( x = Common_Strategy, group = Condition, color = Condition, fill = Condition))
p <- p + geom_bar(position="dodge") + theme_minimal()
p <- p +  theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank()) 
p <- p + scale_x_discrete("Strategy") + scale_y_continuous("Frequency") 
p <- p + scale_fill_manual(values=c("#8CF582", "#82F5EB", "#828BF5")) + scale_color_manual(values=c( "#8CF582",  "#82F5EB", "#828BF5"))


ggsave("Most_Common_Strategies_Static_Competitor_More_Values.pdf")