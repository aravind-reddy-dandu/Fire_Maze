library(dplyr)
library(ggplot2)


Dataset<- read.csv("thinning.csv", header=TRUE) 

Before = Dataset$BeforeThinning
After = Dataset$AfterThinning
rho = Dataset$Rho

plot(rho, Before, type="o", col="blue", pch="o", lty=1, ylim=c(0,100), ylab="Nodes Explored") + 
  points(rho, After, type="o", col="red", pch="o", lty=1) + 
  legend(0,100, legend=c("A-Star Manhattan","After Maze Thinning"), col=c("blue","red"),
         lty=c(1,2), ncol=1) 