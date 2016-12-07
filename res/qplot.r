qf1 <- qdata[ ,c("method","q1") ]
qf1_smm <- summarySE(qf1, measurevar="q1", groupvars=c("method"))
qf2 <- qdata[ ,c("method","q2") ]
qf2_smm <- summarySE(qf2, measurevar="q2", groupvars=c("method"))
qf3 <- qdata[ ,c("method","q3") ]
qf3_smm <- summarySE(qf3, measurevar="q3", groupvars=c("method"))
qf4 <- qdata[ ,c("method","q4") ]
qf4_smm <- summarySE(qf4, measurevar="q4", groupvars=c("method"))
qf5 <- qdata[ ,c("method","q5") ]
qf5_smm <- summarySE(qf5, measurevar="q5", groupvars=c("method"))


ggplot(data=qf1_smm, aes(x=method, y=q1, fill=method)) +
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin=q1-se, ymax=q1+se), width=.1) +
  ylim(0, 7) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="none", axis.title.x=element_blank(), axis.title.y=element_blank()) +
  coord_flip()

ggplot(data=qf2_smm, aes(x=method, y=q2, fill=method)) +
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin=q2-se, ymax=q2+se), width=.1) +
  ylim(0, 7) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="none", axis.title.x=element_blank(), axis.title.y=element_blank()) +
  coord_flip()
  
ggplot(data=qf3_smm, aes(x=method, y=q3, fill=method)) +
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin=q3-se, ymax=q3+se), width=.1) +
  ylim(0, 7) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="none", axis.title.x=element_blank(), axis.title.y=element_blank()) +
  coord_flip()
  
ggplot(data=qf4_smm, aes(x=method, y=q4, fill=method)) +
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin=q4-se, ymax=q4+se), width=.1) +
  ylim(0, 7) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="none", axis.title.x=element_blank(), axis.title.y=element_blank()) +
  coord_flip()
  
ggplot(data=qf5_smm, aes(x=method, y=q5, fill=method)) +
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin=q5-se, ymax=q5+se), width=.1) +
  ylim(0, 7) +
  theme(text = element_text(size=18), axis.text = element_text(size=18), legend.position="none", axis.title.x=element_blank(), axis.title.y=element_blank()) +
  coord_flip()