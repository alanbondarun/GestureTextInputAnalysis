# for ggplot()
# install.packages("ggplot2")
library(ggplot2)

# for summarySE()
# install.packages("Rmisc")
library(Rmisc)

# for rename()
library(plyr)

# for grid.draw()
library(grid)

oned_name <- "1DInput"
ww_name <- "4KWatchWrite"
dodge <- position_dodge(width = 0.9)
grouped_bar_width <- 0.9

input_data <- read.csv("E:/documents/16_stable/motto_futari_de/gesture-pilot-exp-v2/res/keypress_time.csv", header=T, sep=",")

frame_avg1d <- input_data[, c("input", "oned_avgtime", "oned_stdev", "oned_depth")]
frame_avg1d$group <- oned_name
frame_avg1d <- rename(frame_avg1d, c("oned_avgtime"="avgtime", "oned_stdev"="stdev", "oned_depth"="depth"))
frame_avgww <- input_data[, c("input", "ww_avgtime", "ww_stdev", "ww_depth")]
frame_avgww$group <- ww_name
frame_avgww <- rename(frame_avgww, c("ww_avgtime"="avgtime", "ww_stdev"="stdev", "ww_depth"="depth"))

# plot whole keys
frame_avg <- rbind(frame_avg1d, frame_avgww)
ggplot(data=frame_avg1d, aes(x=input, y=avgtime)) +
  geom_bar(stat="identity", position = position_dodge()) +
  geom_errorbar(aes(ymin=avgtime-stdev, ymax=avgtime+stdev), position=dodge, width=.1) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="bottom")
  
ggplot(data=frame_avgww, aes(x=input, y=avgtime)) +
  geom_bar(stat="identity", position = position_dodge()) +
  geom_errorbar(aes(ymin=avgtime-stdev, ymax=avgtime+stdev), position=dodge, width=.1) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="bottom")

# group keys by depth (WatchWrite)
frame_avgww$bar_width <- 0.9
frame_avgww$bar_width[frame_avgww$depth==1] <- 0.9 * (5/14)
frame_avgww$bar_width[frame_avgww$depth==2] <- 0.9 * (11/14)
ggplot(data=frame_avgww, aes(x=input, y=avgtime)) +
  geom_bar(aes(width=bar_width), stat="identity") +
  geom_errorbar(aes(ymin=avgtime-stdev, ymax=avgtime+stdev), width=.1) +
  theme(text = element_text(size=28), axis.text = element_text(size=28), axis.text.x = element_text(angle=45, hjust=1)) +
  ylim(0, 8) +
  facet_wrap(~depth, scale="free")
  
# group keys by depth (1D Input)
frame_avg1d$bar_width <- 0.9
frame_avg1d$bar_width[frame_avg1d$depth==1] <- 0.9 * (5/14)
frame_avg1d$bar_width[frame_avg1d$depth==2] <- 0.9 * (11/14)
ggplot(data=frame_avg1d, aes(x=input, y=avgtime)) +
  geom_bar(aes(width=bar_width), stat="identity") +
  geom_errorbar(aes(ymin=avgtime-stdev, ymax=avgtime+stdev), width=.1) +
  theme(text = element_text(size=28), axis.text = element_text(size=28), axis.text.x = element_text(angle=45, hjust=1)) +
  ylim(0, 8) +
  facet_wrap(~depth, scale="free")
  
# group keys by distance (# of passed areas for each input)
frame_avg1d_dist <- input_data[, c("input", "oned_avgtime", "oned_stdev", "oned_npassedarea")]
frame_avg1d_dist <- rename(frame_avg1d_dist, c("oned_avgtime"="avgtime", "oned_stdev"="stdev", "oned_npassedarea"="distance"))

frame_avg1d_dist$bar_width <- 0.9
frame_avg1d_dist$bar_width[frame_avg1d_dist$distance==1] <- 0.9 * (5/9)
frame_avg1d_dist$bar_width[frame_avg1d_dist$distance==2] <- 0.9 * (6/9)
frame_avg1d_dist$bar_width[frame_avg1d_dist$distance==4] <- 0.9 * (8/9)
frame_avg1d_dist$bar_width[frame_avg1d_dist$distance==5] <- 0.9 * (2/9)
ggplot(data=frame_avg1d_dist, aes(x=input, y=avgtime)) +
  geom_bar(aes(width=bar_width), stat="identity") +
  geom_errorbar(aes(ymin=avgtime-stdev, ymax=avgtime+stdev), width=.1) +
  theme(text = element_text(size=28), axis.text = element_text(size=28), axis.text.x = element_text(angle=45, hjust=1)) +
  ylim(0, 8) +
  facet_wrap(~distance, ncol=5, scale="free")
  
motion_data <- read.csv("E:/documents/16_stable/motto_futari_de/gesture-pilot-exp-v2/res/motion_time.csv", header=T, sep=",")
motion_sum <- summarySE(motion_data, measurevar="time", groupvars=c("key", "motion"))
ggplot(data=motion_sum, aes(x=key, y=time, fill=motion)) +
  geom_bar(stat="identity", position = position_dodge()) +
  geom_errorbar(aes(ymin=time-se, ymax=time+se), position=dodge, width=.1) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="bottom")

motion_motion_sum <- summarySE(motion_data, measurevar="time", groupvars=c("motion"))

# by-person key press time
by_person_data <- read.csv("E:/documents/16_stable/motto_futari_de/gesture-pilot-exp-v2/res/keytime-by-person.csv", header=T, sep=",")
byp_1d <- by_person_data[ which(by_person_data$method == '1DInput'),
  c('person', 'input', 'avgtime', 'stdev', 'depth') ]
byp_ww <- by_person_data[ which(by_person_data$method == '4KWatchWrite'),
  c('person', 'input', 'avgtime', 'stdev', 'depth') ]

# plot by-person key press time (1D Input)
ggplot(data = byp_1d, aes(x = input, y = avgtime, fill = person)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  scale_x_discrete(name = "Input Character") +
  scale_y_continuous(name = "Average Input Time (sec)", limits = c(0, 8)) +
  geom_errorbar(aes(ymin=avgtime-stdev, ymax=avgtime+stdev), position = dodge, width=.1) +
  theme(text = element_text(size=28), axis.text = element_text(size=28), axis.text.x = element_text(angle=45, hjust=1), legend.position = "none") +
  facet_wrap(~depth, scale="free")

# plot by-person key press time (WatchWrite)
ggplot(data = byp_ww, aes(x = input, y = avgtime, fill = person)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  scale_x_discrete(name = "Input Character") +
  scale_y_continuous(name = "Average Input Time (sec)", limits = c(0, 8)) +
  geom_errorbar(aes(ymin=avgtime-stdev, ymax=avgtime+stdev), position = dodge, width=.1) +
  theme(text = element_text(size=28), axis.text = element_text(size=28), axis.text.x = element_text(angle=45, hjust=1), legend.position = "none") +
  facet_wrap(~depth, scale="free")


