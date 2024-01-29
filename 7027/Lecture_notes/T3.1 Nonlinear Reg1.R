############################################################
#Part 1: Polynomial Regression
#load the required packages
library(ISLR)
#Wage<-read.table("wage.txt",sep=',')
#This means that the database is searched by R when evaluating a variable, 
#so objects in the database can be accessed by simply giving their names.
attach(Wage)

#This simply creates the polynomial basis functions on the fly.
#to protect terms like age^2 via a wrapper function I()
#equivalent to poly(age 4, raw=T)
fit1a<-lm(wage~age+I(age^2)+I(age^3)+I(age^4),data=Wage)
summary(fit1a)
fit1b<-lm(wage~cbind(age,age^2,age^3,age^4),data=Wage)
summary(fit1b)


#as comparison
fit2<-lm(wage~age+age^2+age^3+age^4,data=Wage)
summary(fit2)

fit3<-lm(wage~poly(age,4,raw=T),data=Wage)
#We can also use poly() function  to obtain age, age^2, age^3, age^4.
#directly if we prefer. We can do this by using raw<- TRUE
summary(fit3)

#We now create a grid of values for age at which we want predictions.
#Then call the generic  predict(), specifying  that we want standard errors as well
agelims=range(age)
age.grid=seq(from=agelims[1],to=agelims[2])
preds<-predict(fit1a,newdata=list(age=age.grid),se=TRUE)
plot(age,wage,xlim=agelims,cex=.5,col="darkgray")
lines(age.grid,preds$fit,lwd=2,col="blue")
se.bands <-cbind(preds$fit+2*preds$se.fit,preds$fit-2*preds$se.fit)
matlines(age.grid,se.bands,lwd=1, col='blue',lty=3)



# The estimates become different when raw=F (default).
fit4<-lm(wage~poly(age,4),data=Wage)
summary(fit4)


# But raw=T & raw=F are mathmatically equivalent
preds_rawT<-predict(fit3,newdata=list(age=age.grid),se=TRUE)
preds_rawF<-predict(fit4,newdata=list(age=age.grid),se=TRUE)
preds_rawT$fit[1:5]
preds_rawF$fit[1:5]

#In performing a polynomial regression, we must decide on the degree of polynomial.
#polynomial to use.One way to do this is by using hypothesis testing.
fit.1<-lm(wage~age,data=Wage)
fit.2<-lm(wage~poly(age,2),data=Wage)
fit.3<-lm(wage~poly(age,3),data=Wage)
fit.4<-lm(wage~poly(age,4),data=Wage)
fit.5<-lm(wage~poly(age,5),data=Wage)
anova(fit.1,fit.2,fit.3,fit.4,fit.5)
#The p-value comparing the linear Model 1 to the quadratic Model 2 is 
#essentially zero,indicating that a linear fit is not sufficient.
#Similarly the p-value comparing the quadratic Model 2 to the cubic Model 3
#is very low(0.0017), so the quadratic fit is also insufficient. The p value
#comparing the cubic and degree-4 polynomials, Model 3 and 4, is '
#approximately 5% while degree-5 polynomial Model 5 seems to be insignificant
#because its p-value is 0.37. Hence, a cubic polynomial
#appears to provide a reasonable fit to the data, but lower or higher 
#models are not justified.


#Use polynomial regression together with other variables.
fit.1a<-lm(wage~education+age,data=Wage)
fit.2a<-lm(wage~education+poly(age,2),data=Wage)
fit.3a<-lm(wage~education+poly(age,3),data=Wage)
fit.4a<-lm(wage~education+poly(age,4),data=Wage)
fit.5a<-lm(wage~education+poly(age,5),data=Wage)
anova(fit.1a,fit.2a,fit.3a,fit.4a,fit.5a)


#Next, we consider the task of predicting whether an individual earns more than $250,000 per year.
#Use the wrapper function I() to create this binary response.
#The expression wage>250 evaluates to a logical variable containing
#TRUES and FALSES, which glm() coerces to binary by setting the TRUES to 1
#and FALSES to 0
fit<-glm(I(wage>250)~poly(age,4),data=Wage,family=binomial)
preds<-predict(fit,newdata=list(age=age.grid),se=TRUE)
pfit<-exp(preds$fit)/(exp(preds$fit)+1)
se.bands_logit<-cbind(preds$fit-2*preds$se.fit,
				preds$fit+2*preds$se.fit)
se.bands<-exp(se.bands_logit)/(1+exp(se.bands_logit))

#Note that we could have directly computed the probabilities by setting
#type="response" option in the predict() function
#However, the corresponding confidence interval would not be valid
#because we end up with negative probabilities!
pred2<-predict(fit,newdata=list(age=age.grid),type="response",se=TRUE)
range(pred2$fit-2*pred2$se.fit)

plot(age,I(wage>250),xlim=agelims,cex=.5,col="darkgray")
#We have drawn the age values corresponding to the observations with 
#values above 250 as gray points on the top of plot, and those
#values below 250 are gray points on the bottom of plot,
lines(age.grid,pfit,lwd=2,col="blue")
matlines(age.grid,se.bands,lwd=1, col='blue',lty=3)

#In order to fit a step function as discussed in Section 7.2, we use a cut() function
table(cut(age,4))
fit<-lm(wage~cut(age,4),data=Wage)
summary(fit)
#Here cut() automatically picked the cutpoints at 33.5, 49 and 64.5 years
#of age(using equal distance).
#We could also have specified our own cutpoints directly using the 
#breaks option. The function cut() returns ordered categorical variable. 
#The lm() function then creates a set of dummy variables for us in the regression.
#The age<33.5 category is left out, so the intercept coefficient $94,160
#can be interpreted as the average salary for those under 33.5 years of
#age, and the other coefficients can be interpreted as the average additional
#salary for those in other age groups.


#We can produce predictions and plot as we did in the case of polynomial fit.
agelims=range(age)
age.grid=seq(from=agelims[1],to=agelims[2])
preds<-predict(fit,newdata=list(age=age.grid),se=TRUE)
plot(age,wage,xlim=agelims,cex=.5,col="darkgray")
lines(age.grid,preds$fit,lwd=2,col="blue")
se.bands <-cbind(preds$fit+2*preds$se.fit,preds$fit-2*preds$se.fit)
matlines(age.grid,se.bands,lwd=1, col='blue',lty=3)

preds<-predict(fit,newdata=list(age=age.grid),se=TRUE)
plot(age,wage,xlim=agelims,cex=.5,col="darkgray")
lines(age.grid,preds$fit,lwd=2,col="blue")
se.bands <-cbind(preds$fit+2*preds$se.fit,preds$fit-2*preds$se.fit)
matlines(age.grid,se.bands,lwd=1, col='blue',lty=3)
