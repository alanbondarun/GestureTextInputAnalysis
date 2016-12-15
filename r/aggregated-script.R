# for ggplot()
# install.packages("ggplot2")
library(ggplot2)

# for summarySE()
# install.packages("Rmisc")
library(Rmisc)

filepath = "v3-res"
filename = "aggregated.csv"

input_data <- read.csv(paste(filepath, filename, sep="/"), header=T, sep=",")

# WPM plot
wpm_frame <- input_data[,c("Method", "Person", "Block", "WPM")]
wpm_smm <- summarySE(wpm_frame, measurevar="WPM", groupvars=c("Method", "Block"))
ggplot(wpm_smm, aes(x=Block, y=WPM, colour=Method)) +
	geom_errorbar(aes(ymin=WPM-se, ymax=WPM+se), width=.1) +
	geom_line() +
	geom_point() +
	theme(text = element_text(size=18), axis.text = element_text(size=14), legend.position="bottom")

wpm_b6 <- wpm_frame[ which(wpm_frame$Block==6), c("Method", "WPM") ]
aggregate(wpm_b6$WPM, list(wpm_b6$Method), mean)

wpm_b1 <- wpm_frame[ which(wpm_frame$Block==1), c("Method", "WPM") ]
aggregate(wpm_b1$WPM, list(wpm_b1$Method), mean)

# are there any significant differences btw first block and last block of each method?
wpm_b1n6_1d <- wpm_frame[ which((wpm_frame$Block==1 | wpm_frame$Block==6) &
		wpm_frame$Method=="1DInput"),
	c("Block", "WPM") ]
t.test(WPM ~ Block, data=wpm_b1n6_1d)

wpm_b1n6_ww <- wpm_frame[ which((wpm_frame$Block==1 | wpm_frame$Block==6) &
		wpm_frame$Method=="4KWatchWrite"),
	c("Block", "WPM") ]
t.test(WPM ~ Block, data=wpm_b1n6_ww)

# are there any significant differences among means of Method categories?
t.test(WPM ~ Method, data=wpm_b6)

# CER plot and one-way ANOVA
cer_frame <- input_data[,c("Method", "Person", "Block", "CER")]
cer_smm <- summarySE(cer_frame, measurevar="CER", groupvars=c("Method", "Block"))
ggplot(cer_smm, aes(x=Block, y=CER, colour=Method)) +
	geom_errorbar(aes(ymin=CER-se, ymax=CER+se), width=.1) +
	geom_line() +
	geom_point() +
	theme(text = element_text(size=18), axis.text = element_text(size=14), legend.position="bottom")

cer_b6 <- cer_frame[ which(cer_frame$Block==6), c("Method", "CER") ]
aggregate(cer_b6$CER, list(cer_b6$Method), mean)
cer_b1 <- cer_frame[ which(cer_frame$Block==1), c("Method", "CER") ]
aggregate(cer_b1$CER, list(cer_b1$Method), mean)

# are there any significant differences btw first block and last block of each method?
cer_b1n6_1d <- cer_frame[ which((cer_frame$Block==1 | cer_frame$Block==6) &
		cer_frame$Method=="1DInput"),
	c("Block", "CER") ]
t.test(CER ~ Block, data=cer_b1n6_1d)

cer_b1n6_ww <- cer_frame[ which((cer_frame$Block==1 | cer_frame$Block==6) &
		cer_frame$Method=="4KWatchWrite"),
	c("Block", "CER") ]
t.test(CER ~ Block, data=cer_b1n6_ww)

# are there any significant differences between means of Method categories?
t.test(CER ~ Method, data=cer_b6)

# TER (CER + UER) plot and one-way ANOVA (Not corrected error rate)
ter <- input_data["CER"] + input_data["NER"]
ter_frame <- input_data[,c("Method", "Person", "Block")]
ter_frame["TER"] <- ter
ter_smm <- summarySE(ter_frame, measurevar="TER", groupvars=c("Method", "Block"))
ggplot(ter_smm, aes(x=Block, y=TER, colour=Method)) +
	geom_errorbar(aes(ymin=TER-se, ymax=TER+se), width=.1) +
	geom_line() +
	geom_point() +
	theme(text = element_text(size=18), axis.text = element_text(size=14), legend.position="bottom")

ter_b6 <- ter_frame[ which(ter_frame$Block==6), c("Method", "TER") ]
aggregate(ter_b6$TER, list(ter_b6$Method), mean)
ter_b1 <- ter_frame[ which(ter_frame$Block==1), c("Method", "TER") ]
aggregate(ter_b1$TER, list(ter_b1$Method), mean)

# are there any significant differences btw first block and last block of each method?
ter_b1n6_1d <- ter_frame[ which((ter_frame$Block==1 | ter_frame$Block==6) &
		ter_frame$Method=="1DInput"),
	c("Block", "TER") ]
t.test(TER ~ Block, data=ter_b1n6_1d)

ter_b1n6_ww <- ter_frame[ which((ter_frame$Block==1 | ter_frame$Block==6) &
		ter_frame$Method=="4KWatchWrite"),
	c("Block", "TER") ]
t.test(TER ~ Block, data=ter_b1n6_ww)

# are there any significant differences between means of Method categories?
t.test(TER ~ Method, data=ter_b6)

