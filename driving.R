library(tseries)

my_data <-  read.csv(file  = "/Users/jason/Downloads/driving data.csv", fill = TRUE, row.names = NULL)
attach(my_data)

Y <- driving
t <- date
covid <- covid.infection.modified
temp <- TEMPERATURE..C..
rainfall <- RAINFALL
lockdown <- lockdown.yes.no..1.0.
retail <-  retail_and_recreation_percent_change_from_baseline
grocery <- grocery_and_pharmacy_percent_change_from_baseline
parks <- parks_percent_change_from_baseline
transitchange <- transit_stations_percent_change_from_baseline 
workplaces <- workplaces_percent_change_from_baseline
residential <- residential_percent_change_from_baseline
low <- Estimate..Households..Total...25.000.to..34.999
high <- Estimate..Families..Total...100.000.to..149.999
unemployment <- Unemployment.Rates

summary(Y)
summary(t)

adf.test(Y, alternative = "stationary", k = 0)

acf(Y)
pacf(Y)

arima(Y,order=c(1,0,1),xreg = cbind(covid, grocery, transitchange, workplaces, residential))
arima(Y,order=c(1,1,1),xreg = cbind(covid, grocery, transitchange, workplaces, residential))