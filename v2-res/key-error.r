# for ggplot()
# install.packages("ggplot2")
library(ggplot2)

grouped_bar_width <- 0.9

# read key error data from .csv file
key_error_data <- read.csv("E:/documents/16_stable/motto_futari_de/gesture-pilot-exp-v2/res/key-error.csv", header=T, sep=",")

# plot TER with grouping by depth (1D Input)
key_error_1d <- key_error_data[which(key_error_data$method=='1DInput'), c("input", "terrrate", "depth")]

key_error_1d$bar_width <- grouped_bar_width
ke1_dfreq <- count(key_error_1d, "depth")
for (dpt in ke1_dfreq[ ,c("depth") ])
{
  key_error_1d$bar_width[ key_error_1d$depth == dpt ] <- grouped_bar_width *
    (ke1_dfreq[ which(ke1_dfreq$depth == dpt), c("freq") ] /
      max(ke1_dfreq[ ,c("freq") ]))
}
ggplot(data = key_error_1d, aes(x = input, y = terrrate)) +
  geom_bar(aes(width = bar_width), stat = "identity") +
  scale_x_discrete(name = "Input Character") +
  scale_y_continuous(name = "Error Rate (%)", limits = c(0, 16)) +
  theme(text = element_text(size=28), axis.text = element_text(size=28)) +
  facet_wrap(~depth, scale = "free")

# plot TER with grouping by depth (WatchWrite)
key_error_ww <- key_error_data[which(key_error_data$method=='4KWatchWrite'), c("input", "terrrate", "depth")]

key_error_ww$bar_width <- grouped_bar_width
kew_dfreq <- count(key_error_ww, "depth")
for (dpt in kew_dfreq[ ,c("depth") ])
{
  key_error_ww$bar_width[ key_error_ww$depth == dpt ] <- grouped_bar_width *
    (kew_dfreq[ which(kew_dfreq$depth == dpt), c("freq") ] /
      max(kew_dfreq[ ,c("freq") ]))
}
ggplot(data = key_error_ww, aes(x = input, y = terrrate)) +
  geom_bar(aes(width = bar_width), stat = "identity") +
  scale_x_discrete(name = "Input Character") +
  scale_y_continuous(name = "Error Rate (%)", limits = c(0, 16)) +
  theme(text = element_text(size=28), axis.text = element_text(size=28)) +
  facet_wrap(~depth, scale = "free")


