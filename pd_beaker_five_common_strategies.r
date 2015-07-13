library (ggplot2)
library(reshape2)


#makes graph of most common strategy
most_common_strategy <- read.csv("most_common.csv")


most_common_strategy$Condition <- as.factor(as.numeric(as.character(most_common_strategy$Condition)))
most_common_strategy$Common_Strategy <- as.character(most_common_strategy$Common_Strategy)


subset_data = subset( most_common_strategy, Condition != -0.5 && Condition != 0.0)

dat = dcast(subset_data, Common_Strategy ~ Condition, fun.aggregate = length)
dat.melt = melt(dat, id.vars = "Common_Strategy")

dat.melt <- within(dat.melt, 
                   Common_Strategy <- factor(Common_Strategy, 
                                      levels=c("0~~", "00~1~", "01~1~", "0001~11~")))



ggplot(dat.melt, aes(x = Common_Strategy,y = value, fill = variable)) +
  geom_bar(position="dodge", stat = "identity", colour = "black") + 
  geom_text(aes(label = value), position = position_dodge(width = .8), vjust = -0.5) +
  theme_minimal() +
  theme(panel.grid.major = element_blank(), panel.background = element_blank(), panel.grid.minor = element_blank()) +
  scale_x_discrete("Strategy") + scale_y_continuous("Frequency", limits = c(0, 22)) +
  scale_fill_manual(values=c("#8CF582", "#82F5EB", "#828BF5")) + scale_color_manual(values=c( "#8CF582",  "#82F5EB", "#828BF5"))


ggsave("Most_Common_Strategies_Static_Competitor_More_Values.pdf")