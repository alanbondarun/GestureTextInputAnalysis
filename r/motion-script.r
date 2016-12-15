# for ggplot()
# install.packages("ggplot2")
library(ggplot2)

# for summarySE()
# install.packages("Rmisc")
library(Rmisc)

motion_data <- read.csv("E:/documents/16_stable/motto_futari_de/gesture-pilot-exp-v2/res/motion-time-step.csv", header=T, sep=",")
motion_sum <- summarySE(motion_data, measurevar="time", groupvars=c("key", "motion"))
ggplot(data=motion_sum, aes(x=key, y=time, fill=motion)) +
  geom_bar(stat="identity", position = position_dodge()) +
  geom_errorbar(aes(ymin=time-se, ymax=time+se), position=dodge, width=.1) +
  scale_fill_manual(values = c("d1" = "#00cc99", "d2" = "#008060", "h1" = "#9966ff", "h2" = "#5500ff", "v1" = "#ff8000", "v2" = "#b35900")) +
  scale_x_discrete(name = "Input Character") +
  scale_y_continuous(name = "Average Input Time (msec)") +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="none")

motion_motion_sum <- summarySE(motion_data, measurevar="time", groupvars=c("motion"))

m_detailed_data <- read.csv("E:/documents/16_stable/motto_futari_de/gesture-pilot-exp-v2/res/motion-time-detailed.csv", header=T, sep=",")
m_detailed_sum <- summarySE(m_detailed_data, measurevar="time", groupvars=c("motion"))


